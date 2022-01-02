// エクステンション開発で参照するAPIの名前空間の宣言
using NextDesign.Extension;
using NextDesign.Core;
using NextDesign.Desktop;

/// <summary>
/// エントリーポイントとなるDLLのメインクラス
/// </summary>
/// <remarks>
/// エントリーポイントのメインクラスには、 `IExtension` インタフェースを実装します。
/// ハンドラはこのクラスの公開メソッドとして実装します。
/// </remarks>
public class ValidationSample : IExtension
{
	/// <summary>
	/// 検証処理のコマンドハンドラ
	/// </summary>
	/// <param name="context">コマンドコンテキスト</param>
	/// <param name="parameters">コマンドパラメータ</param>
	/// <remarks>
	/// 検証処理のコマンドハンドラをメインクラスの公開メソッドとして実装します。
	/// </remarks>
	public void Run(ICommandContext context, ICommandParams parameters)
	{
		var app = context.App;
		var project = app.Workspace.CurrentProject;

		// 以前のエラーをすべてクリアします。
		app.Errors.ClearErrors();

		// エラー一覧ウィンドウを表示します。
		app.Window.IsInformationPaneVisible = true;
		app.Window.ActiveInfoWindow = "Error";

		// プロジェクト中のすべてのモデルを対象に繰り返し処理を行います。
		var models = project.GetAllChildren();
		foreach (var model in models)
		{
			// 検証ルールに従ってモデルを検証します。
			ValidateModel(model);
		}
	}

	/// <summary>
	/// モデルのフィールド変更のイベントハンドラ
	/// </summary>
	/// <param name="context">イベントコンテキスト</param>
	/// <param name="eventParams">イベントパラメータ</param>
	/// <remarks>
	/// モデルのフィールド変更イベントハンドラをメインクラスの公開メソッドとして実装します。
	/// </remarks>
	public void OnFieldChanged(IEventContext context, IEventParams eventParams)
	{
		// フィールド変更されたモデルやフィール名などの詳細情報は、イベントハンドラの第2引数に渡されるイベントパラメータの中から取得します。
		// イベントパラメータの具体的な型はイベントの種類に応じて異なるため、モデルのフィールド変更イベント用のイベントパラメータに型変換します。
		var fieldChangeParams = eventParams as ModelFieldChangedEventParams;
		var model = fieldChangeParams.Model;        // フィールド変更されたモデル
		var fieldName = fieldChangeParams.Field;    // フィールド変更されたフィールド名
		var app = context.App;

		// 変更されたフィールドが `Name` フィールドの場合のみ検証します。
		if (fieldName == "Name")
		{
			// 対象モデルに対する以前のエラーをクリアします。
			app.Errors.ClearErrorsAt(model);

			// 検証ルールに従ってモデルを検証します。
			ValidateModel(model);
		}
	}

	/// <summary>
	/// 検証ルールに従ってモデルを検証
	/// </summary>
	/// <param name="model">モデル</param>
	private void ValidateModel(IModel model)
	{
		// 次の検証ルールと照合します。
		// ・モデル名には半角スペースを含めないこと
		if (model.Name.IndexOf(" ") > 0)
		{
			// 検証ルールに合わない場合は、該当モデルにエラー情報を追加します。
			var message = string.Format("モデル名に半角スペースが含まれています。モデル名: {0}", model.Name);
			var error = model.AddError("Name", "Error", "モデル命名規則チェック", message);
		}
	}

	/// <summary>
	/// エクステンションの初期化処理
	/// </summary>
	/// <param name="context">実行コンテキスト</param>
	/// <remarks>
	/// エクステンションの初期化処理・終了処理が不要な場合も、空の `Activate`, `Deactivate` メソッドが必要です。
	/// </remarks>
	public void Activate(IContext context)
	{
		// 必要に応じてエクステンションの初期化処理などを実装します。
	}

	/// <summary>
	/// エクステンションの終了処理
	/// </summary>
	/// <param name="context">実行コンテキスト</param>
	/// <remarks>
	/// エクステンションの初期化処理・終了処理が不要な場合も、空の `Activate`, `Deactivate` メソッドが必要です。
	/// </remarks>
	public void Deactivate(IContext context)
	{
		// 必要に応じてエクステンションの終了処理などを実装します。
	}
}