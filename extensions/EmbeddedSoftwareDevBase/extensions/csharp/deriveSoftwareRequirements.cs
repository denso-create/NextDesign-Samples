// =======================================
// 機能 : ソフトウェア要求モデルを導出
// =======================================
//
// メインエディタで選択されたシステム要求グループ／システム要求と同様の階層構造を持つ
// ソフトウェア要求グループ／ソフトウェア要求を、サブエディタで選択されたソフトウェア要求分析
// または、ソフトウェア要求グループ配下に一括作成します。
// システム要求からソフトウェア要求への導出関連（上位のシステム要求）を設定します。
// 作成したソフトウェア要求にはIDを自動付与します。
//
// 処理概要
//   - 選択中のモデルが不正でないかを確認します。
//   - 導出元のシステム要求グループ／システム要求を取得します。
//   - 導出元を再帰的に走査し、ソフトウェア要求グループ／ソフトウェア要求を作成します。
//   - 作成したソフトウェア要求にIDを連番で付与します。
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
#load "updateId.cs"  // 作成したモデルにIDを付与するため、ID付与関数を使います。

// =======================================
// ユーザが変更する設定値（パラメータ類）
// この領域を編集して、操作対象やメッセージを変更できます。
// =======================================

// ---------------------------------------
// メッセージ（ユーザ通知）
// ダイアログやエラー追加で表示する文字列です。
// ---------------------------------------
// ダイアログに表示するメッセージ
string DIALOG_MSG_DERIVE_SW_REQ_NO_SELECTED_SOURCE = "導出元のシステム要求グループ、または、システム要求をメインエディタで選択してください。";
string DIALOG_MSG_DERIVE_SW_REQ_SUB_EDITOR_INVALID = "導出先モデルの追加先となるソフトウェア要求分析、または、ソフトウェア要求グループを1つ、サブエディタで選択してください。";
string DIALOG_MSG_DERIVE_SW_REQ_HAS_ERROR = "作成に失敗したモデルがあります。\nエラーウインドウを確認してください。";

// 導出処理の通知
string ERROR_TITLE_DERIVE_SW_REQ = "ソフトウェア要求モデルの導出";
string ERROR_MSG_DERIVE_SW_REQ_CREATED = "モデルを作成しました。";
string ERROR_MSG_DERIVE_SW_REQ_FAILED = "ソフトウェア要求のモデルを作成できませんでした。";
string ERROR_MSG_DERIVE_SW_REQ_ID_OVERFLOW = "連番が最大値を超えたため、値を設定できませんでした。";

// =======================================
// メイン処理関数
// ここで作成した関数をmanifest.jsonのCommandに紐づけます。
// =======================================
public void DeriveSoftwareRequirements(ICommandContext context, ICommandParams parameters)
{
    // 1. メインエディタ・サブエディタで選択中のモデルを取得します。
    // メインエディタで選択中のモデルとシステム要求グループ・システム要求を取得します。
    var selectedModelsMain = GetSelectedModelsInMainEditor(context).ToList();
    var selectedSystemReqs = selectedModelsMain
        .Where(model => model.AsIn(new[] { CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, CLASS_NAME_SYSTEM_REQUIREMENT }))
        .ToList();

    // サブエディタで選択中のモデルを取得します。
    var selectedModelsSub = GetSelectedModelsInSubEditor(context).ToList();

    // 2. 正しくモデルが選択されているかを確認します。不正である場合はダイアログを表示して終了します。
    // 2.1. メインエディタでシステム要求グループまたはシステム要求が1つ以上選択されていること。
    if (!selectedSystemReqs.Any())
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_NO_SELECTED_SOURCE);
        return;
    }

    // 2.2. サブエディタが表示されていて、1つ選択されていて、ソフトウェア要求分析またはソフトウェア要求グループであること。
    var isValidSubEditor =
        context.App.Window.EditorPage.IsSubEditorVisible &&
        selectedModelsSub.Count == 1 &&
        selectedModelsSub.First().AsIn(new[] { CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS, CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP });

    if (!isValidSubEditor)
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_SUB_EDITOR_INVALID);
        return;
    }

    // 3. 導出元・導出先モデルを取得します。
    // 導出元モデルを取得します。システム要求分析をルートとして再帰的に探索します。
    var srcModels = new List<IModel>();
    var srcProcessRoot = selectedSystemReqs.First().FindOwnerByClass(CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS);
    var targetClasses = new[] { CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, CLASS_NAME_SYSTEM_REQUIREMENT };
    CollectSelectedRootModels(srcProcessRoot, selectedSystemReqs, targetClasses, srcModels);

    // 導出先のモデルを取得します。
    var dstModel = selectedModelsSub.First();

    // 4. 既存のソフトウェア要求のIDの最大値を取得します。
    // 導出先のソフトウェア要求分析ルート以下の全ソフトウェア要求を取得します。
    var allSoftwareReqAnalyses = context.App.Workspace.CurrentProject.GetRootChildren()
        .Where(model => model.As(CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS));
    var allSoftwareReqs = allSoftwareReqAnalyses
        .SelectMany(analysis => analysis.GetAllChildren().Where(model => model.As(CLASS_NAME_SOFTWARE_REQUIREMENT)));

    // ソフトウェア要求のIDプレフィックスを取得します。
    // updateId.csで定義されたPROCESS_ID_CONFIGSから取得します。
    var idPrefix = PROCESS_ID_CONFIGS
        .First(c => c.TargetClasses.Contains(CLASS_NAME_SOFTWARE_REQUIREMENT))
        .Prefix;

    // 取得した全ソフトウェア要求から、IDの最大値を取得します。
    var maxId = GetMaxId(allSoftwareReqs, FIELD_NAME_ID, idPrefix);

    // 5. 導出を実施します。
    // 実行前にエラーウインドウの内容をクリアします。
    context.App.Errors.ClearErrors();

    // 作成したソフトウェア要求モデルを収集するリストを用意します。
    var createdSoftwareRequirements = new List<IModel>();

    foreach (var srcModel in srcModels)
    {
        // 導出元モデルの子孫を辿り、同様の構造を導出先モデル配下に作成します。
        if (srcModel.As(CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP))
        {
            // 導出先モデルのクラスに応じて、導出するフィールドを変えます。
            var derivationFieldName = FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS;
            if (dstModel.As(CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS))
            {
                derivationFieldName = FIELD_NAME_REQUIREMENTS_GROUP;
            }

            // システム要求グループを導出元として、ソフトウェア要求グループを作成します。
            var newModel = dstModel.AddNewModel(derivationFieldName, CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP);
            newModel.SetField(FIELD_NAME_NAME, srcModel.Name);

            // サブエディタの選択モデル直下に追加した子モデルにInformation通知を登録します。
            newModel.AddError(FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_CREATED);

            // 子孫を再帰的に導出します。
            DeriveChildSoftwareRequirements(srcModel, newModel, createdSoftwareRequirements);
        }
        else if (srcModel.As(CLASS_NAME_SYSTEM_REQUIREMENT))
        {
            if (dstModel.As(CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS))
            {
                // 導出元がシステム要求、導出先がソフトウェア要求の場合はモデル作成不可のため、エラーを追加します。
                srcModel.AddError(FIELD_NAME_NAME, "Error", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_FAILED);
                continue;
            }

            // システム要求を導出元として、ソフトウェア要求を作成します。
            var newModel = dstModel.AddNewModel(FIELD_NAME_SOFTWARE_REQUIREMENTS, CLASS_NAME_SOFTWARE_REQUIREMENT);
            newModel.SetField(FIELD_NAME_NAME, srcModel.Name);
            newModel.SetField(FIELD_NAME_INPUT_SYSTEM_REQUIREMENT, srcModel);

            // 作成したソフトウェア要求をリストに追加します。
            createdSoftwareRequirements.Add(newModel);

            // サブエディタの選択モデル直下に追加した子モデルにInformation通知を登録します。
            newModel.AddError(FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_CREATED);
        }
    }

    // 6. 作成したソフトウェア要求にIDを一括付与します。
    var (updatedModels, errorModels) = SetSequentialIds(
        createdSoftwareRequirements,
        maxId + 1,
        idPrefix
    );

    // エラーモデルに通知を付与します。
    foreach (var model in errorModels)
    {
        model.AddError(FIELD_NAME_ID, "Error", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_ID_OVERFLOW);
    }

    // 7. エラーウインドウを表示します。
    context.App.Window.IsInformationPaneVisible = true;
    context.App.Window.ActiveInfoWindow = "Error";

    // 8. エラーがあった場合はダイアログを表示します。
    if (context.App.Errors.Errors.Any())
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_HAS_ERROR);
    }
}

// =======================================
// サブ処理関数
// =======================================

// ---------------------------------------
// 子孫のソフトウェア要求導出関数
// 導出元のシステム要求グループと同様の構造を、導出先のソフトウェア要求グループ配下に作成します。
// 引数：導出元システム要求グループ、導出先ソフトウェア要求グループ、作成したソフトウェア要求を格納するリスト
// ---------------------------------------
private void DeriveChildSoftwareRequirements(IModel srcGroup, IModel dstGroup, List<IModel> createdSoftwareRequirements)
{
    // 導出元グループの子モデルを走査します。
    var children = srcGroup.GetChildren();
    foreach (var model in children)
    {
        if (model.As(CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP))
        {
            // システム要求グループ → ソフトウェア要求グループを作成します。
            var newModel = dstGroup.AddNewModel(FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS, CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP);
            newModel.SetField(FIELD_NAME_NAME, model.Name);

            // 追加したモデルを起点に、子孫モデルを導出します。
            DeriveChildSoftwareRequirements(model, newModel, createdSoftwareRequirements);
        }
        else if (model.As(CLASS_NAME_SYSTEM_REQUIREMENT))
        {
            // システム要求 → ソフトウェア要求を作成します。
            var newModel = dstGroup.AddNewModel(FIELD_NAME_SOFTWARE_REQUIREMENTS, CLASS_NAME_SOFTWARE_REQUIREMENT);
            newModel.SetField(FIELD_NAME_NAME, model.Name);
            newModel.SetField(FIELD_NAME_INPUT_SYSTEM_REQUIREMENT, model);

            // 作成したソフトウェア要求をリストに追加します。
            createdSoftwareRequirements.Add(newModel);
        }
        else
        {
            // システム要求グループとシステム要求以外は無視します。
        }
    }
}

