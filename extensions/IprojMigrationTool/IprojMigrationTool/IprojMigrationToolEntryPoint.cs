using NextDesign.Desktop.ExtensionPoints;
using System;
using System.Windows;
using IprojMigrationTool.Properties;
using IprojMigrationTool.Commands;

namespace IprojMigrationTool
{
    /// <summary>
    /// エクステンションのエントリポイントです
    /// </summary>
    public class IprojMigrationToolEntryPoint : ExtensionBase
    {
        /// <summary>
        /// アクティベート時の処理です。
        /// </summary>
        protected override void OnActivate()
        {
            // リボン
            var ribonTabGroup = ExtensionPoints.Ribbon.AddTab(Messages.ExtensionRibbonTab).AddGroup(Messages.ExtensionRibbonGroup);
            ribonTabGroup.AddLargeButton<IProjMigrationCommand>(Messages.ExtensionIProjMigrationCommand, "./Resources/auto_renew-32.png");
            ribonTabGroup.AddLargeButton<PartialLoadMigrationCommand>(Messages.ExtensionPartialLoadMigrationCommand, "./Resources/playlist_add_check-32.png");
        }

        /// <summary>
        /// ディアクティベート時の処理です。
        /// </summary>
        protected override void OnDeactivate()
        {
        }
    }
}
