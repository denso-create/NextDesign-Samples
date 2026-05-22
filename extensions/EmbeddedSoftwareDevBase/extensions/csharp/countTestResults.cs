// =======================================
// 機能 : テスト結果を集計
// =======================================
// 
// 選択中のモデル及びその配下にある全モデルの総合情報に対して、テスト結果を集計しフィールドを更新します。
// 総合情報を更新した場合、対応する総合情報モデルにエラー（種別：Information）を追加します。
// 
// 処理概要
//   - 対象のモデルが選択されているかを確認します。
//   - 対象のテスト結果グループを取得します。
//   - 対象のテスト結果グループの配下を下の階層から順に集計し、総合情報を更新します。
//
// 補足
//   処理の実装にLINQ(Add, AddRange, Append, Contains, FirstOrDefault, Select, ToList, Where)を使用しています。
//   LINQについては以下を参照してください。
//   LINQの概要：https://learn.microsoft.com/ja-jp/dotnet/csharp/linq
//   APIリファレンス：https://learn.microsoft.com/ja-jp/dotnet/api/system.linq.enumerable


// =======================================
// 外部ファイル・名前空間読み込み
// =======================================
#load "utils.cs"     // 汎用関数
#load "metamodel.cs" // クラス名などのメタモデル情報

// =======================================
// ユーザが変更する設定値（パラメータ類）
// この領域を編集して、操作対象やメッセージを変更できます。
// =======================================

// ---------------------------------------
// 工程情報の配列
// 各工程の情報をまとめて定義します。
// この配列に要素を追加することで、新しい工程を追加できます。
// ---------------------------------------
TestProcessClassNames[] COUNT_TARGET_PROCESS_CLASS_NAMES = new TestProcessClassNames[]
{ 
    // ソフトウェアテスト工程
    new TestProcessClassNames
    {
        ProcessClass            = CLASS_NAME_SOFTWARE_TEST,
        TestCasesGroupClass     = CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST,
        TestCaseClass           = CLASS_NAME_TEST_CASE_SOFTWARE_TEST,
        TestResultsGroupClass   = CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_TEST,
        TestResultClass         = CLASS_NAME_TEST_RESULT_SOFTWARE_TEST,
    },
    // ソフトウェアコンポーネントテスト工程
    new TestProcessClassNames
    {
        ProcessClass            = CLASS_NAME_SOFTWARE_COMPONENT_TEST,
        TestCasesGroupClass     = CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST,
        TestCaseClass           = CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST,
        TestResultsGroupClass   = CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_COMPONENT_TEST,
        TestResultClass         = CLASS_NAME_TEST_RESULT_SOFTWARE_COMPONENT_TEST,
    },
    // ソフトウェア統合テスト工程
    new TestProcessClassNames
    {
        ProcessClass            = CLASS_NAME_SOFTWARE_INTEGRATION_TEST,
        TestCasesGroupClass     = CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST,
        TestCaseClass           = CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST,
        TestResultsGroupClass   = CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_INTEGRATION_TEST,
        TestResultClass         = CLASS_NAME_TEST_RESULT_SOFTWARE_INTEGRATION_TEST,
    }
};

// ---------------------------------------
// メッセージ（ユーザ通知）
// ダイアログやエラー追加で表示する文字列です。
// ---------------------------------------
string DIALOG_MSG_NO_GROUP_OR_SUMMARY_SELECTED = "テスト結果グループ、または、総合情報をエディタで選択してください。";
string DIALOG_MSG_NO_UPDATED_SUMMARY = "更新対象となるモデルはありませんでした。";
string ERROR_TITLE_UPDATE_TEST_RESULTS_SUMMARY = "テスト結果の集計";
string ERROR_MSG_UPDATED_TEST_CASE_COUNTS = "テストケース数を更新しました。";

// =======================================
// メイン処理関数
// ここで作成した関数をmanifest.jsonのCommandに紐づけます。
// =======================================
public void CountTestResults(ICommandContext context, ICommandParams parameters)
{
    // 1. エディタで選択中のモデルのうち、対象クラスに該当するモデルを取得します。
    var targetClasses = COUNT_TARGET_PROCESS_CLASS_NAMES
        .Select(p => p.TestResultsGroupClass)
        .Append(CLASS_NAME_TEST_RESULTS_SUMMARY);
    var selectedModels = GetSelectedModels(context).Where(model => model.AsIn(targetClasses)).ToList();

    // 2. 対象クラスに該当するモデルが選択されているかを確認します。
    if (!selectedModels.Any())
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_GROUP_OR_SUMMARY_SELECTED);
        return;
    }

    // 3. 選択中のモデルが属する工程を取得します。
    var representative = selectedModels.First();
    var targetProcess = COUNT_TARGET_PROCESS_CLASS_NAMES.First(process => representative.FindOwnerByClass(process.ProcessClass) != null);
    var processRoot = representative.FindOwnerByClass(targetProcess.ProcessClass);

    // 4. 対象のテスト結果グループを取得します。
    var targetGroups = GetTargetTestResultsGroups(processRoot, selectedModels, targetProcess.TestResultsGroupClass);

    // 5. 配下の総合情報を更新します。
    context.App.Errors.ClearErrors();
    foreach (var targetGroup in targetGroups)
    {
        CountAndUpdateSummary(targetGroup, targetProcess);
    }

    // 6. 結果を出力します。
    var errors = context.App.Workspace.CurrentProject.GetAllErrorsWithChildren();
    if (errors.Any())
    {
        // 変更があった場合、エラーウィンドウを表示します。
        context.App.Window.IsInformationPaneVisible = true;
        context.App.Window.ActiveInfoWindow = "Error";
    }
    else
    {
        // 変更がない場合、ダイアログで通知します。
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_UPDATED_SUMMARY);
    }
}

// ---------------------------------------
// 対象テスト結果グループ取得関数
// 選択されているグループ・総合情報のうち、祖先に選択されたグループを持たないものを取得します。
// 探索ルートモデルから再帰的に探索します。
// 引数:探索ルートモデル、選択モデル群、対象とするグループのクラス名
// 戻り値:対象結果リスト
// ---------------------------------------
private List<IModel> GetTargetTestResultsGroups(IModel root, IEnumerable<IModel> selectedModels, string targetClass)
{
    var results = new List<IModel>();

    var selectedModelsList = selectedModels.ToList();
    if (selectedModelsList.Contains(root))
    {
        // 選択中の場合は、結果に追加します。
        results.Add(root);
        return results;
    }

    var testResultsSummary = root.GetChildren().FirstOrDefault(model => model.As(CLASS_NAME_TEST_RESULTS_SUMMARY));
    if (testResultsSummary != null && selectedModelsList.Contains(testResultsSummary))
    {
        // 総合情報が選択中の場合は、テスト結果グループを結果に追加します。
        results.Add(root);
        return results;
    }

    // 選択中でない場合は、子モデルを再帰的に探索します。
    var childrenGroup = root.GetChildren().Where(model => model.As(targetClass));
    foreach (var group in childrenGroup)
    {
        var childResults = GetTargetTestResultsGroups(group, selectedModelsList, targetClass);
        results.AddRange(childResults);
    }
    return results;
}

// ---------------------------------------
// テスト結果集計・総合情報更新関数
// 対象テスト結果グループ配下にあるすべての総合情報について、テスト結果を集計し更新します。
// 引数:対象テスト結果グループ、対象工程のクラス名
// 戻り値:対象結果リスト
// ---------------------------------------
private TestResultsCounts CountAndUpdateSummary(IModel testResultGroup, TestProcessClassNames targetProcess)
{
    var counter = new TestResultsCounts();

    // 子グループを先に集計・更新し、結果を加算します。
    var childrenGroups = testResultGroup.GetChildren().Where(model => model.As(targetProcess.TestResultsGroupClass));
    foreach (var group in childrenGroups)
    {
        var childCounts = CountAndUpdateSummary(group, targetProcess);
        counter.Planned += childCounts.Planned;
        counter.Actual += childCounts.Actual;
        counter.Ok += childCounts.Ok;
        counter.Ng += childCounts.Ng;
        counter.NotRun += childCounts.NotRun;
        counter.Excluded += childCounts.Excluded;
    }

    // 直下のテスト結果を集計します。
    var childrenTestCases = testResultGroup.GetChildren().Where(model => model.As(targetProcess.TestResultClass));
    foreach (var testCase in childrenTestCases)
    {
        var status = testCase.GetFieldString(FIELD_NAME_TEST_RESULTS_STATUS);

        if (status != FIELD_VALUE_STATUS_EXCLUDED) counter.Planned++;
        if (status == FIELD_VALUE_STATUS_OK || status == FIELD_VALUE_STATUS_NG) counter.Actual++;
        if (status == FIELD_VALUE_STATUS_OK) counter.Ok++;
        if (status == FIELD_VALUE_STATUS_NG) counter.Ng++;
        if (status == FIELD_VALUE_STATUS_NOT_RUN) counter.NotRun++;
        if (status == FIELD_VALUE_STATUS_EXCLUDED) counter.Excluded++;
    }

    // 総合情報を更新します。
    var summary = testResultGroup.GetChildren().FirstOrDefault(model => model.As(CLASS_NAME_TEST_RESULTS_SUMMARY));
    if (summary != null)
    {
        // フィールドを更新します。
        summary.SetField(FIELD_NAME_PLANNED_TEST_CASES, counter.Planned);
        summary.SetField(FIELD_NAME_ACTUAL_TEST_CASES, counter.Actual);
        summary.SetField(FIELD_NAME_OK_TEST_CASES, counter.Ok);
        summary.SetField(FIELD_NAME_NG_TEST_CASES, counter.Ng);
        summary.SetField(FIELD_NAME_NOT_RUN_TEST_CASES, counter.NotRun);
        summary.SetField(FIELD_NAME_EXCLUDED_TEST_CASES, counter.Excluded);

        // エラー（種別：Information）を追加します。
        summary.AddError
        (
            fields: FIELD_NAME_NAME,
            type: "Information",
            title: ERROR_TITLE_UPDATE_TEST_RESULTS_SUMMARY,
            message: ERROR_MSG_UPDATED_TEST_CASE_COUNTS
        );
    }

    return counter;
}

// =======================================
// データ構造定義
// =======================================

// テスト結果の集計用の構造体。
private struct TestResultsCounts
{
    public int Planned;  // 計画テストケース数
    public int Actual;   // 実績テストケース数
    public int Ok;       // OKテストケース数
    public int Ng;       // NGテストケース数
    public int NotRun;   // 未実施テストケース数
    public int Excluded; // 対象外テストケース数
};