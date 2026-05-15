"""機能 : ソフトウェア要求モデルを導出

メインエディタで選択されたシステム要求グループ／システム要求と同様の階層構造を持つ
ソフトウェア要求グループ／ソフトウェア要求を、サブエディタで選択されたソフトウェア要求分析
または、ソフトウェア要求グループ配下に一括作成します。
システム要求からソフトウェア要求への導出関連（上位のシステム要求）を設定します。
作成したソフトウェア要求にはIDを自動付与します。

処理概要
    - 選択中のモデルが不正でないかを確認します。
    - 導出元のシステム要求グループ／システム要求を取得します。
    - 導出元を再帰的に走査し、ソフトウェア要求グループ／ソフトウェア要求を作成します。
    - 作成したソフトウェア要求にIDを連番で付与します。
"""

# =======================================
# 外部ファイル・モジュール読み込み
# =======================================
from typing import TYPE_CHECKING, List  # 型検査中か否かを表すTYPE_CHECKINGと、型注釈で使う型
import utils      # 汎用関数
import metamodel  # クラス名などのメタモデル情報
from update_id import PROCESS_ID_CONFIGS, get_max_id, set_sequential_ids  # 作成したモデルにIDを付与するため、ID付与関数を使います。

# エントリポイントであるmain.py以外でndモジュールをインポートすると実行時にエラーになります。
# そのため、TYPE_CHECKINGを用いて型検査時のみインポートします。
if TYPE_CHECKING:
    from nd import *

# =======================================
# ユーザが変更する設定値（パラメータ類）
# この領域を編集して、操作対象やメッセージを変更できます。
# =======================================

# ---------------------------------------
# メッセージ（ユーザ通知）
# ダイアログやエラー追加で表示する文字列です。
# ---------------------------------------
# ダイアログに表示するメッセージ
DIALOG_MSG_DERIVE_SW_REQ_NO_SELECTED_SOURCE = "導出元のシステム要求グループ、または、システム要求をメインエディタで選択してください。"
DIALOG_MSG_DERIVE_SW_REQ_SUB_EDITOR_INVALID = "導出先モデルの追加先となるソフトウェア要求分析、または、ソフトウェア要求グループを1つ、サブエディタで選択してください。"
DIALOG_MSG_DERIVE_SW_REQ_HAS_ERROR = "作成に失敗したモデルがあります。\nエラーウインドウを確認してください。"

# 導出処理の通知
ERROR_TITLE_DERIVE_SW_REQ = "ソフトウェア要求モデルの導出"
ERROR_MSG_DERIVE_SW_REQ_CREATED = "モデルを作成しました。"
ERROR_MSG_DERIVE_SW_REQ_FAILED = "ソフトウェア要求のモデルを作成できませんでした。"
ERROR_MSG_DERIVE_SW_REQ_ID_OVERFLOW = "連番が最大値を超えたため、値を設定できませんでした。"

# =======================================
# メイン処理関数
# ここで作成した関数をmanifest.jsonのCommandに紐づけます。
# =======================================
def derive_software_requirements(context: "ICommandContext", parameters: "ICommandParams") -> None:
    """メインエディタで選択されたシステム要求グループ／システム要求を導出元として、
    サブエディタで選択されたソフトウェア要求分析またはソフトウェア要求グループに同様の構造を作成します。
    manifest.json の Command に紐づけるコマンドハンドラです。
    """
    # 1. メインエディタ・サブエディタで選択中のモデルを取得します。
    # メインエディタで選択中のモデルとシステム要求グループ・システム要求を取得します。
    selected_models_main = utils.get_selected_models_in_main_editor(context)
    selected_system_reqs = [
        model for model in selected_models_main
        if model.AsIn(classNames=[metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, metamodel.CLASS_NAME_SYSTEM_REQUIREMENT])
    ]

    # サブエディタで選択中のモデルを取得します。
    selected_models_sub = utils.get_selected_models_in_sub_editor(context)

    # 2. 正しくモデルが選択されているかを確認します。不正である場合はダイアログを表示して終了します。
    # 2.1. メインエディタでシステム要求グループまたはシステム要求が1つ以上選択されていること。
    if not selected_system_reqs:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_NO_SELECTED_SOURCE)
        return

    # 2.2. サブエディタが表示されていて、1つ選択されていて、ソフトウェア要求分析またはソフトウェア要求グループであること。
    is_valid_sub_editor = (
        context.App.Window.EditorPage.IsSubEditorVisible
        and len(selected_models_sub) == 1
        and selected_models_sub[0].AsIn(classNames=[metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP])
    )

    if not is_valid_sub_editor:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_SUB_EDITOR_INVALID)
        return

    # 3. 導出元・導出先モデルを取得します。
    # 導出元モデルを取得します。システム要求分析をルートとして再帰的に探索します。
    src_models = []
    src_process_root = selected_system_reqs[0].FindOwnerByClass(metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS)
    target_classes = [metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, metamodel.CLASS_NAME_SYSTEM_REQUIREMENT]
    utils.collect_selected_root_models(src_process_root, selected_system_reqs, target_classes, src_models)

    # 導出先のモデルを取得します。
    dst_model = selected_models_sub[0]

    # 4. 既存のソフトウェア要求のIDの最大値を取得します。
    # 導出先のソフトウェア要求分析ルート以下の全ソフトウェア要求を取得します。
    all_software_req_analyses = [
        model for model in context.App.Workspace.CurrentProject.DesignModel.GetChildren()
        if model.As(metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS)
    ]
    all_software_reqs = []
    for analysis in all_software_req_analyses:
        all_software_reqs.extend([
            model for model in analysis.GetAllChildren()
            if model.As(metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT)
        ])

    # ソフトウェア要求のIDプレフィックスを取得します。
    # update_id.pyで定義されたPROCESS_ID_CONFIGSから取得します。
    id_prefix = next(
        c.prefix for c in PROCESS_ID_CONFIGS
        if metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT in c.target_classes
    )

    # 取得した全ソフトウェア要求から、IDの最大値を取得します。
    max_id = get_max_id(all_software_reqs, metamodel.FIELD_NAME_ID, id_prefix)

    # 5. 導出を実施します。
    # 実行前にエラーウインドウの内容をクリアします。
    context.App.Errors.ClearErrors()

    # 作成したソフトウェア要求モデルを収集するリストを用意します。
    created_software_requirements = []

    for src_model in src_models:
        # 導出元モデルの子孫を辿り、同様の構造を導出先モデル配下に作成します。
        if src_model.As(metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP):
            # 導出先モデルのクラスに応じて、導出するフィールドを変えます。
            derivation_field_name = metamodel.FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS
            if dst_model.As(metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS):
                derivation_field_name = metamodel.FIELD_NAME_REQUIREMENTS_GROUP

            # システム要求グループを導出元として、ソフトウェア要求グループを作成します。
            new_model = dst_model.AddNewModel(derivation_field_name, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP)
            new_model.SetField(metamodel.FIELD_NAME_NAME, src_model.Name)

            # サブエディタの選択モデル直下に追加した子モデルにInformation通知を登録します。
            new_model.AddError(metamodel.FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_CREATED)

            # 子孫を再帰的に導出します。
            _derive_child_software_requirements(src_model, new_model, created_software_requirements)
        elif src_model.As(metamodel.CLASS_NAME_SYSTEM_REQUIREMENT):
            if dst_model.As(metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS):
                # 導出元がシステム要求、導出先がソフトウェア要求の場合はモデル作成不可のため、エラーを追加します。
                src_model.AddError(metamodel.FIELD_NAME_NAME, "Error", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_FAILED)
                continue

            # システム要求を導出元として、ソフトウェア要求を作成します。
            new_model = dst_model.AddNewModel(metamodel.FIELD_NAME_SOFTWARE_REQUIREMENTS, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT)
            new_model.SetField(metamodel.FIELD_NAME_NAME, src_model.Name)
            new_model.SetField(metamodel.FIELD_NAME_INPUT_SYSTEM_REQUIREMENT, src_model)

            # 作成したソフトウェア要求をリストに追加します。
            created_software_requirements.append(new_model)

            # サブエディタの選択モデル直下に追加した子モデルにInformation通知を登録します。
            new_model.AddError(metamodel.FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_CREATED)

    # 6. 作成したソフトウェア要求にIDを一括付与します。
    updated_models, error_models = set_sequential_ids(
        created_software_requirements,
        max_id + 1,
        id_prefix
    )

    # エラーモデルに通知を付与します。
    for model in error_models:
        model.AddError(metamodel.FIELD_NAME_ID, "Error", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_ID_OVERFLOW)

    # 7. エラーウインドウを表示します。
    context.App.Window.IsInformationPaneVisible = True
    context.App.Window.ActiveInfoWindow = "Error"

    # 8. エラーがあった場合はダイアログを表示します。
    if list(context.App.Errors.Errors):
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_HAS_ERROR)

# =======================================
# サブ処理関数
# =======================================
def _derive_child_software_requirements(src_group: "IModel", dst_group: "IModel", created_software_requirements: List["IModel"]) -> None:
    """子孫のソフトウェア要求導出関数
    導出元のシステム要求グループと同様の構造を、導出先のソフトウェア要求グループ配下に作成します。

    Args:
        src_group: 導出元システム要求グループ
        dst_group: 導出先ソフトウェア要求グループ
        created_software_requirements: 作成したソフトウェア要求を格納するリスト
    """
    # 導出元グループの子モデルを走査します。
    children = src_group.GetChildren()
    for model in children:
        if model.As(metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP):
            # システム要求グループ → ソフトウェア要求グループを作成します。
            new_model = dst_group.AddNewModel(metamodel.FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP)
            new_model.SetField(metamodel.FIELD_NAME_NAME, model.Name)

            # 追加したモデルを起点に、子孫モデルを導出します。
            _derive_child_software_requirements(model, new_model, created_software_requirements)
        elif model.As(metamodel.CLASS_NAME_SYSTEM_REQUIREMENT):
            # システム要求 → ソフトウェア要求を作成します。
            new_model = dst_group.AddNewModel(metamodel.FIELD_NAME_SOFTWARE_REQUIREMENTS, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT)
            new_model.SetField(metamodel.FIELD_NAME_NAME, model.Name)
            new_model.SetField(metamodel.FIELD_NAME_INPUT_SYSTEM_REQUIREMENT, model)

            # 作成したソフトウェア要求をリストに追加します。
            created_software_requirements.append(new_model)
        else:
            # システム要求グループとシステム要求以外は無視します。
            pass
