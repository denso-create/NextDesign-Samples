"""機能 : テスト結果モデルを導出

メインエディタで選択されたテストケースグループと同様の階層構造を持つテスト結果グループ／テスト結果を、
サブエディタで選択されたテスト結果グループ配下に一括作成します。
テストケースからテスト結果への導出関連を設定します。
作成したテスト結果グループには総合情報モデルを追加します。

処理概要
    - 選択中のモデルが不正でないかを確認します。
    - 導出元のテストケースグループを取得します。
    - 導出元のテストケースグループを再帰的に走査し、テスト結果グループに追加します。
"""

# =======================================
# 外部ファイル・モジュール読み込み
# =======================================
from typing import TYPE_CHECKING  # 型検査中か否かを表すTYPE_CHECKING
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
# 工程情報の配列
# 各工程の情報をまとめて定義します。
# この配列に要素を追加することで、新しい工程を追加できます。
# ---------------------------------------
DERIVE_TARGET_PROCESS_CLASS_NAMES = [
    # ソフトウェアテスト工程
    metamodel.TestProcessClassNames(
        process_class=metamodel.CLASS_NAME_SOFTWARE_TEST,
        test_cases_group_class=metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST,
        test_case_class=metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_TEST,
        test_results_group_class=metamodel.CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_TEST,
        test_result_class=metamodel.CLASS_NAME_TEST_RESULT_SOFTWARE_TEST,
    ),
    # ソフトウェアコンポーネントテスト工程
    metamodel.TestProcessClassNames(
        process_class=metamodel.CLASS_NAME_SOFTWARE_COMPONENT_TEST,
        test_cases_group_class=metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST,
        test_case_class=metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST,
        test_results_group_class=metamodel.CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_COMPONENT_TEST,
        test_result_class=metamodel.CLASS_NAME_TEST_RESULT_SOFTWARE_COMPONENT_TEST,
    ),
    # ソフトウェア統合テスト工程
    metamodel.TestProcessClassNames(
        process_class=metamodel.CLASS_NAME_SOFTWARE_INTEGRATION_TEST,
        test_cases_group_class=metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST,
        test_case_class=metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST,
        test_results_group_class=metamodel.CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_INTEGRATION_TEST,
        test_result_class=metamodel.CLASS_NAME_TEST_RESULT_SOFTWARE_INTEGRATION_TEST,
    )
]

# ---------------------------------------
# メッセージ（ユーザ通知）
# ダイアログやエラー追加で表示する文字列です。
# ---------------------------------------
# ダイアログに表示するメッセージ
DIALOG_MSG_NO_SELECTED_TEST_CASE_GROUP = "導出元のテストケースグループをメインエディタで選択してください。"
DIALOG_MSG_HAS_MULTIPLE_CLASSES = "導出元のテストケースグループはすべて同一の種類を選択してください。"
DIALOG_MSG_SUB_EDITOR_INVALID = "導出先モデルの追加先となるテスト結果グループを1つ、サブエディタで選択してください。"
DIALOG_MSG_DIFFERENT_PROCESSES_SELECTED = "選択されたテストケースグループとテスト結果グループの工程が異なります。"

# 導出処理の通知
ERROR_TITLE_DERIVE_TEST_RESULTS = "テスト結果モデルの導出"
ERROR_MSG_TEST_RESULTS_CREATED = "モデルを作成しました。"

# =======================================
# メイン処理関数
# ここで作成した関数をmanifest.jsonのCommandに紐づけます。
# =======================================
def derive_test_results(context: "ICommandContext", parameters: "ICommandParams") -> None:
    """メインエディタで選択されたテストケースグループを導出元として、サブエディタで選択されたテスト結果グループに同様の構造を作成します。
    manifest.json の Command に紐づけるコマンドハンドラです。
    """
    # 1. メインエディタ・サブエディタで選択中のモデルを取得します。
    # メインエディタで選択中のモデルとテストケースグループを取得します。
    test_cases_group_classes = [p.test_cases_group_class for p in DERIVE_TARGET_PROCESS_CLASS_NAMES]
    selected_models_main = utils.get_selected_models_in_main_editor(context)
    selected_test_cases_groups = [model for model in selected_models_main if model.AsIn(classNames=test_cases_group_classes)]

    # サブエディタで選択中モデルを取得します。
    selected_models_sub = utils.get_selected_models_in_sub_editor(context)

    # 2. 正しくモデルが選択されているかを確認します。不正である場合はダイアログを表示して終了します。
    # 2.1. メインエディタでテストケースグループが1つ以上選択されていること。
    if not selected_test_cases_groups:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_SELECTED_TEST_CASE_GROUP)
        return

    # 2.2. メインエディタで選択されているテストケースグループがすべて同一の種類であること。
    first = selected_test_cases_groups[0] if selected_test_cases_groups else None
    if not all(model.ClassName == first.ClassName for model in selected_test_cases_groups):
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_HAS_MULTIPLE_CLASSES)
        return

    # 2.3. サブエディタが表示されていて、サブエディタで選択中のモデルが1つであること。
    if not context.App.Window.EditorPage.IsSubEditorVisible or len(selected_models_sub) != 1:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_SUB_EDITOR_INVALID)
        return

    # メインエディタで選択中のテストケースグループが属する工程を取得します。
    representative = selected_test_cases_groups[0] if selected_test_cases_groups else None
    target_process = next(
        (process for process in DERIVE_TARGET_PROCESS_CLASS_NAMES if process.test_cases_group_class == representative.ClassName),
        None
    )
    process_root = representative.FindOwnerByClass(target_process.process_class)

    # 2.4. サブエディタで選択されているクラスがメインエディタで選択されているクラスと対応していること。
    if selected_models_sub[0].ClassName != target_process.test_results_group_class:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DIFFERENT_PROCESSES_SELECTED)
        return

    # 3. 導出元と導出先を取得します。
    # 導出元のテストケースグループを取得します。
    src_groups = []
    utils.collect_selected_root_models(process_root, selected_test_cases_groups, [target_process.test_cases_group_class], src_groups)

    # 導出先のテスト結果グループを取得します。
    dst_group = selected_models_sub[0]

    # 4. 導出を実施します。
    # 実行前にエラーウインドウの内容をクリアします。
    context.App.Errors.ClearErrors()

    # 導出元テストケースグループを再帰的に走査し、テスト結果グループ配下に同様の構造を作成します。
    for src_group in src_groups:
        new_model = dst_group.AddNewModel(metamodel.FIELD_NAME_TEST_RESULTS_SUB_GROUPS, target_process.test_results_group_class)
        new_model.SetField(metamodel.FIELD_NAME_NAME, src_group.Name)

        # 導出先モデル直下に追加した子モデルにInformation通知を登録します。
        new_model.AddError(metamodel.FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_TEST_RESULTS, ERROR_MSG_TEST_RESULTS_CREATED)

        _derive_child_test_results(src_group, new_model, target_process)

# =======================================
# サブ処理関数
# =======================================
def _derive_child_test_results(
    test_cases_group: "IModel",
    test_results_group: "IModel",
    target_process: metamodel.TestProcessClassNames
) -> None:
    """子孫のテスト結果導出関数
    導出元のテストケースグループと同様の構造を、導出先のテスト結果グループ配下に作成します。
    ただし、テスト結果グループには総合情報モデルを追加します。

    Args:
        test_cases_group: 導出元テストケースグループ
        test_results_group: 導出先テスト結果グループ
        target_process: 対象工程のクラス名
    """
    # テスト結果グループに総合情報モデルを追加します。
    test_results_group.AddNewModel(metamodel.FIELD_NAME_TEST_RESULTS_SUMMARY, metamodel.CLASS_NAME_TEST_RESULTS_SUMMARY)

    # 導出元テストケースグループの子モデルを走査します。
    children = test_cases_group.GetChildren()
    for model in children:
        if model.As(target_process.test_cases_group_class):
            # テスト結果グループにテストケースグループを追加します。
            new_model = test_results_group.AddNewModel(metamodel.FIELD_NAME_TEST_RESULTS_SUB_GROUPS, target_process.test_results_group_class)
            new_model.SetField(metamodel.FIELD_NAME_NAME, model.Name)

            # 追加したモデルを起点に、子孫モデルを導出します。
            _derive_child_test_results(model, new_model, target_process)
        elif model.As(target_process.test_case_class):
            # テスト結果グループにテスト結果を追加します。
            new_model = test_results_group.AddNewModel(metamodel.FIELD_NAME_TEST_RESULTS, target_process.test_result_class)
            new_model.SetField(metamodel.FIELD_NAME_NAME, model.Name)
            new_model.SetField(metamodel.FIELD_NAME_TEST_CASES, model)
        else:
            # テストケースグループとテストケース以外は無視します。
            pass
