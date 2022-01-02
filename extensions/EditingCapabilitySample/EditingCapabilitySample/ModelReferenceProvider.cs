using System.Linq;
using NextDesign.Core;
using NextDesign.Core.EditingCapabilities;
using NextDesign.Desktop;

namespace EditingCapability
{
	/// <summary>
	/// モデルの関連付け機能をカスタマイズするプロバイダです
	/// </summary>
	public class ModelReferenceProvider : IModelReferenceProvider
	{
		/// <summary>
		/// コンテキスト。
		/// </summary>
		private IContext m_Context;

		#region 構築・消滅

		/// <summary>
		/// コンストラクタ。
		/// </summary>
		/// <param name="context">コンテキスト</param>
		public ModelReferenceProvider(IContext context)
		{
			m_Context = context;
		}

		#endregion

		/// <summary>
		/// モデル参照時の選択候補を取得します
		/// </summary>
		/// <param name="referableParams">選択候補を決めるためのパラメータ</param>
		/// <returns>選択候補の結果</returns>
		public ModelReferableResult GetReferences(ModelReferableParams referableParams)
		{
			var model = referableParams.Model;
			var modelMetaClass = model.Metaclass;
			var field = referableParams.Field;

			// 接続先ポートの候補を絞り込みます
			if (!IsPort(modelMetaClass))
			{
				// ポート以外は判定不要です
				return null;
			}

			if (field.Name != "ToPorts")
			{
				// 接続先ポート以外は判定不要です
				return null;
			}

			var result = CapabilityResults.Ignore;
			var models = Enumerable.Empty<IModel>();
			
			if (IsInputPort(modelMetaClass))
			{
				// 自身が入力ポートの場合、
				// 自身の親（コンポーネント）の子コンポーネントの入力ポートかつ名前にTBDを含まないものを候補にします
				result = CapabilityResults.Success;
				var metamodels = m_Context.App.Workspace.CurrentProject.Profile.Metamodels;
				var subSystems = model.Owner.GetChildren().Where(c => c.Metaclass.IsClassOf(metamodels.GetClass("SubSystem")));
				var inputPorts = subSystems.SelectMany(s => s.GetChildren().Where(c => (
					IsInputPort(c.Metaclass)
					&& (!c.Name.Contains("TBD"))
				)));
				models = inputPorts;
			}
			else if (IsOutputPort(modelMetaClass))
			{
				// 自身が出力ポートの場合、
				// 自身の親（コンポーネント）の親（コンポーネント）の子コンポーネント（機能のみ）の入力ポートと
				// 自身の親（コンポーネント）の親（コンポーネント）の出力ポートかつ名前にTBDを含まないものを候補にします
				result = CapabilityResults.Success;
				var metamodels = m_Context.App.Workspace.CurrentProject.Profile.Metamodels;
				var subSystems = model.Owner.Owner.GetChildren().Where(c => c.Metaclass.IsClassOf(metamodels.GetClass("SubSystem"))).ToList();
				var inputPorts = subSystems.SelectMany(s => s.GetChildren().Where(c => (
					IsInputPort(c.Metaclass)
					&& (!c.Name.Contains("TBD"))
					)));
				var outputPorts = model.Owner.Owner.GetChildren().Where(c => (
				    IsOutputPort(c.Metaclass)
					&& (!c.Name.Contains("TBD"))
					));
				models = inputPorts.Union(outputPorts);
			}

			var referenceResult = new ModelReferableResult
			{
				Result = result,
				Models = models
			};
			return referenceResult;
		}

		/// <summary>
		/// モデル関連付け可否を判定します
		/// </summary>
		/// <param name="relateParams">関連付け可否を決めるためのパラメータ</param>
		/// <returns>関連付け可否の結果</returns>
		public ModelRelateResult CanRelate(ModelRelateParams relateParams)
		{
			var model = relateParams.Model;
			var opposite = relateParams.OppositeModel;
			var modelMetaClass = model.Metaclass;
			var oppositeMetaClass = opposite.Metaclass;

			if (!IsPort(modelMetaClass) || !IsPort(oppositeMetaClass))
			{
				// ポート以外はNext Designの標準のままとするためnullを返します
				return null;
			}

			var result = CapabilityResults.Ignore;
			var canRelate = false;
			string guideText = null;
			// 「TBD」を名称に含むポートとは接続を制限します。
			if (opposite.Name.Contains("TBD"))
			{
				result = CapabilityResults.Success;
				canRelate = false;
				guideText = "TBDとは関連付けできません";
			}
			else
			{
				// TBD以外はNext Design標準の可否判定のままするためnullを返します。
				return null;
			}
			var relateResult = new ModelRelateResult
			{
				Result = result,
				CanRelate = canRelate,
				GuideText = guideText
			};

			return relateResult;
		}

		/// <summary>
		/// 対象のクラスがポートか判定します
		/// </summary>
		/// <param name="targetClass">対象のクラス</param>
		/// <returns>ポートの場合は真</returns>
		private bool IsPort(IClass targetClass)
		{
			var metamodels = m_Context.App.Workspace.CurrentProject.Profile.Metamodels;
			IClass systemStructurePortBase = metamodels.GetClass("SystemStructurePortBase");

			return targetClass.IsClassOf(systemStructurePortBase);
		}

		/// <summary>
		/// 対象のクラスが入力ポートか判定します
		/// </summary>
		/// <param name="targetClass">対象のクラス</param>
		/// <returns>ポートの場合は真</returns>
		private bool IsInputPort(IClass targetClass)
		{
			var metamodels = m_Context.App.Workspace.CurrentProject.Profile.Metamodels;
			IClass inputPort = metamodels.GetClass("FuntionFlowInputPortInnerSystem");

			return targetClass.IsClassOf(inputPort);
		}

		/// <summary>
		/// 対象のクラスが出力ポートか判定します
		/// </summary>
		/// <param name="targetClass">対象のクラス</param>
		/// <returns>ポートの場合は真</returns>
		private bool IsOutputPort(IClass targetClass)
		{
			var metamodels = m_Context.App.Workspace.CurrentProject.Profile.Metamodels;
			IClass outputPort = metamodels.GetClass("FuntionFlowOutputPortInnerSystem");

			return targetClass.IsClassOf(outputPort);
		}
	}
}
