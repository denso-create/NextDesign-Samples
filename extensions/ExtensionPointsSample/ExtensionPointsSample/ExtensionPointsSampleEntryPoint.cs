using ExtensionPointsSample.Commands;
using ExtensionPointsSample.Events;
using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using NextDesign.Extension;
using System;
using System.Windows;

namespace ExtensionPointsSample
{
    /// <summary>
    /// エクステンションのエントリポイントです
    /// </summary>
    public class ExtensionPointsSampleEntryPoint : ExtensionBase
    {
        /// <summary>
        /// アクティベート時の処理です。
        /// </summary>
        protected override void OnActivate()
        {
            // リボン
            ExtensionPoints.Ribbon.AddTab("ExtensionPointsSample").AddGroup("Group1").AddLargeButton<HelloCommand>("Hello world");

            // イベント
            ExtensionPoints.Events.Application.RegisterOnAfterStart<ApplicationAfterStart>();
        }
    }
}
