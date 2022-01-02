using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;
using System.Linq;
using NextDesign.Core;
using NextDesign.Desktop;
using NextDesign.Desktop.CustomUI;

namespace CustomUISample.ViewModel.Navigator
{
    public class CustomNavigatorViewModel : ICustomNavigator, IDisposable
    {
		#region プロパティ
		/// <summary>
		/// タイプ記述子
		/// </summary>
		public ICustomDescriptor Descriptor { get; set; }

		/// <summary>
		/// 選択しているアイテム
		/// </summary>
		private object m_SelectedItem;

		/// <summary>
		/// 選択しているアイテム
		/// </summary>
		public object SelectedItem
		{
			get => m_SelectedItem;
			set
			{
				m_SelectedItem = value;

				// 選択しているアイテムが、Modelの場合は
				// 現在のワークスペースのカレントモデルとインスペクト対象の要素を設定します。
				if (m_SelectedItem is IModel model)
				{
					Workspace.State.SetCurrentModel(model); ;
					Workspace.State.SetInspectedObject(model); ;
				}
			}
		}

		/// <summary>
		/// エディタで選択された要素の列挙
		/// 選択された要素がない場合は、空の列挙を返すように実装してください。
		/// </summary>
		public IEnumerable<object> SelectedItems => Enumerable.Empty<object>();

		/// <summary>
		/// ID
		/// </summary>

		/// <summary>
		/// アイテム
		/// </summary>
		private ObservableCollection<CustomNavigatorItemViewModel> m_Items;

		/// <summary>
		/// アイテム
		/// </summary>
		public IEnumerable<CustomNavigatorItemViewModel> Items => m_Items;

		/// <summary>
		/// ワークスペース
		/// </summary>
		private IWorkspace Workspace => m_App.Workspace;

		#endregion

		#region 内部フィールド

		/// <summary>
		/// コンフィグレーション
		/// </summary>
		private CustomNavigatorConfigs m_Configs;

		/// <summary>
		/// アプリケーション
		/// </summary>
		private NextDesign.Desktop.IApplication m_App;

		#endregion

		#region 構築・消滅

		/// <summary>
		/// 破棄
		/// </summary>
		public void Dispose()
		{
			DisposeItems();
			if (m_App != null)
			{
				m_App = null;
			}
		}

		/// <summary>
		/// アイテムをDisposeする
		/// </summary>
		public void DisposeItems()
		{
			if (m_Items == null)
			{
				return;
			}

			foreach (var item in m_Items)
			{
				item.Dispose();
			}

			m_Items.Clear();
			m_Items = null;
		}

		#endregion

		#region イベントハンドラ

		/// <summary>
		/// OnInitialized	"独自拡張するユーザインタフェースを初期化する際の処理
		/// Next Designは、独自拡張するユーザインタフェースを初期化する際にこのメソッドを呼び出します。
		/// 拡張側で初期化時に実行したい処理がある場合はここで実装します。"
		/// </summary>
		/// <param name="args"></param>
		public void OnInitialized(InitializedEventArgs args)
		{
			m_Configs = new CustomNavigatorConfigs();
			m_Configs.SelectionMode = SelectionMode.Multiple;
		}

		/// <summary>
		/// 独自拡張するユーザインタフェースを破棄する前の処理
		/// Next Designは、独自拡張するユーザインタフェースを破棄する前にこのメソッドを呼び出します。
		/// 拡張側で破棄前に実行したい処理がある場合はここで実装します。
		/// </summary>
		/// <param name="args"></param>
		public void OnBeforeDispose(BeforeDisposeEventArgs args)
		{
			// 処理なし
		}

		/// <summary>
		/// このナビゲータを表示する際の処理
		/// Next Designは、独自拡張するナビゲータを表示する際にこのメソッドを呼び出します。
		/// 拡張側で表示時に実行したい処理がある場合はここで実装します。
		/// </summary>
		/// <param name="args"></param>
		public void OnShow(OnShowEventArgs args)
		{
			m_App = args.App;
			var project = m_App.Workspace.CurrentProject;
			CreateChildren(project);
		}

		/// <summary>
		/// このナビゲータを非表示にする際の処理
		/// Next Designは、独自拡張するナビゲータを隠す際にこのメソッドを呼び出します。
		/// 拡張側で非表示時に実行したい処理がある場合はここで実装します。
		/// </summary>
		/// <param name="args"></param>
		public void OnHide(OnHideEventArgs args)
		{
			// 処理なし
		}

		#endregion

		#region 内部処理

		/// <summary>
		/// 子要素を生成
		/// </summary>
		/// <param name="project"></param>
		private void CreateChildren(IProject project)
		{
			if (project == null)
			{
				return;
			}

			// モデルの子要素を取得し、ナビゲータの子要素を生成します
			var models = project.GetChildren().OfType<IModel>();
			var items = new ObservableCollection<CustomNavigatorItemViewModel>();
			foreach (var model in models)
			{
				var item = new CustomNavigatorItemViewModel(model, this);
				items.Add(item);
			}

			m_Items = items;
		}

		/// <summary>
		/// アイコンを取得する
		/// </summary>
		/// <param name="model"></param>
		/// <returns></returns>
		internal object GetIcon(IModel model)
		{
			if (m_App == null)
			{
				return null;
			}

			if (model == null)
			{
				return null;
			}

			var icon = m_App.Resources.GetObjectIcon(model);
			return icon;
		}

		#endregion
	}
}

