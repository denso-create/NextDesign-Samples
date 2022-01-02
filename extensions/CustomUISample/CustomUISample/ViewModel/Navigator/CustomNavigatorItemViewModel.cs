using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;
using System.Linq;
using NextDesign.Core;

namespace CustomUISample.ViewModel.Navigator
{
	/// <summary>
	/// サンプルナビゲータのアイテムVM
	/// </summary>
	public class CustomNavigatorItemViewModel : IDisposable
	{
		#region 内部フィールド

		/// <summary>
		/// 子要素
		/// </summary>
		private ObservableCollection<CustomNavigatorItemViewModel> m_Children;

		/// <summary>
		/// モデル
		/// </summary>
		private IModel m_Model;

		/// <summary>
		/// オーナー
		/// </summary>
		private CustomNavigatorViewModel m_Owner;

		#endregion

		#region プロパティ

		/// <summary>
		/// モデル
		/// </summary>
		public IModel Model => m_Model;

		/// <summary>
		/// 子要素
		/// </summary>
		public IEnumerable<CustomNavigatorItemViewModel> Children => m_Children;

		/// <summary>
		/// アイコン
		/// </summary>
		public object Icon => m_Owner?.GetIcon(Model);

		#endregion

		#region 構築・消滅

		/// <summary>
		/// コンストラクタ
		/// </summary>
		public CustomNavigatorItemViewModel(IModel model, CustomNavigatorViewModel owner)
		{
			m_Model = model;
			m_Owner = owner;

			CreateChildren();
		}

		/// <summary>
		/// 破棄
		/// </summary>
		public void Dispose()
		{
			if (m_Model != null)
			{
				m_Model = null;
			}

			if (m_Children != null)
			{
				foreach (var child in m_Children)
				{
					child.Dispose();
				}

				m_Children.Clear();
				m_Children = null;
			}
		}

		#endregion

		#region 内部処理

		/// <summary>
		/// 子要素の生成
		/// </summary>
		private void CreateChildren()
		{
			var children = m_Model.GetChildren().OfType<IModel>();
			if (!children.Any())
			{
				return;
			}

			if (m_Children == null)
			{
				m_Children = new ObservableCollection<CustomNavigatorItemViewModel>();
			}

			foreach (var child in children)
			{
				var item = new CustomNavigatorItemViewModel(child, m_Owner);
				m_Children.Add(item);
			}
		}

		#endregion
	}
}
