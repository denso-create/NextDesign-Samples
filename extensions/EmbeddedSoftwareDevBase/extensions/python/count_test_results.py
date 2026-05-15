"""機能 : テスト結果を集計

選択中のモデル及びその配下にある全モデルの総合情報に対して、テスト結果を集計しフィールドを更新します。
総合情報を更新した場合、対応する総合情報モデルにエラー（種別：Information）を追加します。

処理概要
    - 対象のモデルが選択されているかを確認します。
    - 対象のテスト結果グループを取得します。
    - 対象のテスト結果グループの配下を下の階層から順に集計し、総合情報を更新します。
"""

# =======================================
# 外部ファイル・モジュール読み込み
# =======================================
from typing import TYPE_CHECKING, List  # 型検査中か否かを表すTYPE_CHECKINGと、型注釈で使う型
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

# テスト結果の集計用の構造体。
class TestResultsCounts:
    def __init__(self) -> None:
        self.planned = 0   # 計画テストケース数
        self.actual = 0    # 実績テストケース数
        self.ok = 0        # OKテストケース数
        self.ng = 0        # NGテストケース数
        self.not_run = 0   # 未実施テストケース数
        self.excluded = 0  # 対象外テストケース数

# ---------------------------------------
# 工程情報の配列
# 各工程の情報をまとめて定義します。
# この配列に要素を追加することで、新しい工程を追加できます。
# ---------------------------------------
COUNT_TARGET_PROCESS_CLASS_NAMES = [
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
DIALOG_MSG_NO_GROUP_OR_SUMMARY_SELECTED = "テスト結果グループ、または、総合情報をエディタで選択してください。"
DIALOG_MSG_NO_UPDATED_SUMMARY = "更新対象となるモデルはありませんでした。"
ERROR_TITLE_UPDATE_TEST_RESULTS_SUMMARY = "テスト結果の集計"
ERROR_MSG_UPDATED_TEST_CASE_COUNTS = "テストケース数を更新しました。"

# =======================================
# メイン処理関数
# ここで作成した関数をmanifest.jsonのCommandに紐づけます。
# =======================================
def count_test_results(context: "ICommandContext", parameters: "ICommandParams") -> None:
    """選択中のモデル及びその配下にある全モデルの総合情報に対して、テスト結果を集計しフィールドを更新します。
    manifest.json の Command に紐づけるコマンドハンドラです。
    """
    # 1. エディタで選択中のモデルのうち、対象クラスに該当するモデルを取得します。
    target_classes = [p.test_results_group_class for p in COUNT_TARGET_PROCESS_CLASS_NAMES] + [metamodel.CLASS_NAME_TEST_RESULTS_SUMMARY]
    selected_models = [model for model in utils.get_selected_models(context) if model.AsIn(classNames=target_classes)]

    # 2. 対象クラスに該当するモデルが選択されているかを確認します。
    if not selected_models:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_GROUP_OR_SUMMARY_SELECTED)
        return

    # 3. 選択中のモデルが属する工程を取得します。
    representative = selected_models[0]
    target_process = next(
        process for process in COUNT_TARGET_PROCESS_CLASS_NAMES
        if representative.FindOwnerByClass(process.process_class) is not None
    )
    process_root = representative.FindOwnerByClass(target_process.process_class)

    # 4. 対象のテスト結果グループを取得します。
    target_groups = _get_target_test_results_groups(process_root, selected_models, target_process.test_results_group_class)

    # 5. 配下の総合情報を更新します。
    context.App.Errors.ClearErrors()
    for target_group in target_groups:
        _count_and_update_summary(target_group, target_process)

    # 6. 結果を出力します。
    errors = list(context.App.Workspace.CurrentProject.GetAllErrorsWithChildren())
    if errors:
        # 変更があった場合、エラーウィンドウを表示します。
        context.App.Window.IsInformationPaneVisible = True
        context.App.Window.ActiveInfoWindow = "Error"
    else:
        # 変更がない場合、ダイアログで通知します。
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_UPDATED_SUMMARY)

# =======================================
# サブ処理関数
# =======================================
def _get_target_test_results_groups(root: "IModel", selected_models: List["IModel"], target_class: str) -> List["IModel"]:
    """対象テスト結果グループ取得関数
    選択されているグループ・総合情報のうち、祖先に選択されたグループを持たないものを取得します。
    探索ルートモデルから再帰的に探索します。

    Args:
        root: 探索ルートモデル
        selected_models: 選択モデル群
        target_class: 対象とするグループのクラス名
    Returns:
        対象結果リスト
    """
    results = []

    if root in selected_models:
        # 選択中の場合は、結果に追加します。
        results.append(root)
        return results

    test_results_summary = next(
        (model for model in root.GetChildren() if model.As(metamodel.CLASS_NAME_TEST_RESULTS_SUMMARY)),
        None
    )
    if test_results_summary is not None and test_results_summary in selected_models:
        # 総合情報が選択中の場合は、テスト結果グループを結果に追加します。
        results.append(root)
        return results

    # 選択中でない場合は、子モデルを再帰的に探索します。
    children_group = [model for model in root.GetChildren() if model.As(target_class)]
    for group in children_group:
        child_results = _get_target_test_results_groups(group, selected_models, target_class)
        results.extend(child_results)

    return results

def _count_and_update_summary(test_result_group: "IModel", target_process: metamodel.TestProcessClassNames) -> TestResultsCounts:
    """テスト結果集計・総合情報更新関数
    対象テスト結果グループ配下にあるすべての総合情報について、テスト結果を集計し更新します。

    Args:
        test_result_group: 対象テスト結果グループ
        target_process: 対象工程のクラス名
    Returns:
        集計結果
    """
    counter = TestResultsCounts()

    # 子グループを先に集計・更新し、結果を加算します。
    children_groups = [model for model in test_result_group.GetChildren() if model.As(target_process.test_results_group_class)]
    for group in children_groups:
        child_counts = _count_and_update_summary(group, target_process)
        counter.planned += child_counts.planned
        counter.actual += child_counts.actual
        counter.ok += child_counts.ok
        counter.ng += child_counts.ng
        counter.not_run += child_counts.not_run
        counter.excluded += child_counts.excluded

    # 直下のテスト結果を集計します。
    children_test_cases = [model for model in test_result_group.GetChildren() if model.As(target_process.test_result_class)]
    for test_case in children_test_cases:
        status = test_case.GetFieldString(metamodel.FIELD_NAME_TEST_RESULTS_STATUS)

        if status != metamodel.FIELD_VALUE_STATUS_EXCLUDED:
            counter.planned += 1
        if status == metamodel.FIELD_VALUE_STATUS_OK or status == metamodel.FIELD_VALUE_STATUS_NG:
            counter.actual += 1
        if status == metamodel.FIELD_VALUE_STATUS_OK:
            counter.ok += 1
        if status == metamodel.FIELD_VALUE_STATUS_NG:
            counter.ng += 1
        if status == metamodel.FIELD_VALUE_STATUS_NOT_RUN:
            counter.not_run += 1
        if status == metamodel.FIELD_VALUE_STATUS_EXCLUDED:
            counter.excluded += 1

    # 総合情報を更新します。
    summary = next(
        (model for model in test_result_group.GetChildren() if model.As(metamodel.CLASS_NAME_TEST_RESULTS_SUMMARY)),
        None
    )
    if summary is not None:
        # フィールドを更新します。
        summary.SetField(metamodel.FIELD_NAME_PLANNED_TEST_CASES, counter.planned)
        summary.SetField(metamodel.FIELD_NAME_ACTUAL_TEST_CASES, counter.actual)
        summary.SetField(metamodel.FIELD_NAME_OK_TEST_CASES, counter.ok)
        summary.SetField(metamodel.FIELD_NAME_NG_TEST_CASES, counter.ng)
        summary.SetField(metamodel.FIELD_NAME_NOT_RUN_TEST_CASES, counter.not_run)
        summary.SetField(metamodel.FIELD_NAME_EXCLUDED_TEST_CASES, counter.excluded)

        # エラー（種別：Information）を追加します。
        summary.AddError(metamodel.FIELD_NAME_NAME, "Information", ERROR_TITLE_UPDATE_TEST_RESULTS_SUMMARY, ERROR_MSG_UPDATED_TEST_CASE_COUNTS)

    return counter
