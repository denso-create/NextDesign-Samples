using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;
using NextDesign.Core;
using NextDesign.Desktop.CustomUI;

namespace CustomUISample.ViewModel.Inspector
{
	class CustomInspectorViewModel : ICustomInspector
	{
		#region フィールド

		/// <summary>
		/// ターゲットモデル
		/// </summary>
		private object m_Object;

		#endregion

		#region プロパティ

		/// <summary>
		/// タイプ記述子
		/// </summary>
		public ICustomDescriptor Descriptor { get; set; }

		/// <summary>
		/// 名前
		/// </summary>
		public string Name
		{
			get
			{
				if (m_Object is IModel model)
				{
					return $"{model.Name}({model.GetType().Name})";
				}
				return m_Object?.GetType().Name;
			}
		}

		#endregion

		#region イベントハンドラ

		/// <summary>
		/// 初期化
		/// </summary>
		/// <param name="args">イベントパラメータ</param>
		public void OnInitialized(InitializedEventArgs args)
		{
			// 独自拡張するユーザインタフェースを初期化する際の処理
			// Next Designは、独自拡張するユーザインタフェースを初期化する際にこのメソッドを呼び出します。
			// 拡張側で初期化時に実行したい処理がある場合はここで実装します。
		}

		/// <summary>
		/// 破棄
		/// </summary>
		/// <param name="args">イベントパラメータ</param>
		public void OnBeforeDispose(BeforeDisposeEventArgs args)
		{
			// 独自拡張するユーザインタフェースを破棄する前の処理
			// Next Designは、独自拡張するユーザインタフェースを破棄する前にこのメソッドを呼び出します。
			// 拡張側で破棄前に実行したい処理がある場合はここで実装します。
		}

		/// <summary>
		/// このインスペクタの表示対象のモデルを設定します。
		/// </summary>
		/// <param name="target">ターゲットのモデル</param>
		/// <param name="targets">ターゲットのモデル群</param>
		public void SetModel(object target, IEnumerable<object> targets)
		{
			m_Object = target;
		}

		#endregion
	}
}

