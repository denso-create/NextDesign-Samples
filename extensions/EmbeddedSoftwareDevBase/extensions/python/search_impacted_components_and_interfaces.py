"""機能 : IFの影響箇所を抽出

選択されたソフトウェアコンポーネントまたは提供インタフェースを起点に、
影響を受けるソフトウェアコンポーネントとインタフェースを探索し、検索結果に登録します。
エディタでダイアグラムを表示中の場合は、影響箇所の経路となるコネクタも検索結果に登録します。

処理概要
    - エディタで選択中のモデルが調査対象のクラスであることを確認します。
    - カレントエディタで表示中のERダイアグラムからコネクタを取得します。
    - 調査対象のモデルから影響箇所をスタックベースで探索し、検索結果に登録します。
    - 検索結果をユーザに通知します。
"""

# =======================================
# 外部ファイル・モジュール読み込み
# =======================================
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple  # 型検査中か否かを表すTYPE_CHECKINGと、型注釈で使う型
import utils      # 汎用関数
import metamodel  # メタモデル情報

# エントリポイントであるmain.py以外でndモジュールをインポートすると実行時にエラーになります。
# そのため、TYPE_CHECKINGを用いて型検査時のみインポートします。
if TYPE_CHECKING:
    from nd import *

# =======================================
# ユーザが変更する設定値（パラメータ類）
# この領域を編集して、操作対象やメッセージを変更できます。
# =======================================

# ---------------------------------------
# 調査対象のクラス名
# 調査の起点として選択できるモデルのクラス名を定義します。
# ---------------------------------------
SEARCH_TARGET_CLASSES = [
    metamodel.CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT,
    metamodel.CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN
]

# ---------------------------------------
# 検索結果に関する定義
# ---------------------------------------
SEARCH_NAME = "IFの影響箇所"
SEARCH_MATCH_TYPE = "match"

# 検索結果に設定するフィールド名
SEARCH_FIELD_ORIGIN = "Name"
SEARCH_FIELD_INTERFACE = "Name"
SEARCH_FIELD_COMPONENT = "Name"
SEARCH_FIELD_CONNECTOR = None  # Noneを指定することで、フィールドを指定せずに検索結果に登録します。

# 検索結果に設定するメッセージ
SEARCH_MSG_ORIGIN = "起点となるモデルです。"
SEARCH_MSG_INTERFACE = "{0} の影響を受けるインタフェースです。"      # {0}には起点モデルの名前を代入します。
SEARCH_MSG_COMPONENT = "{0} の影響を受けるソフトウェアコンポーネントです。"
SEARCH_MSG_CONNECTOR = "{0} と {1} のコネクタです。"                # {0}には検索対象モデルの名前、{1}にはその影響を受けるモデルの名前を代入します。

# ---------------------------------------
# メッセージ（ユーザ通知）
# ダイアログで表示する文字列です。
# ---------------------------------------
DIALOG_MSG_INVALID_SEARCH_TARGET_SELECTION = "起点となるインタフェース、または、ソフトウェアコンポーネントを1つだけエディタで選択してください。"
DIALOG_MSG_NO_IMPACT = "接続している要素はありませんでした。"

# =======================================
# メイン処理関数
# ここで作成した関数をmanifest.jsonのCommandに紐づけます。
# =======================================
def search_impacted_components_and_interfaces(context: "ICommandContext", parameters: "ICommandParams") -> None:
    """選択されたソフトウェアコンポーネントまたはインタフェースを起点に、影響を受けるモデルを探索し検索結果に登録します。
    manifest.json の Command に紐づけるコマンドハンドラです。
    """
    # 1. 調査対象のモデルを取得します。
    selected_models = utils.get_selected_models(context)

    # 選択中のモデルの内、調査対象のクラスに該当するモデルを取得します。
    search_root_model = next(
        (model for model in selected_models if model.AsIn(classNames=SEARCH_TARGET_CLASSES)),
        None
    )

    # 2. 選択中のモデルが1つかつ調査対象のクラスであるかを確認します。
    if len(selected_models) != 1 or search_root_model is None:
        # 条件を満たさない場合、ダイアログを表示して終了します。
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_INVALID_SEARCH_TARGET_SELECTION)
        return

    # 3. 現在のエディタで開かれているダイアグラムからコネクタを取得し、始点・終点モデルで検索できるようにインデックス化します。
    diagram = None
    if context.App.Window.EditorPage and context.App.Window.EditorPage.CurrentEditorView:
        diagram = context.App.Window.EditorPage.CurrentEditorView.Editor
    connector_lookup = _create_connector_lookup(diagram)

    # 4. 既存の検索結果をクリアし、検索を開始します。
    search_manager = context.App.Search
    search = search_manager.Create()
    search_manager.ClearResults()
    search.BeginSearch(SEARCH_NAME, SEARCH_MATCH_TYPE)

    # 5. 起点モデルから影響箇所を探索します。
    visited = set()
    _search_impact(search_root_model, visited, search, connector_lookup)

    # 検索を終了します。
    search.EndSearch()

    # 6. 結果をユーザに通知します。
    all_results = list(search_manager.AllResults)
    if len(all_results) > 1:
        # 起点のモデル以外に影響を受けるモデルがあった場合、検索ウィンドウをアクティブ化します。
        context.App.Window.IsInformationPaneVisible = True
        context.App.Window.ActiveInfoWindow = "SearchResult"
    else:
        # 起点のモデル以外に影響を受けるモデルがなかった場合、検索結果をクリアします。
        search_manager.ClearResults()

        # 影響を受けるモデルがないことをダイアログで通知します。
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_IMPACT)

# =======================================
# サブ処理関数
# =======================================
def _search_impact(
    search_root_model: "IModel",
    visited: Set[str],
    search: "ISearch",
    connector_lookup: Dict[Tuple[str, str], List["IConnector"]]
) -> None:
    """影響箇所探索関数
    起点となるモデルを検索結果に登録し、該当フィールドに設定されているモデルを影響箇所として探索します。
    探索の際、影響箇所の経路となるコネクタも検索結果に登録します。
    モデルを1つずつ辿るため、スタックオーバーフロー対策として再帰の代わりにスタックを使用しています。

    Args:
        search_root_model: 起点となるモデル
        visited: 訪問済みモデルのIDセット
        search: 検索オブジェクト
        connector_lookup: コネクタインデックス
    """
    # 影響箇所を辿るためのスタックを用意し、起点となるモデルを最初に追加します。
    stack = [(search_root_model, None)]

    # スタックが空になるまで、影響箇所を辿ります。
    is_first = True
    while stack:
        # スタックから次の調査対象モデルを取得します。
        impacted_model, search_model = stack.pop()

        # 親モデルとの間のコネクタを検索結果に登録します。
        _search_connectors_between(search_model, impacted_model, connector_lookup, search)

        # 訪問済みである場合は無視します。
        if impacted_model.Id in visited:
            continue

        # 調査対象モデルのクラスに応じて、検索結果のメッセージと次の探索対象を決定します。
        next_target_models = []
        if impacted_model.As(metamodel.CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT):
            # インタフェースの場合。
            message = SEARCH_MSG_INTERFACE.format(search_root_model.Name)
            field_name = SEARCH_FIELD_INTERFACE

            # 次の調査対象モデルを取得します。
            next_target_models.extend(list(impacted_model.GetFieldValues(metamodel.FIELD_NAME_USED_BY_COMPONENTS)))
            next_target_models.extend(list(impacted_model.GetFieldValues(metamodel.FIELD_NAME_DELEGATED_INTERFACES)))
        elif impacted_model.As(metamodel.CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN):
            # ソフトウェアコンポーネントの場合。
            message = SEARCH_MSG_COMPONENT.format(search_root_model.Name)
            field_name = SEARCH_FIELD_COMPONENT

            # 次の調査対象モデルを取得します。
            next_target_models.extend(list(impacted_model.GetFieldValues(metamodel.FIELD_NAME_INTERFACE_FUNCTIONS)))
            next_target_models.extend(list(impacted_model.GetFieldValues(metamodel.FIELD_NAME_INTERFACE_DATA)))
        else:
            # 対象外のクラスの場合は無視します。
            continue

        if is_first:
            # 起点モデルの場合はメッセージを変更します。
            message = SEARCH_MSG_ORIGIN
            field_name = SEARCH_FIELD_ORIGIN
            is_first = False

        # 検索結果に登録します。
        search.AddSearchResult(impacted_model, field_name, message)

        # 訪問済みに追加します。
        visited.add(impacted_model.Id)

        # 次の調査対象モデルをスタックに追加します。重複を排除します。
        seen = set()
        for next_target in next_target_models:
            if next_target.Id not in seen:
                seen.add(next_target.Id)
                stack.append((next_target, impacted_model))

def _search_connectors_between(
    search_model: Optional["IModel"],
    impacted_model: Optional["IModel"],
    connector_lookup: Dict[Tuple[str, str], List["IConnector"]],
    search: "ISearch"
) -> None:
    """モデル間のコネクタ検索関数
    2つのモデル間を結ぶコネクタをインデックスから検索し、見つかった場合は検索結果に登録します。

    Args:
        search_model: モデル1
        impacted_model: モデル2
        connector_lookup: コネクタインデックス
        search: 検索オブジェクト
    """
    if search_model is None or impacted_model is None:
        return

    # コネクタのインデックスから、2つのモデルを結ぶコネクタを検索します。
    key = (search_model.Id, impacted_model.Id)
    connectors = connector_lookup.get(key)
    if connectors:
        # 見つかったコネクタを検索結果に登録します。
        for connector in connectors:
            message = SEARCH_MSG_CONNECTOR.format(search_model.Name, impacted_model.Name)
            search.AddSearchResult(connector.Model, SEARCH_FIELD_CONNECTOR, message)

def _create_connector_lookup(diagram: Optional["IDiagram"]) -> Dict[Tuple[str, str], List["IConnector"]]:
    """コネクタインデックス作成関数
    ダイアグラムからコネクタを取得し、始点・終点モデルの組み合わせをキーとするインデックスを作成します。
    始点・終点の向きは問わず、双方向で登録します。
    ダイアグラムがNoneの場合は空のインデックスを返します。

    Args:
        diagram: ダイアグラム
    Returns:
        コネクタインデックス
    """
    connector_lookup = {}

    if diagram is None:
        # ダイアグラムがNoneの場合は空のインデックスを返します。
        return connector_lookup

    # ダイアグラムにConnectorsプロパティがない場合は空のインデックスを返します。
    connectors = getattr(diagram, 'Connectors', None)
    if connectors is None:
        return connector_lookup

    # ダイアグラム中のコネクタを走査し、始点・終点モデルの組み合わせをキーとするインデックスを作成します。
    for connector in connectors:
        start_id = connector.StartPoint.Model.Id
        end_id = connector.EndPoint.Model.Id

        # 双方向でキーを作成します。
        key1 = (start_id, end_id)
        key2 = (end_id, start_id)

        # 始点・終点の組み合わせをキーとするリストを作成します。
        # 同じ始点・終点を持つコネクタは同じキーのリストに追加します。
        connector_lookup.setdefault(key1, []).append(connector)
        connector_lookup.setdefault(key2, []).append(connector)

    return connector_lookup
