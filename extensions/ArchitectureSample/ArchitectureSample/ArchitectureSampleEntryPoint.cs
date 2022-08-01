using ArchitectureSample.Commands;
using ArchitectureSample.Core;
using ArchitectureSample.Events;
using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using NextDesign.Extension;
using System;
using System.Windows;

namespace ArchitectureSample
{
    /// <summary>
    /// エクステンションのエントリポイントです
    /// </summary>
    public class ArchitectureSampleEntryPoint : ExtensionBase
    {
        /// <summary>
        /// アクティベート時の処理です。
        /// </summary>
        protected override void OnActivate()
        {
            // インターフェースの登録
            // テスト時はモックのインターフェースも登録できます
            SampleServiceFactory.InitializeDefaults();

            // リボン
            var tab = ExtensionPoints.Ribbon.AddTab("ArchitectureSample");
            var group = tab.AddGroup("作成");
            group.AddLargeButton<CreateUseCasesCommand>("ユースケースの作成");

            // イベント
            ExtensionPoints.Events.Application.RegisterOnAfterStart<ApplicationAfterStart>();
        }
    }
}
