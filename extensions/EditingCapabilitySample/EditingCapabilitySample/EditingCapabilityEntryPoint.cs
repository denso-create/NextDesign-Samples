using NextDesign.Core;
using NextDesign.Desktop;
using NextDesign.Extension;

namespace EditingCapability
{
	/// <summary>
	/// モデル編集操作時の動的制約のエクステンションエントリポイントです
	/// </summary>
	public class EditingCapabilityEntryPoint : IExtension
	{
		/// <summary>
		/// エクステンションを活性化します
		/// </summary>
		/// <param name="context">実行コンテキスト</param>
		public void Activate(IContext context)
		{
			// 動的制約を登録します。
			var registry = context.App.Workspace.CurrentProject.EditingCapabilityProviderRegistry;
			registry.Register(new ModelReferenceProvider(context));
			registry.Register(new ModelCreationProvider());
		}

		/// <summary>
		/// エクステンションを非活性化します
		/// </summary>
		/// <param name="context">実行コンテキスト</param>
		public void Deactivate(IContext context)
		{
			// 制約の解除は不要です。
		}
	}
}
