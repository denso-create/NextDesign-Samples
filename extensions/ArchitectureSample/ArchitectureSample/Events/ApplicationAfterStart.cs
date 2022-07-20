using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;

namespace ArchitectureSample.Events
{
    /// <summary>
    /// アプリケーション実行イベント
    /// </summary>
    internal class ApplicationAfterStart : ApplicationAfterStartEventHandlerBase
    {
        /// <summary>
        /// イベントハンドラの処理です。
        /// </summary>
        /// <param name="c"></param>
        /// <param name="p"></param>
        protected override void OnHandle(IEventContext c, AfterStartEventParams p)
        {
            // イベント処理を実装します。
            Output.WriteLine(ExtensionName, $"Events: ApplicationAfterStart Event. Version: {App.Version}");

            // アクティブにします
            App.Window.IsInformationPaneVisible = true;
            App.Window.CurrentOutputCategory = ExtensionName;
            App.Window.ActiveInfoWindow = "Output";
        }
    }
}