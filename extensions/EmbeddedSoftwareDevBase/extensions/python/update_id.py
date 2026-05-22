"""機能 : IDを更新

選択中のモデルとその子孫のモデルのIDを一意になるように一括で振りなおします。
IDは工程毎に一意になるように割り振ります。

処理概要
    - 更新対象となるモデルを取得します。
    - 更新対象でないモデルから、既存のIDの最大値を求めます。
    - 求めたIDの最大値+1からはじめ、順にIDを割り振ります。
    - 結果をダイアログとエラー追加で通知します。
"""

# =======================================
# 外部ファイル・モジュール読み込み
# =======================================
from typing import TYPE_CHECKING, List, Tuple  # 型検査中か否かを表すTYPE_CHECKINGと、型注釈で使う型
import re        # 正規表現を使用するためのモジュール
import utils      # 汎用関数
import metamodel  # クラス名などのメタモデル情報

# エントリポイントであるmain.py以外でndモジュールをインポートすると実行時にエラーになります。
# そのため、TYPE_CHECKINGを用いて型検査時のみインポートします。
if TYPE_CHECKING:
    from nd import *

# =======================================
# ユーザが変更する設定値（パラメータ類）
# この領域を編集して、操作対象やメッセージを変更できます。
# =======================================

# ---------------------------------------
# データ構造定義
# ---------------------------------------

# 工程ごとにIDの更新に必要な情報をまとめて管理する構造体
class ProcessIdConfig:
    def __init__(self, root_classes: List[str], start_classes: List[str], target_classes: List[str], prefix: str) -> None:
        self.root_classes = root_classes      # 工程のルートとなるクラス名の配列（工程ごとの全モデル取得に使用）
        self.start_classes = start_classes    # 起点となるクラス名の配列（工程ごとの選択モデルの判定に使用）
        self.target_classes = target_classes  # 更新対象となるクラス名の配列（ID更新対象の判定に使用）
        self.prefix = prefix                  # IDのプレフィックス（例："SYRQ-"）

# ---------------------------------------
# 工程情報の配列
# 各工程の情報をまとめて定義します。
# この配列に要素を追加することで、新しい工程を処理対象に追加できます。
# ---------------------------------------
PROCESS_ID_CONFIGS = [
    # システム要求分析工程
    ProcessIdConfig(
        root_classes=[metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS],
        start_classes=[metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS, metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, metamodel.CLASS_NAME_SYSTEM_REQUIREMENT],
        target_classes=[metamodel.CLASS_NAME_SYSTEM_REQUIREMENT],
        prefix="SYRQ-"
    ),
    # ソフトウェア要求分析工程
    ProcessIdConfig(
        root_classes=[metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS],
        start_classes=[metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT],
        target_classes=[metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT],
        prefix="SWRQ-"
    ),
    # ソフトウェアコンポーネントテスト工程
    ProcessIdConfig(
        root_classes=[metamodel.CLASS_NAME_SOFTWARE_COMPONENT_TEST],
        start_classes=[metamodel.CLASS_NAME_SOFTWARE_COMPONENT_TEST, metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST, metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST],
        target_classes=[metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST],
        prefix="SWCT-"
    ),
    # ソフトウェア統合テスト工程
    ProcessIdConfig(
        root_classes=[metamodel.CLASS_NAME_SOFTWARE_INTEGRATION_TEST],
        start_classes=[metamodel.CLASS_NAME_SOFTWARE_INTEGRATION_TEST, metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST, metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST],
        target_classes=[metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST],
        prefix="SWIT-"
    ),
    # ソフトウェアテスト工程
    ProcessIdConfig(
        root_classes=[metamodel.CLASS_NAME_SOFTWARE_TEST],
        start_classes=[metamodel.CLASS_NAME_SOFTWARE_TEST, metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST, metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_TEST],
        target_classes=[metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_TEST],
        prefix="SWTT-"
    )
]

# ---------------------------------------
# IDに関する定義
# ---------------------------------------
UPDATE_ID_DIGITS = 6  # IDの桁数

# ---------------------------------------
# メッセージ（ユーザ通知）
# ダイアログやエラー追加で表示する文字列です。
# ---------------------------------------
DIALOG_MSG_NO_UPDATE_TARGET_SELECTED = "IDがあるモデル、または、IDがあるモデルの祖先モデルをエディタで選択してください。"
DIALOG_MSG_HAS_FAILED_ID = "IDの更新に失敗したモデルがあります。\nエラーウインドウを確認してください。"
DIALOG_NO_ID_UPDATED = "更新対象となるモデルはありませんでした。"
ERROR_TITLE_UPDATE_ID = "IDの更新"
ERROR_MSG_SUCCESS_UPDATE_ID = "{0} を設定しました。"
ERROR_MSG_FAILED_UPDATE_ID = "連番が最大値を超えたため、値をクリアしました。"

# =======================================
# メイン処理関数
# ここで作成した関数をmanifest.jsonのCommandに紐づけます。
# =======================================
def update_id(context: "ICommandContext", parameters: "ICommandParams") -> None:
    """選択モデルとその子孫のIDを一括で振りなおします。
    manifest.json の Command に紐づけるコマンドハンドラです。
    """
    # 1. 選択モデルを取得し、工程ごとの選択モデルの配列を作成します。
    # エディタで選択中のモデルを取得します。
    selected_models = utils.get_selected_models(context)

    # 工程ごとに「起点クラス(start_classes)に該当する選択モデル」だけを抽出して配列にまとめます。
    # 例：ソフトウェア要求のモデルが1つだけ選択されている場合、
    #    selected_models_by_process = [[], [ソフトウェア要求のモデル], []]
    selected_models_by_process = [
        [model for model in selected_models if model.AsIn(classNames=process.start_classes)]
        for process in PROCESS_ID_CONFIGS
    ]

    # 2. 起点となるクラスに該当するモデルが1つでも選択されているかを確認します。
    if not any(models for models in selected_models_by_process):
        # 選択されていない場合、ダイアログを表示して終了します。
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_UPDATE_TARGET_SELECTED)
        return

    # 3. 各工程のIDを更新します。
    # 既存のエラーを全てクリアします。
    context.App.Errors.ClearErrors()

    # プロジェクト直下のモデルを取得します。
    root_children = list(context.App.Workspace.CurrentProject.DesignModel.GetChildren())

    # 4. 各工程のID更新処理を実行します。
    for config, selected in zip(PROCESS_ID_CONFIGS, selected_models_by_process):
        # 工程ごとのプロジェクト直下のモデルを取得します。
        process_root_models = [model for model in root_children if model.AsIn(classNames=config.root_classes)]

        # ID更新処理を実行します。
        _update_ids_for_process(
            config,
            selected,
            process_root_models
        )

    # 5. 処理結果を通知します。
    _show_result_notification(context.App.Errors, context.App.Window)

# =======================================
# サブ処理関数
# =======================================
def _update_ids_for_process(process_info: ProcessIdConfig, selected_models: List["IModel"], root_models: List["IModel"]) -> None:
    """1工程のID更新関数
    工程内の選択モデルとその子孫のモデルを対象にIDを更新します。
    対象でないモデルから既存IDの最大値を取得し、最大値+1からはじめモデルナビゲータで上から順になるようにIDを付与します。
    IDに設定できる最大値を超える場合はエラーとし、空文字を設定します。

    Args:
        process_info: 工程情報
        selected_models: 選択モデル
        root_models: 対象工程のルートのモデル
    """
    # 1. 工程内の更新対象クラスに該当するモデルを全て取得します。
    all_target_class_models = []
    for model in root_models:
        for child in model.GetAllChildren():
            if child.AsIn(classNames=process_info.target_classes):
                all_target_class_models.append(child)

    # 2. 更新対象のモデルを取得します。
    target_models, other_models = _split_models_into_target_and_others(all_target_class_models, selected_models, process_info.target_classes)

    # 3. 更新対象外のモデルからIDの最大値を取得します。
    max_id = get_max_id(other_models, metamodel.FIELD_NAME_ID, process_info.prefix)

    # 4. IDを更新します。
    updated_models, error_models = set_sequential_ids(
        target_models,
        max_id + 1,
        process_info.prefix
    )

    # 5. 通知を付与します。
    for model in updated_models:
        # 成功したモデルには、エラー（種別=information）を追加します。
        new_id = model.GetFieldString(metamodel.FIELD_NAME_ID)
        model.AddError(metamodel.FIELD_NAME_ID, "Information", ERROR_TITLE_UPDATE_ID, ERROR_MSG_SUCCESS_UPDATE_ID.format(new_id))
    for model in error_models:
        # エラーとなったモデルには、エラー（種別=error）を追加します。
        model.AddError(metamodel.FIELD_NAME_ID, "Error", ERROR_TITLE_UPDATE_ID, ERROR_MSG_FAILED_UPDATE_ID)

def _split_models_into_target_and_others(models: List["IModel"], selected_models: List["IModel"], target_class_names: List[str]) -> Tuple[List["IModel"], List["IModel"]]:
    """更新対象・更新対象外モデル振り分け関数
    以下の2つに振り分けます。
    - 更新対象モデル：選択中モデルとその子孫モデルの内、指定された工程の対象クラスに該当するもの。
    - 更新対象外モデル：指定された工程の対象クラスに該当する全モデルの内、上記以外のもの。

    Args:
        models: すべてのモデル
        selected_models: 選択モデル
        target_class_names: 対象クラス名配列
    Returns:
        更新対象モデル、更新対象外モデル
    """
    # 選択中モデルとその子孫モデルの内、対象クラスに該当するものを取得します。
    selected_with_children_ids = set()
    for model in selected_models:
        for child in [model] + list(model.GetAllChildren()):
            if child.AsIn(classNames=target_class_names):
                selected_with_children_ids.add(child.Id)

    # 更新対象モデルと更新対象外モデルに分離します。
    target_models = []
    other_models = []
    for model in models:
        if model.Id in selected_with_children_ids:
            target_models.append(model)
        else:
            other_models.append(model)

    return target_models, other_models

def get_max_id(models: List["IModel"], field_name: str, prefix: str) -> int:
    """ID最大値算出関数
    受け取ったモデルの中からIDの最大値を取得します。

    Args:
        models: モデル
        field_name: IDのフィールド名
        prefix: IDのプレフィックス
    Returns:
        IDの最大値
    """
    models_list = list(models)
    if not models_list:
        # 受け取ったモデルが空の場合、0を返します。
        return 0

    # 命名規則に合致するIDの最大値を取得します。
    # プレフィックスと桁数から正規表現を生成します。
    regex_pattern = f"^{re.escape(prefix)}(?P<num>[0-9]{{{UPDATE_ID_DIGITS}}})$"
    regex = re.compile(regex_pattern)

    max_id = 0
    for model in models_list:
        id_str = model.GetFieldString(field_name)

        # 正規表現で命名規則に合致するかを確認します。
        match = regex.match(id_str)
        if not match:
            # 命名規則に則っていない場合は無視します。
            continue

        # ID文字列から数字部分を抽出して整数に変換します。
        # 例："SYRQ-000123" の場合、 "000123" を取得して 123 に変換します。
        num = int(match.group("num"))
        if num > max_id:
            max_id = num

    return max_id

def set_sequential_ids(target_models: List["IModel"], start_id_number: int, prefix: str) -> Tuple[List["IModel"], List["IModel"]]:
    """連番ID設定関数
    指定された値を初期値として、全モデルのIDに連番のIDを付与します。
    IDが最大値を超えた場合は、モデルのIDに空文字列を設定します。

    Args:
        target_models: 更新対象のモデル
        start_id_number: IDの開始値
        prefix: IDのプレフィックス
    Returns:
        成功したモデル、最大値を超えて失敗したモデル
    """
    updated_models = []
    error_models = []
    next_id_number = start_id_number

    max_id_number = 10 ** UPDATE_ID_DIGITS

    # 各モデルに対してIDを設定します。
    for model in target_models:
        if next_id_number >= max_id_number:
            # IDの最大値を超える場合は空文字を設定します。
            model.SetField(metamodel.FIELD_NAME_ID, "")
            error_models.append(model)
            continue

        # 新しいIDを生成します。
        new_id = f"{prefix}{next_id_number:0{UPDATE_ID_DIGITS}d}"
        current_id = model.GetFieldString(metamodel.FIELD_NAME_ID)

        if current_id != new_id:
            # もとのIDと異なる場合、IDを設定します。
            model.SetField(metamodel.FIELD_NAME_ID, new_id)
            updated_models.append(model)

        next_id_number += 1

    return updated_models, error_models

def _show_result_notification(errors: "IErrors", window: "IWorkspaceWindow") -> None:
    """結果通知関数
    処理結果に応じた通知を行います。
    エラーウインドウを表示し、処理結果に応じたダイアログ通知を行います。

    Args:
        errors: エラー情報
        window: UI操作のためのウインドウオブジェクト
    """
    # エラーの有無を取得します。
    has_error = bool(list(errors.Errors))
    has_changed = bool(list(errors.Informations))

    # エラーウインドウを表示します。
    if has_error or has_changed:
        window.IsInformationPaneVisible = True
        window.ActiveInfoWindow = "Error"

    # 処理結果に応じたユーザ通知を行います。
    if has_error:
        window.UI.ShowInformationDialog(DIALOG_MSG_HAS_FAILED_ID)
    elif not has_changed:
        window.UI.ShowInformationDialog(DIALOG_NO_ID_UPDATED)
