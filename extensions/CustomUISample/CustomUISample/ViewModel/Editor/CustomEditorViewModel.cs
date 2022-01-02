using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;
using NextDesign.Core;
using NextDesign.Desktop;
using NextDesign.Desktop.CustomUI;
using NextDesign.Extension;

namespace CustomUISample.ViewModel.Editor
{
	class CustomEditorViewModel : ICustomEditorView
	{
		#region タイプ記述子

		/// <summary>
		/// タイプ記述子
		/// </summary>
		private static CustomEditorDefinitionDescriptor s_DefinitionDescriptor;

		/// <summary>
		/// タイプ記述子
		/// </summary>
		public static CustomEditorDefinitionDescriptor DefinitionDescriptor
		{
			get
			{
				return s_DefinitionDescriptor ?? (s_DefinitionDescriptor = new CustomEditorDefinitionDescriptor
				{
					// カスタムエディタの種類識別子
					CustomEditorTypeId = "CustomUI.Test",
					// アクセスキー
					AccessKey = "P",
					// 表示名
					DisplayName = "カスタムエディタ",
					// グループ名
					GroupName = "カスタムエディタ",
					// アイコン（大）pack - uri 形式の文字列、または Stream 型を指定できます。
					LargeIcon =
						"pack://application:,,,/CustomUISample;component/Resources/Images/TestEditor32.png",
					// アイコン（小）pack - uri 形式の文字列、または Stream 型を指定できます。
					SmallIcon =
						"pack://application:,,,/CustomUISample;component/Resources/Images/TestEditor16.png"
				});
			}
		}

		#endregion

		#region プロパティ

		/// <summary>
		/// タイプ記述子
		/// </summary>
		public ICustomDescriptor Descriptor { get; set; }

		/// <summary>
		/// 対応するビュー定義のId
		/// </summary>
		public string ViewDefinitionId => Editor?.EditorDefinition.Id;

		/// <summary>
		/// エディタで選択された要素
		/// 選択された要素がない場合は、null を返すように実装してください。
		/// </summary>
		public object SelectedItem => null;

		/// <summary>
		/// エディタで選択された要素の列挙
		/// 選択された要素がない場合は、空の列挙を返すように実装してください。
		/// </summary>
		public IEnumerable<object> SelectedItems => Enumerable.Empty<object>();

		/// <summary>
		/// アプリケーション
		/// </summary>
		public IApplication App { get; private set; }

		/// <summary>
		/// エクステンション
		/// </summary>
		public CustomUISampleEntryPoint Extension { get; private set; }

		/// <summary>
		/// エディタ情報
		/// </summary>
		public ICustomEditor Editor { get; private set; }

		/// <summary>
		/// 対象モデル
		/// </summary>
		public IModel TargetModel { get; private set; }

		#endregion

		#region イベントハンドラ

		/// <summary>
		/// 独自拡張するユーザインタフェースを初期化する際の処理
		/// Next Designは、独自拡張するユーザインタフェースを初期化する際にこのメソッドを呼び出します。
		/// 拡張側で初期化時に実行したい処理がある場合はここで実装します。
		/// </summary>
		/// <param name="args"></param>
		public void OnInitialized(InitializedEventArgs args)
		{
			// アプリケーションとエクステンションの情報を記憶します
			App = args.App;
			Extension = args.Extension as CustomUISampleEntryPoint;
		}


		/// <summary>
		/// 独自拡張するユーザインタフェースを破棄する前の処理
		/// Next Designは、独自拡張するユーザインタフェースを破棄する前にこのメソッドを呼び出します。
		/// 拡張側で破棄前に実行したい処理がある場合はここで実装します。
		/// </summary>
		/// <param name="args"></param>
		public void OnBeforeDispose(BeforeDisposeEventArgs args)
		{
			// 破棄する前の処理なし
		}


		#endregion

		#region インターフェース実装

		/// <summary>
		/// このエディタの表示対象のモデルを設定します。
		/// </summary>
		/// <param name="model"></param>
		public void SetModel(ICustomEditor model)
		{
			Editor = model;
			TargetModel = model.Model;
		}

		/// <summary>
		/// ドキュメント出力するコンテンツの内容を取得します。
		/// </summary>
		/// <param name="context"></param>
		public ICustomEditorDocumentContent GetDocumentContent(ICustomEditorDocumentGenerationContext context)
        {
			// 現行バージョンでは、null 固定とします
			return null;
		}

		#endregion
	}
}
