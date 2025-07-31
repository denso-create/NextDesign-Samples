using NextDesign.Cli.ExtensionFramework;
using DensoCreate.Cli.Framework;

namespace HelloWorldCliExtensionSample
{
	public class HelloWorldCliExtensionSample : ExtensionBase
	{
		/// <summary>
		/// コンストラクタです
		/// </summary>
		public HelloWorldCliExtensionSample(): base("HelloWorldCliExtensionSample")
		{
		}
	}

	/// <summary>
	/// HelloWorld コマンドを実装します
	/// </summary>
	public class HelloWorld : Command
	{
		/// <summary>
		/// コンストラクタ
		/// </summary>
		public HelloWorld() : base("HelloWorld", "'Hello World'を出力します")
		{
			RegisterHandler(nameof(OnExecute));
		}

		/// <summary>
		/// ハンドラ実行
		/// </summary>
		private void OnExecute()
		{
			Console.WriteLine("'Hello World'");
		}
	}
}
