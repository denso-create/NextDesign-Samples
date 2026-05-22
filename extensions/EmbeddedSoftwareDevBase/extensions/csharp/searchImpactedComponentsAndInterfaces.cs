// =======================================
// 機能 : IFの影響箇所を抽出
// =======================================
//
// 選択されたソフトウェアコンポーネントまたは提供インタフェースを起点に、
// 影響を受けるソフトウェアコンポーネントとインタフェースを探索し、検索結果に登録します。
// エディタでダイアグラムを表示中の場合は、影響箇所の経路となるコネクタも検索結果に登録します。
//
// 処理概要
//   - エディタで選択中のモデルが調査対象のクラスであることを確認します。
//   - カレントエディタで表示中のERダイアグラムからコネクタを取得します。
//   - 調査対象のモデルから影響箇所をスタックベースで探索し、検索結果に登録します。
//   - 検索結果をユーザに通知します。
//
// 補足
//   処理の実装にLINQ(Any, Skip, FirstOrDefault, Distinct, ToList)を使用しています。
//   LINQについては以下を参照してください。
//   LINQの概要：https://learn.microsoft.com/ja-jp/dotnet/csharp/linq
//   APIリファレンス：https://learn.microsoft.com/ja-jp/dotnet/api/system.linq.enumerable


// =======================================
// 外部ファイル・名前空間読み込み
// =======================================
#load "utils.cs" // 汎用関数
#load "metamodel.cs" // メタモデル情報

// =======================================
// ユーザが変更する設定値（パラメータ類）
// この領域を編集して、操作対象やメッセージを変更できます。
// =======================================

// ---------------------------------------
// 調査対象のクラス名
// 調査の起点として選択できるモデルのクラス名を定義します。
// ---------------------------------------
string[] SEARCH_TARGET_CLASSES = new string[]
{
    CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT,
    CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN
};

// ---------------------------------------
// 検索結果に関する定義
// ---------------------------------------
string SEARCH_NAME = "IFの影響箇所";
string SEARCH_MATCH_TYPE = "match";

// 検索結果に設定するフィールド名
string SEARCH_FIELD_ORIGIN = "Name";
string SEARCH_FIELD_INTERFACE = "Name";
string SEARCH_FIELD_COMPONENT = "Name";
string SEARCH_FIELD_CONNECTOR = null; // nullを指定することで、フィールドを指定せずに検索結果に登録します。

// 検索結果に設定するメッセージ
string SEARCH_MSG_ORIGIN = "起点となるモデルです。";
string SEARCH_MSG_INTERFACE = "{0} の影響を受けるインタフェースです。"; // {0}には起点モデルの名前を代入します。
string SEARCH_MSG_COMPONENT = "{0} の影響を受けるソフトウェアコンポーネントです。";
string SEARCH_MSG_CONNECTOR = "{0} と {1} のコネクタです。"; // {0}には検索対象モデルの名前、{1}にはその影響を受けるモデルの名前を代入します。

// ---------------------------------------
// メッセージ（ユーザ通知）
// ダイアログで表示する文字列です。
// ---------------------------------------
string DIALOG_MSG_INVALID_SEARCH_TARGET_SELECTION = "起点となるインタフェース、または、ソフトウェアコンポーネントを1つだけエディタで選択してください。";
string DIALOG_MSG_NO_IMPACT = "接続している要素はありませんでした。";

// =======================================
// メイン処理関数
// ここで作成した関数をmanifest.jsonのCommandに紐づけます。
// =======================================
public void SearchImpactedComponentsAndInterfaces(ICommandContext context, ICommandParams parameters)
{
    // 1. 調査対象のモデルを取得します。
    var selectedModels = GetSelectedModels(context).ToList();

    // 選択中のモデルの内、調査対象のクラスに該当するモデルを取得します。
    var searchRootModel = selectedModels.FirstOrDefault(model => model.AsIn(SEARCH_TARGET_CLASSES));

    // 2. 選択中のモデルが1つかつ調査対象のクラスであるかを確認します。
    if (selectedModels.Count != 1 || searchRootModel == null)
    {
        // 条件を満たさない場合、ダイアログを表示して終了します。
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_INVALID_SEARCH_TARGET_SELECTION);
        return;
    }

    // 3. 現在のエディタで開かれているダイアグラムからコネクタを取得し、始点・終点モデルで検索できるようにインデックス化します。
    var diagram = context.App.Window.EditorPage?.CurrentEditorView.Editor as IDiagram;
    var connectorLookup = CreateConnectorLookup(diagram);

    // 4. 既存の検索結果をクリアし、検索を開始します。
    var searchManager = context.App.Search;
    var search = searchManager.Create();
    searchManager.ClearResults();
    search.BeginSearch(SEARCH_NAME, SEARCH_MATCH_TYPE);

    // 5. 起点モデルから影響箇所を探索します。
    var visited = new HashSet<IModel>();
    SearchImpact(searchRootModel, visited, search, connectorLookup);

    // 検索を終了します。
    search.EndSearch();

    // 6. 結果をユーザに通知します。
    if (searchManager.AllResults.Skip(1).Any())
    {
        // 起点のモデル以外に影響を受けるモデルがあった場合、検索ウィンドウをアクティブ化します。
        context.App.Window.IsInformationPaneVisible = true;
        context.App.Window.ActiveInfoWindow = "SearchResult";
    }
    else
    {
        // 起点のモデル以外に影響を受けるモデルがなかった場合、検索結果をクリアします。
        searchManager.ClearResults();

        // 影響を受けるモデルがないことをダイアログで通知します。
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_IMPACT);
    }
}

// =======================================
// サブ処理関数
// =======================================

// ---------------------------------------
// 影響箇所探索関数
// 起点となるモデルを検索結果に登録し、該当フィールドに設定されているモデルを影響箇所として探索します。
// 探索の際、影響箇所の経路となるコネクタも検索結果に登録します。
// モデルを1つずつ辿るため、スタックオーバーフロー対策として再帰の代わりにスタックを使用しています。
// 引数：起点となるモデル、訪問済みモデルのセット、検索オブジェクト、コネクタインデックス
// ---------------------------------------
private void SearchImpact(IModel searchRootModel, HashSet<IModel> visited, ISearch search, Dictionary<(string, string), List<IConnector>> connectorLookup)
{
    // 影響箇所を辿るためのスタックを用意し、起点となるモデルを最初に追加します。
    var stack = new Stack<(IModel impactedModel, IModel searchModel)>();
    stack.Push((searchRootModel, null));

    // スタックが空になるまで、影響箇所を辿ります。
    var isFirst = true;
    while (stack.Count > 0)
    {
        // スタックから次の調査対象モデルを取得します。
        var (impactedModel, searchModel) = stack.Pop();

        // 親モデルとの間のコネクタを検索結果に登録します。
        SearchConnectorsBetween(searchModel, impactedModel, connectorLookup, search);

        // 訪問済みである場合は無視します。
        if (visited.Contains(impactedModel)) continue;

        // 調査対象モデルのクラスに応じて、検索結果のメッセージと次の探索対象を決定します。
        string message;
        string fieldName;
        var nextTargetModels = new List<IModel>();
        if (impactedModel.As(CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT))
        {
            // インタフェースの場合。
            message = string.Format(SEARCH_MSG_INTERFACE, searchRootModel.Name);
            fieldName = SEARCH_FIELD_INTERFACE;

            // 次の調査対象モデルを取得します。
            nextTargetModels.AddRange(impactedModel.GetFieldValues(FIELD_NAME_USED_BY_COMPONENTS));
            nextTargetModels.AddRange(impactedModel.GetFieldValues(FIELD_NAME_DELEGATED_INTERFACES));
        }
        else if (impactedModel.As(CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN))
        {
            // ソフトウェアコンポーネントの場合。
            message = string.Format(SEARCH_MSG_COMPONENT, searchRootModel.Name);
            fieldName = SEARCH_FIELD_COMPONENT;

            // 次の調査対象モデルを取得します。
            nextTargetModels.AddRange(impactedModel.GetFieldValues(FIELD_NAME_INTERFACE_FUNCTIONS));
            nextTargetModels.AddRange(impactedModel.GetFieldValues(FIELD_NAME_INTERFACE_DATA));
        }
        else
        {
            // 対象外のクラスの場合は無視します。
            continue;
        }

        if (isFirst)
        {
            // 起点モデルの場合はメッセージを変更します。
            message = SEARCH_MSG_ORIGIN;
            fieldName = SEARCH_FIELD_ORIGIN;
            isFirst = false;
        }

        // 検索結果に登録します。
        search.AddSearchResult(impactedModel, fieldName, message);

        // 訪問済みに追加します。
        visited.Add(impactedModel);

        // 次の調査対象モデルをスタックに追加します。Distinctで重複を排除します。
        foreach (var nextTarget in nextTargetModels.Distinct())
        {
            stack.Push((nextTarget, impactedModel));
        }
    }
}

// ---------------------------------------
// モデル間のコネクタ検索関数
// 2つのモデル間を結ぶコネクタをインデックスから検索し、見つかった場合は検索結果に登録します。
// 引数：モデル1、モデル2、コネクタインデックス、検索オブジェクト
// ---------------------------------------
private void SearchConnectorsBetween(IModel searchModel, IModel impactedModel, Dictionary<(string, string), List<IConnector>> connectorLookup, ISearch search)
{
    if (searchModel == null || impactedModel == null) return;

    // コネクタのインデックスから、2つのモデルを結ぶコネクタを検索します。
    var key = (searchModel.Id, impactedModel.Id);
    if (connectorLookup.TryGetValue(key, out var connectors))
    {
        // 見つかったコネクタを検索結果に登録します。
        foreach (var connector in connectors)
        {
            var message = string.Format(SEARCH_MSG_CONNECTOR, searchModel.Name, impactedModel.Name);
            search.AddSearchResult(connector.Model, SEARCH_FIELD_CONNECTOR, message);
        }
    }
}

// ---------------------------------------
// コネクタインデックス作成関数
// ダイアグラムからコネクタを取得し、始点・終点モデルの組み合わせをキーとするインデックスを作成します。
// 始点・終点の向きは問わず、双方向で登録します。
// ダイアグラムがnullの場合は空のインデックスを返します。
// 引数：ダイアグラム
// 戻り値：コネクタインデックス
// ---------------------------------------
private Dictionary<(string, string), List<IConnector>> CreateConnectorLookup(IDiagram diagram)
{
    var connectorLookup = new Dictionary<(string, string), List<IConnector>>();

    if (diagram == null)
    {
        // ダイアグラムがnullの場合は空のインデックスを返します。
        return connectorLookup;
    }

    // ダイアグラム中のコネクタを走査し、始点・終点モデルの組み合わせをキーとするインデックスを作成します。
    foreach (var connector in diagram.Connectors)
    {
        var startId = connector.StartPoint.Model.Id;
        var endId = connector.EndPoint.Model.Id;

        // 双方向でキーを作成します。
        var key1 = (startId, endId);
        var key2 = (endId, startId);

        // 始点・終点の組み合わせをキーとするリストを作成します。
        // 同じ始点・終点を持つコネクタは同じキーのリストに追加します。
        if (!connectorLookup.ContainsKey(key1))
        {
            connectorLookup[key1] = new List<IConnector>();
        }
        if (!connectorLookup.ContainsKey(key2))
        {
            connectorLookup[key2] = new List<IConnector>();
        }

        // コネクタをリストに追加します。
        connectorLookup[key1].Add(connector);
        connectorLookup[key2].Add(connector);
    }

    return connectorLookup;
}