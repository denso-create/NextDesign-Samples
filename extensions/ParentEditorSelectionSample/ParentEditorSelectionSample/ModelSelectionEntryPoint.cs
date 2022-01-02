// エクステンション開発で参照するAPIの名前空間の宣言
using NextDesign.Extension;
using NextDesign.Core;
using NextDesign.Desktop;

namespace ParentEditorSelectionSample
{
    public class ModelSelectionEntryPoint : IExtension
    {
		/// <summary>
		/// エクステンションを活性化します
		/// </summary>
		public void Activate(IContext context)
		{
			// 表示するモデルの変更処理を登録します。
			var registry = context.App.Workspace.CurrentProject.EditingCapabilityProviderRegistry;
			registry.Register(new ParentEditorSelectionProvider());
		}

		/// <summary>
		/// エクステンションを非活性化します
		/// </summary>
		public void Deactivate(IContext context)
		{
			// 制約の解除は不要です。
		}
	}
}
