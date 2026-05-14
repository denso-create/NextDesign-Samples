// =======================================
// 機能 : IDを更新
// =======================================
//
// 選択中のモデルとその子孫のモデルのIDを一意になるように一括で振りなおします。
// IDは工程毎に一意になるように割り振ります。
//
// 処理概要
//   - 更新対象となるモデルを取得します。
//   - 更新対象でないモデルから、既存のIDの最大値を求めます。
//   - 求めたIDの最大値+1からはじめ、順にIDを割り振ります。
//   - 結果をダイアログとエラー追加で通知します。
//
// 補足
//   処理の実装にLINQ(Any, Where, Select, SelectMany, Except, Max, ToArray, ToList, ToHashSet)を使用しています。
//   LINQについては以下を参照してください。
//   LINQの概要：https://learn.microsoft.com/ja-jp/dotnet/csharp/linq
//   APIリファレンス：https://learn.microsoft.com/ja-jp/dotnet/api/system.linq.enumerable


// =======================================
// 外部ファイル・名前空間読み込み
// =======================================
#load "utils.cs"     // 汎用関数
#load "metamodel.cs" // クラス名などのメタモデル情報
using System.Text.RegularExpressions; // 正規表現を使用するための名前空間

// =======================================
// ユーザが変更する設定値（パラメータ類）
// この領域を編集して、操作対象やメッセージを変更できます。
// =======================================

// ---------------------------------------
// 工程情報の配列
// 各工程の情報をまとめて定義します。
// この配列に要素を追加することで、新しい工程を処理対象に追加できます。
// ---------------------------------------
ProcessIdConfig[] PROCESS_ID_CONFIGS = new ProcessIdConfig[]
{
    // システム要求分析工程
    new ProcessIdConfig
    {
        RootClasses     = new[] {CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS},
        StartClasses    = new[] {CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS, CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, CLASS_NAME_SYSTEM_REQUIREMENT},
        TargetClasses   = new[] {CLASS_NAME_SYSTEM_REQUIREMENT},
        Prefix = "SYRQ-"
    },

    // ソフトウェア要求分析工程
    new ProcessIdConfig
    {
        RootClasses     = new[] {CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS},
        StartClasses    = new[] {CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS, CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP, CLASS_NAME_SOFTWARE_REQUIREMENT},
        TargetClasses   = new[] {CLASS_NAME_SOFTWARE_REQUIREMENT},
        Prefix = "SWRQ-"
    },

    // ソフトウェアコンポーネントテスト工程
    new ProcessIdConfig
    {
        RootClasses     = new[] {CLASS_NAME_SOFTWARE_COMPONENT_TEST},
        StartClasses    = new[] {CLASS_NAME_SOFTWARE_COMPONENT_TEST, CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST, CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST},
        TargetClasses   = new[] {CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST},
        Prefix = "SWCT-"
    },

    // ソフトウェア統合テスト工程
    new ProcessIdConfig
    {
        RootClasses     = new[] {CLASS_NAME_SOFTWARE_INTEGRATION_TEST},
        StartClasses    = new[] {CLASS_NAME_SOFTWARE_INTEGRATION_TEST, CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST, CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST},
        TargetClasses   = new[] {CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST},
        Prefix = "SWIT-"
    },

    // ソフトウェアテスト工程
    new ProcessIdConfig
    {
        RootClasses     = new[] {CLASS_NAME_SOFTWARE_TEST},
        StartClasses    = new[] {CLASS_NAME_SOFTWARE_TEST, CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST, CLASS_NAME_TEST_CASE_SOFTWARE_TEST},
        TargetClasses   = new[] {CLASS_NAME_TEST_CASE_SOFTWARE_TEST},
        Prefix = "SWTT-"
    }
};

// ---------------------------------------
// IDに関する定義
// ---------------------------------------
int UPDATE_ID_DIGITS = 6; // IDの桁数

// ---------------------------------------
// メッセージ（ユーザ通知）
// ダイアログやエラー追加で表示する文字列です。
// ---------------------------------------
string DIALOG_MSG_NO_UPDATE_TARGET_SELECTED = "IDがあるモデル、または、IDがあるモデルの祖先モデルをエディタで選択してください。";
string DIALOG_MSG_HAS_FAILED_ID = "IDの更新に失敗したモデルがあります。\nエラーウインドウを確認してください。";
string DIALOG_NO_ID_UPDATED = "更新対象となるモデルはありませんでした。";
string ERROR_TITLE_UPDATE_ID = "IDの更新";
string ERROR_MSG_SUCCESS_UPDATE_ID = "{0} を設定しました。"; //{0}としておくことで、後から変数で置き換えられる。
string ERROR_MSG_FAILED_UPDATE_ID = "連番が最大値を超えたため、値をクリアしました。";

// =======================================
// メイン処理関数
// ここで作成した関数をmanifest.jsonのCommandに紐づけます。
// =======================================
public void UpdateId(ICommandContext context, ICommandParams parameters)
{
    // 1. 選択モデルを取得し、工程ごとの選択モデルの配列を作成します。
    // エディタで選択中のモデルを取得します。
    var selectedModels = GetSelectedModels(context);

    // 工程ごとに「起点クラス(StartClasses)に該当する選択モデル」だけを抽出して配列にまとめます。
    // 例：ソフトウェア要求のモデルが1つだけ選択されている場合、
    //    selectedModelsByProcess = {[], [ソフトウェア要求のモデル], []}
    var selectedModelsByProcess = PROCESS_ID_CONFIGS
        .Select(process =>
            // この工程のStartClassesに該当する選択モデルだけを抽出します。
            selectedModels.Where(model => model.AsIn(process.StartClasses)))
        .ToArray();

    // 2. 起点となるクラスに該当するモデルが1つでも選択されているかを確認します。
    if (!selectedModelsByProcess.Any(arr => arr.Any()))
    {
        // 選択されていない場合、ダイアログを表示して終了します。
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_UPDATE_TARGET_SELECTED);
        return;
    }

    // 3. 各工程のIDを更新します。
    // 既存のエラーを全てクリアします。
    context.App.Errors.ClearErrors();

    // プロジェクト直下のモデルを取得します。
    var rootChildren = context.App.Workspace.CurrentProject.GetRootChildren();

    // 4. 各工程のID更新処理を実行します。
    for (int i = 0; i < PROCESS_ID_CONFIGS.Length; i++)
    {
        // 工程ごとのプロジェクト直下のモデルを取得します。
        var processRootModels = rootChildren.Where(model => model.AsIn(PROCESS_ID_CONFIGS[i].RootClasses)).ToList();

        // ID更新処理を実行します。
        UpdateIdsForProcess(
            PROCESS_ID_CONFIGS[i],
            selectedModelsByProcess[i],
            processRootModels
        );
    }

    // 5. 処理結果を通知します。
    ShowResultNotification(context.App.Errors, context.App.Window);
}

// =======================================
// サブ処理関数
// =======================================

// ---------------------------------------
// 1工程のID更新関数
// 工程内の選択モデルとその子孫のモデルを対象にIDを更新します。
// 対象でないモデルから既存IDの最大値を取得し、最大値+1からはじめモデルナビゲータで上から順になるようにIDを付与します。
// IDに設定できる最大値を超える場合はエラーとし、空文字を設定します。
// 引数：工程情報、選択モデル、対象工程のルートのモデル
// ---------------------------------------
private void UpdateIdsForProcess(
    ProcessIdConfig processInfo,
    IEnumerable<IModel> selectedModels,
    IEnumerable<IModel> rootModels
    )
{
    // 1. 工程内の更新対象クラスに該当するモデルを全て取得します。
    var allTargetClassModels = rootModels
        .SelectMany(model => model.GetAllChildren()) // 全てのmodelから子孫モデルを取得します。
        .Where(model => model.AsIn(processInfo.TargetClasses)) // 対象クラスのみ抽出します。
        .ToList();

    // 2. 更新対象のモデルを取得します。
    var (targetModels, otherModels) = SplitModelsIntoTargetAndOthers(allTargetClassModels, selectedModels, processInfo.TargetClasses);

    // 3. 更新対象外のモデルからIDの最大値を取得します。
    var maxId = GetMaxId(otherModels, FIELD_NAME_ID, processInfo.Prefix);

    // 4. IDを更新します。
    var (updatedModels, errorModels) = SetSequentialIds(
        targetModels,
        maxId + 1,
        processInfo.Prefix
    );

    // 5. 通知を付与します。
    foreach (var model in updatedModels)
    {
        // 成功したモデルには、エラー（種別=information）を追加します。
        var newId = model.GetFieldString(FIELD_NAME_ID);
        model.AddError(FIELD_NAME_ID, "Information", ERROR_TITLE_UPDATE_ID, string.Format(ERROR_MSG_SUCCESS_UPDATE_ID, newId));
    }
    foreach (var model in errorModels)
    {
        // エラーとなったモデルには、エラー（種別=error）を追加します。
        model.AddError(FIELD_NAME_ID, "Error", ERROR_TITLE_UPDATE_ID, ERROR_MSG_FAILED_UPDATE_ID);
    }
}

// ---------------------------------------
// 更新対象・更新対象外モデル振り分け関数
// 以下の2つに振り分けます。
// - 更新対象モデル：選択中モデルとその子孫モデルの内、指定された工程の対象クラスに該当するもの。
// - 更新対象外モデル：指定された工程の対象クラスに該当する全モデルの内、上記以外のもの。
// 引数：すべてのモデル、選択モデル、対象クラス名配列
// 戻り値：更新対象モデル、更新対象外モデル
// ---------------------------------------
private (IEnumerable<IModel>, IEnumerable<IModel>) SplitModelsIntoTargetAndOthers(
    IEnumerable<IModel> models,
    IEnumerable<IModel> selectedModels,
    string[] targetClassNames
    )
{
    // 選択中モデルとその子孫モデルの内、対象クラスに該当するものを取得します。
    var selectedWithChildren = selectedModels
        .SelectMany(model => model.GetAllChildren().Prepend(model)) // 選択中のモデルと子孫モデルのコレクションを取得します。
        .Where(model => model.AsIn(targetClassNames)).ToHashSet(); // 対象のクラスのみ抜き出し、重複を排除します。

    // 更新対象モデルと更新対象外モデルに分離します。
    var targetModels = new List<IModel>();
    var otherModels = new List<IModel>();
    foreach (var model in models)
    {
        if (selectedWithChildren.Contains(model))
        {
            targetModels.Add(model);
        }
        else
        {
            otherModels.Add(model);
        }
    }

    return (targetModels, otherModels);
}

// ---------------------------------------
// ID最大値算出関数
// 受け取ったモデルの中からIDの最大値を取得します。
// 引数：モデル、IDのフィールド名、IDのプレフィックス
// 戻り値：IDの最大値
// ---------------------------------------
private int GetMaxId(IEnumerable<IModel> models, string fieldName, string prefix)
{
    if (!models.Any())
    {
        // 受け取ったモデルが空の場合、0を返します。
        return 0;
    }

    // 命名規則に合致するIDの最大値を取得します。
    // プレフィックスと桁数から正規表現を生成します。
    var regexPattern = $"^{Regex.Escape(prefix)}(?<num>[0-9]{{{UPDATE_ID_DIGITS}}})$";
    var regex = new Regex(regexPattern);

    var maxId = models.Max(model =>
    {
        var id = model.GetFieldString(fieldName);

        // 正規表現で命名規則に合致するかを確認します。
        var match = regex.Match(id);
        if (!match.Success)
        {
            // 命名規則に則っていない場合は無視します。
            return 0;
        }

        // ID文字列から数字部分を抽出して整数に変換します。
        // 例："SYRQ-000123" の場合、 "000123" を取得して 123 に変換します。
        return int.Parse(match.Groups["num"].Value);
    });

    return maxId;
}

// ---------------------------------------
// 連番ID設定関数
// 指定された値を初期値として、全モデルのIDに連番のIDを付与します。
// IDが最大値を超えた場合は、モデルのIDに空文字列を設定します。
// 引数：更新対象のモデル、IDの開始値、IDのプレフィックス
// 戻り値：成功したモデル、最大値を超えて失敗したモデル
// ---------------------------------------
private (List<IModel> updatedModels, List<IModel> errorModels) SetSequentialIds(
    IEnumerable<IModel> targetModels,
    int startIdNumber,
    string prefix
    )
{
    var updatedModels = new List<IModel>();
    var errorModels = new List<IModel>();
    int nextIdNumber = startIdNumber;

    int maxIdNumber = (int)Math.Pow(10, UPDATE_ID_DIGITS);

    // 各モデルに対してIDを設定します。
    foreach (IModel model in targetModels)
    {
        if (nextIdNumber >= maxIdNumber)
        {
            // IDの最大値を超える場合は空文字を設定します。
            model.SetField(FIELD_NAME_ID, string.Empty);
            errorModels.Add(model);
            continue;
        }

        // 新しいIDを生成します。
        var newId = prefix + nextIdNumber.ToString($"D{UPDATE_ID_DIGITS}");
        var currentId = model.GetFieldString(FIELD_NAME_ID);

        if (currentId != newId)
        {
            // もとのIDと異なる場合、IDを設定します。
            model.SetField(FIELD_NAME_ID, newId);
            updatedModels.Add(model);
        }

        nextIdNumber++;
    }

    return (updatedModels, errorModels);
}

// ---------------------------------------
// 結果通知関数
// 処理結果に応じた通知を行います。
// エラーウインドウを表示し、処理結果に応じたダイアログ通知を行います。
// 引数：エラー情報、UI操作のためのウインドウオブジェクト
// ---------------------------------------
private void ShowResultNotification(IErrors errors, IWorkspaceWindow window)
{
    // エラーの有無を取得します。
    var hasError = errors.Errors.Any();
    var hasChanged = errors.Informations.Any();

    // エラーウインドウを表示します。
    if (hasError || hasChanged)
    {
        window.IsInformationPaneVisible = true;
        window.ActiveInfoWindow = "Error";
    }

    // 処理結果に応じたユーザ通知を行います。
    if (hasError)
    {
        window.UI.ShowInformationDialog(DIALOG_MSG_HAS_FAILED_ID);
    }
    else if (!hasChanged)
    {
        window.UI.ShowInformationDialog(DIALOG_NO_ID_UPDATED);
    }
}

// =======================================
// データ構造定義
// =======================================

// 工程ごとにIDの更新に必要な情報をまとめて管理する構造体
private struct ProcessIdConfig
{
    public string[] RootClasses;    // 工程のルートとなるクラス名の配列（工程ごとの全モデル取得に使用）
    public string[] StartClasses;   // 起点となるクラス名の配列（工程ごとの選択モデルの判定に使用）
    public string[] TargetClasses;  // 更新対象となるクラス名の配列（ID更新対象の判定に使用）
    public string Prefix;           // IDのプレフィックス（例："SYRQ-")
}