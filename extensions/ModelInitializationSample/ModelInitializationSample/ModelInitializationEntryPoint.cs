// エクステンション開発で参照するAPIの名前空間の宣言
using NextDesign.Extension;
using NextDesign.Core;
using NextDesign.Desktop;

namespace ModelInitializationSample
{
	/// <summary>
	/// モデル追加時の初期化処理のエクステンションエントリポイント。
	/// </summary>
	public class ModelInitializationEntryPoint : IExtension
	{
		/// <summary>
		/// エクステンションを活性化する。
		/// </summary>
		/// <param name="context">実行コンテキスト</param>
		public void Activate(IContext context)
		{
			// 初期化処理を登録します。
			var registry = context.App.Workspace.CurrentProject.EditingCapabilityProviderRegistry;
			registry.Register(new ModelInitializationProvider());
		}

		/// <summary>
		/// エクステンションを非活性化する。
		/// </summary>
		/// <param name="context">実行コンテキスト</param>
		public void Deactivate(IContext context)
		{
			// 制約の解除は不要です。
		}
	}
}
