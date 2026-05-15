// =======================================
// 機能 : テスト結果モデルを導出
// =======================================
//
// メインエディタで選択されたテストケースグループと同様の階層構造を持つテスト結果グループ／テスト結果を、
// サブエディタで選択されたテスト結果グループ配下に一括作成します。
// テストケースからテスト結果への導出関連を設定します。
// 作成したテスト結果グループには総合情報モデルを追加します。
// 
// 処理概要
//   - 選択中のモデルが不正でないかを確認します。
//   - 導出元のテストケースグループを取得します。
//   - 導出元のテストケースグループを再帰的に走査し、テスト結果グループに追加します。
//
// 補足
//   処理の実装にLINQ(Any, Where, Select, First, FirstOrDefault, ToList)を使用しています。
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
TestProcessClassNames[] DERIVE_TARGET_PROCESS_CLASS_NAMES = new TestProcessClassNames[]
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
// ダイアログに表示するメッセージ
string DIALOG_MSG_NO_SELECTED_TEST_CASE_GROUP = "導出元のテストケースグループをメインエディタで選択してください。";
string DIALOG_MSG_HAS_MULTIPLE_CLASSES = "導出元のテストケースグループはすべて同一の種類を選択してください。";
string DIALOG_MSG_SUB_EDITOR_INVALID = "導出先モデルの追加先となるテスト結果グループを1つ、サブエディタで選択してください。";
string DIALOG_MSG_DIFFERENT_PROCESSES_SELECTED = "選択されたテストケースグループとテスト結果グループの工程が異なります。";

// 導出処理の通知
string ERROR_TITLE_DERIVE_TEST_RESULTS = "テスト結果モデルの導出";
string ERROR_MSG_TEST_RESULTS_CREATED = "モデルを作成しました。";

// =======================================
// メイン処理関数
// ここで作成した関数をmanifest.jsonのCommandに紐づけます。
// =======================================
public void DeriveTestResults(ICommandContext context, ICommandParams parameters)
{
    // 1. メインエディタ・サブエディタで選択中のモデルを取得します。
    // メインエディタで選択中のモデルとテストケースグループを取得します。
    var testCasesGroupClasses = DERIVE_TARGET_PROCESS_CLASS_NAMES.Select(p => p.TestCasesGroupClass);
    var selectedModelsMain = GetSelectedModelsInMainEditor(context).ToList();
    var selectedTestCasesGroups = selectedModelsMain.Where(model => model.AsIn(testCasesGroupClasses)).ToList();

    // サブエディタで選択中モデルを取得します。
    var selectedModelsSub = GetSelectedModelsInSubEditor(context).ToList();

    // 2. 正しくモデルが選択されているかを確認します。不正である場合はダイアログを表示して終了します。
    // 2.1. メインエディタでテストケースグループが1つ以上選択されていること。
    if (!selectedTestCasesGroups.Any())
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_SELECTED_TEST_CASE_GROUP);
        return;
    }

    // 2.2. メインエディタで選択されているテストケースグループがすべて同一の種類であること。
    var first = selectedTestCasesGroups.FirstOrDefault();
    if (!selectedTestCasesGroups.All(model => string.Equals(model.ClassName, first?.ClassName)))
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_HAS_MULTIPLE_CLASSES);
        return;
    }

    // 2.3. サブエディタが表示されていて、サブエディタで選択中のモデルが1つであること。
    if (!context.App.Window.EditorPage.IsSubEditorVisible || selectedModelsSub.Count != 1)
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_SUB_EDITOR_INVALID);
        return;
    }

    // メインエディタで選択中のテストケースグループが属する工程を取得します。
    var representative = selectedTestCasesGroups.FirstOrDefault();
    var targetProcess = DERIVE_TARGET_PROCESS_CLASS_NAMES.FirstOrDefault(process => process.TestCasesGroupClass == representative?.ClassName);
    var processRoot = representative?.FindOwnerByClass(targetProcess.ProcessClass);

    // 2.4. サブエディタで選択されているクラスがメインエディタで選択されているクラスと対応していること。
    if (selectedModelsSub.First().ClassName != targetProcess.TestResultsGroupClass)
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DIFFERENT_PROCESSES_SELECTED);
        return;
    }

    // 3. 導出元と導出先を取得します。
    // 導出元のテストケースグループを取得します。
    var srcGroups = new List<IModel>();
    CollectSelectedRootModels(processRoot, selectedTestCasesGroups, new[] { targetProcess.TestCasesGroupClass }, srcGroups);

    // 導出先のテスト結果グループを取得します。
    var dstGroup = selectedModelsSub.First();

    // 4. 導出を実施します。
    // 実行前にエラーウインドウの内容をクリアします。
    context.App.Errors.ClearErrors();

    // 導出元テストケースグループを再帰的に走査し、テスト結果グループ配下に同様の構造を作成します。
    foreach (var srcGroup in srcGroups)
    {
        var newModel = dstGroup.AddNewModel(FIELD_NAME_TEST_RESULTS_SUB_GROUPS, targetProcess.TestResultsGroupClass);
        newModel.SetField(FIELD_NAME_NAME, srcGroup.Name);

        // 導出先モデル直下に追加した子モデルにInformation通知を登録します。
        newModel.AddError(FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_TEST_RESULTS, ERROR_MSG_TEST_RESULTS_CREATED);

        DeriveChildTestResults(srcGroup, newModel, targetProcess);
    }
}

// =======================================
// サブ処理関数
// =======================================

// ---------------------------------------
// 子孫のテスト結果導出関数
// 導出元のテストケースグループと同様の構造を、導出先のテスト結果グループ配下に作成します。  
// ただし、テスト結果グループには総合情報モデルを追加します。
// 引数:導出元テストケースグループ、導出先テスト結果グループ、対象工程のクラス名
// ---------------------------------------
private void DeriveChildTestResults(IModel testCasesGroup, IModel testResultsGroup, TestProcessClassNames targetProcess)
{
    // テスト結果グループに総合情報モデルを追加します。
    testResultsGroup.AddNewModel(FIELD_NAME_TEST_RESULTS_SUMMARY, CLASS_NAME_TEST_RESULTS_SUMMARY);

    // 導出元テストケースグループの子モデルを走査します。
    var children = testCasesGroup.GetChildren();
    foreach (var model in children)
    {
        if (model.As(targetProcess.TestCasesGroupClass))
        {
            // テスト結果グループにテストケースグループを追加します。
            var newModel = testResultsGroup.AddNewModel(FIELD_NAME_TEST_RESULTS_SUB_GROUPS, targetProcess.TestResultsGroupClass);
            newModel.SetField(FIELD_NAME_NAME, model.Name);

            // 追加したモデルを起点に、子孫モデルを導出します。
            DeriveChildTestResults(model, newModel, targetProcess);
        }
        else if (model.As(targetProcess.TestCaseClass))
        {
            // テスト結果グループにテスト結果を追加します。
            var newModel = testResultsGroup.AddNewModel(FIELD_NAME_TEST_RESULTS, targetProcess.TestResultClass);
            newModel.SetField(FIELD_NAME_NAME, model.Name);
            newModel.SetField(FIELD_NAME_TEST_CASES, model);
        }
        else
        {
            // テストケースグループとテストケース以外は無視します。
        }
    }
}