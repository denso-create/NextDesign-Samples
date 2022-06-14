using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using System;
using System.Collections.Generic;
using System.Text;
using System.Windows;

namespace ExtensionPointsSample.Commands
{
    /// <summary>
    /// Hello コマンドの実装です。
    /// </summary>
    public class HelloCommand : CommandHandlerBase
    {
        /// <summary>
        /// コマンドの実行
        /// </summary>
        /// <param name="c"></param>
        /// <param name="p"></param>
        protected override void OnExecute(ICommandContext c, ICommandParams p)
        {
            UI.ShowMessageBox("Hello world", ExtensionName);
        }

        /// <summary>
        /// コマンド実行可否の実装（任意です）
        /// </summary>
        /// <returns></returns>
        protected override bool OnCanExecute()
        {
            return true;
        }
    }
}
