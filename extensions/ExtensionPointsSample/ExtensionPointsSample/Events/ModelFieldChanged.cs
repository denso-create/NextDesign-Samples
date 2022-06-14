using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;

namespace ExtensionPointsSample.Events
{
    /// <summary>
    /// モデルフィールド変更後イベント
    /// </summary>
    internal class ModelFieldChanged : ModelsFieldChangedEventHandlerBase
    {
        /// <summary>
        /// イベントハンドラの処理です。
        /// </summary>
        /// <param name="c"></param>
        /// <param name="p"></param>
        protected override void OnHandle(IEventContext c, ModelFieldChangedEventParams p)
        {
            // イベント処理を実装します。
            Output.WriteLine(ExtensionName, $"Events: ModelsFieldChanged Event. :{p.Model.Name} - {p.Field}");

            // 情報ウィンドウをアクティブにします
            App.Window.IsInformationPaneVisible = true;
            App.Window.CurrentOutputCategory = ExtensionName;
            App.Window.ActiveInfoWindow = "Output";
        }
    }
}