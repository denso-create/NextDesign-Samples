using ExtensionPointsSample.Commands;
using ExtensionPointsSample.Events;
using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using NextDesign.Extension;
using System;
using System.Windows;
using System.Windows.Input;

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
            // タブ
            var tab = ExtensionPoints.Ribbon.AddTab("ExtensionPointsSample");
            tab.SetOrderBefore(RibbonTabs.View);

            // グループ
            var group0 = tab.AddGroup("Button");
            var group1 = tab.AddGroup("StackPanel");
            var group2 = tab.AddGroup("ButtonGroup");
            var group3 = tab.AddGroup("Menu");
            var group4 = tab.AddGroup("SplitMenu");
            var group5 = tab.AddGroup("AddModel");

            // ボタン(大)
            group0.AddLargeButton<HelloCommand>("Large Button", "Resources/About.png");
            group5.AddLargeButton<AddSampleModelCommand>("Add SampleModel", "Resources/About.png");

            // スタックパネル
            var stackPanel = group1.AddStackPanel();
            stackPanel.AddSmallButton<HelloCommand>("smallbutton", "Resources/About.png"); // ボタン
            stackPanel.AddCheckBox<CheckParamCommand>("checkbox", "MyProperty", true); // チェックボックス

            // ボタングループ
            var buttonGroup = group2.AddButtonGroup();
            buttonGroup.AddSmallButton<HelloCommand>("button1", "Resources/About.png"); // ボタン
            buttonGroup.AddSmallButton<HelloCommand>("button2", "Resources/About.png"); // ボタン

            // メニュー
            var menu = group3.AddMenu("Menu", "Resources/About.png");
            menu.AddSmallButton<HelloCommand>("smallbutton", "Resources/About.png"); // ボタン

            // スプリットボタン
            var splitButton = group4.AddSplitButton<HelloCommand>("Split Button", "Resources/About.png");
            var spl_menu = splitButton.AddMenu();
            spl_menu.AddSmallButton<HelloCommand>("smallbutton", "Resources/About.png"); // ボタン

            // イベント
            ExtensionPoints.Events.Application.RegisterOnAfterStart<UserBaseModel>();
            ExtensionPoints.Events.AddModelEvent().RegisterOnFieldChanged<ModelFieldChanged>();

            // ショートカットキーの登録
            ExtensionPoints.ShortcutKeyCommands.Register<HelloCommand>(Key.I, ModifierKeys.Control);
        }

        /// <summary>
        /// <summary>
        /// ディアクティベート時の処理です。
        /// </summary>
        /// </summary>
        protected override void OnDeactivate()
        {

        }
    }
}
