using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using System;
using System.Text;
using System.Windows.Threading;

namespace IprojMigrationTool.Commands
{
    internal static class CommandHandlerBaseExtension
    {
        internal static void ShowOutputMessage(this CommandHandlerBase c, string message)
        {
            OutputMessage(c, message);

            // メッセージボックス表示
            c.App.Window.UI.ShowMessageBox(message, c.ExtensionName);

            // 出力ウィンドウの表示を強制（他エクステンション切替対策）
            c.App.Window.CurrentOutputCategory = c.ExtensionName;
        }

        internal static void OutputMessage(this CommandHandlerBase c, string message)
        {
            c.Output.WriteLine(c.ExtensionName, message);

            // 出力ウィンドウを表示
            c.App.Window.IsInformationPaneVisible = true;
            c.App.Window.CurrentOutputCategory = c.ExtensionName;
            c.App.Window.ActiveInfoWindow = "Output";

            // スクロール
            c.App.Window.CurrentInfoView.ScrollToBottom();

            // 画面表示を更新
            DoEvents();
        }
        
        internal static void DoEvents()
        {
            var frame = new DispatcherFrame();

            var callback = new DispatcherOperationCallback(obj =>
            {
                ((DispatcherFrame)obj).Continue = false;
                return null;
            });

            Dispatcher.CurrentDispatcher.BeginInvoke(DispatcherPriority.Background, callback, frame);
            Dispatcher.PushFrame(frame);
        }
    }
}
