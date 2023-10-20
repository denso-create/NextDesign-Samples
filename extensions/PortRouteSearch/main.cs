private const string c_StyleName = "ADAS開発向けサンプル.スタイル";

/// <summary>
/// 探索経路を記録するスタック
/// 一度、探索した経路は探索から除外するために使用する
/// </summary>
private IList<IModel> ROUTE = new List<IModel>();

/// <summary>
/// 枠線の色一覧
/// </summary>
private static string[] BorderColors = new string[] { "#FF0000", "#FFFF00", "#0000FF", "#FFA500", "#008000", "#FF00FF", "#00FFFF" };

/// <summary>
/// 使用する枠線の色
/// </summary>
private static string BorderColor = "";

/// <summary>
/// 前回の枠線の色番号
/// </summary>
private static int LastBorderColorNo = 0;

#region ポート経路探索

/// <summary>
/// ポート経路探索の切り替え
/// </summary>
/// <param name="context">コンテキスト</param>
/// <param name="parameters">パラメータ</param>
public void SwitchPortRouteSearch(ICommandContext context,ICommandParams paramemters)
{
	// 経路探索チェックの確認
	if (DoPortRouteSearch(context.Global))
	{
		return;
	}

	// 経路探索OFFの場合は検索結果をクリアするために空検索を実行する
	var search = Search.Create();
	search.BeginSearch("ポート経路探索", "type"); 
	search.EndSearch();
}


/// <summary>
/// ポート選択イベント処理
/// </summary>
/// <param name="context">コンテキスト</param>
/// <param name="parameters">パラメータ</param>
public void OnPortSelected(IEventContext context,IEventParams parameters)
{
	// 経路探索チェックの確認
	if (!DoPortRouteSearch(context.Global))
	{
		return;
	}

	// 前回の検索結果をクリア
	var search = Search.Create();
	search.ClearSearchResult();	

	// 枠線の色の決定 (将来、検索の度に色が変更できるようにしておく。現状は何度検索されても色は同じ)
	BorderColor = BorderColors[LastBorderColorNo];

	//検索トランザクションの開始
	search.BeginSearch("ポート経路探索", "type", true); 

	//選択要素の取得
	var modelSelectionChangedEventParams = parameters as ModelSelectionChangedEventParams;
	var selectedModel = modelSelectionChangedEventParams.SelectedItem;

	//探索開始
	PrintSearchResult(search, selectedModel, "ToPorts");
	SearchTerminalNode(selectedModel, search, "ToPorts");

	//検索トランザクションの終了
	search.EndSearch();
}

/// <summary>
/// 指定のポートから入出力ポートを探索する
/// </summary>
/// <param name="startPort">本メソッドで探索を開始するポート</param>
/// <param name="search">検索管理</param>
/// <param name="field">本メソッドで探索を開始するポートの属性名</param>
private void SearchTerminalNode(IModel startPort, ISearch search, string field) 
{
	if (ROUTE.Contains(startPort)) 
	{
		//探索済みの経路は出力しない
		return;
	}
	ROUTE.Add(startPort);
	//ROUTE.Push(startPort);		

	var owner = startPort.Owner;
	if (!startPort.GetRelations("ToPorts").Any()) 
	{
		if (owner.As("SystemFunctionalElement"))
		{
			if (!owner.GetRelations("OutputPorts").Any()) 
			{
				//終端に達した場合
				return;
			} 
	
			//OutputPorts属性の探索
			SearchOutputPorts(startPort, search);
		}
		else if (owner.As("ControlLogicElement"))
		{
			if (!owner.GetRelations("OutputPort").Any()) 
			{
				//終端に達した場合
				return;
			} 
	
			//OutputPort属性の探索
			SearchOutputPort(startPort, search);
		}
	}
	else 
	{
		//ToPorts属性の探索()
		SearchInputPort(startPort, search);
	}
	//ROUTE.Pop();
}

/// <summary>
/// 指定のポートから出力ポートを探索する
/// </summary>
/// <param name="startPort">本メソッドで探索を開始するポート</param>
/// <param name="search">検索管理</param>
private void SearchOutputPorts(IModel startPort, ISearch search)
{
	//出力ポート(OutputPorts)の探索
	var owner = startPort.Owner;	
	foreach (var relation in owner.GetRelations("OutputPorts")) 
	{
		var target = relation.Target;
		PrintSearchResult(search, target, relation, "OutputPorts");
		SearchTerminalNode(target, search, "OutputPorts");
	}
}

/// <summary>
/// 指定のポートから出力ポートを探索する
/// </summary>
/// <param name="startPort">本メソッドで探索を開始するポート</param>
/// <param name="search">検索管理</param>
private void SearchOutputPort(IModel startPort, ISearch search)
{
	//出力ポート(OutputPorts)の探索
	var owner = startPort.Owner;	
	foreach (var relation in owner.GetRelations("OutputPort")) 
	{
		var target = relation.Target;
		PrintSearchResult(search, target, relation, "OutputPort");
		SearchTerminalNode(target, search, "OutputPort");
	}
}

/// <summary>
/// 指定のポートから入力ポートを探索する
/// </summary>
/// <param name="startPort">本メソッドで探索を開始するポート</param>
/// <param name="search">検索管理</param>
private void SearchInputPort(IModel startPort, ISearch search)
{
	//入力ポート(ToPorts)の探索
	foreach(var relation in startPort.GetRelations("ToPorts")) 
	{
		var target = relation.Target;
		PrintSearchResult(search, target, relation, "ToPorts");
		SearchTerminalNode(target, search, "ToPorts");
	}
}

#region 検索結果出力
/// <summary>
/// 検索結果を出力する
/// </summary>
/// <param name="search">検索管理</param>
/// <param name="model">モデル</param>
/// <param name="field">modelの属性名</param>
private void PrintSearchResult(ISearch search, IModel port, IModel relation, string field) 
{
	//関連線の出力
	PrintSearchResult(search, relation, "関連", field);		
	//入出力ポートの出力	
	PrintSearchResult(search, port, field);
}

/// <summary>
/// 検索結果を出力する
/// </summary>
/// <param name="search">検索管理</param>
/// <param name="model">モデル</param>
/// <param name="field">modelの属性名</param>
private void PrintSearchResult(ISearch search, IModel model, string field) 
{
   	var styleSet = Workspace.InfoDisplayStyleSet;
   	var style = styleSet.CreateStyle(c_StyleName);

	var dic = new Dictionary<string, string>();
	dic.Add("BorderColor", BorderColor);
   	style.SetStyleSets("", dic);

   	var result = search.AddSearchResult(model, field, model.Name);
   	result.DisplayStyleName = style.Name;
	//Output.WriteLine("経路検索", string.Format("{0}({1})", model.Name, model.ModelPath));
}

/// <summary>
/// 検索結果を出力する
/// </summary>
/// <param name="search">検索管理</param>
/// <param name="model">モデル</param>
/// <param name="name">名前</param>
/// <param name="field">modelの属性名</param>
private void PrintSearchResult(ISearch search, IModel model, string name, string field) 
{
   	var styleSet = Workspace.InfoDisplayStyleSet;
   	var style = styleSet.CreateStyle(c_StyleName);

	var dic = new Dictionary<string, string>();
	dic.Add("BorderColor", BorderColor);
    style.SetStyleSets("", dic);

   	var result = search.AddSearchResult(model, field, name);
   	result.DisplayStyleName = style.Name;
	//Output.WriteLine("経路検索", string.Format("{0}({1})", model.Name, model.ModelPath));
}

/// <summary>
/// ポート経路探索を実行するか確認する
/// ポート経路探索は、コンテキストでPortRouteSearchが真値の場合のみ実施する
/// </summary>
private bool DoPortRouteSearch(IContext context)
{
	var check = context.GetProperty("PortRouteSearch");
	return (check != null && (bool)check);
}

#endregion

#endregion