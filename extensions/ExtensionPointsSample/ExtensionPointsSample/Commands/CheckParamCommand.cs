using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using System;
using System.Collections.Generic;
using System.Text;
using System.Windows;

namespace ExtensionPointsSample.Commands
{
    /// <summary>
    /// CheckBoxのパラメータ確認 コマンドの実装です。
    /// </summary>
    public class CheckParamCommand : CommandHandlerBase
    {
        /// <summary>
        /// コマンドの実行
        /// </summary>
        /// <param name="c"></param>
        /// <param name="p"></param>
        protected override void OnExecute(ICommandContext c, ICommandParams p)
        {
            var isChecked = c.GetProperty<bool>("MyProperty");
            UI.ShowMessageBox($"Checked: {isChecked.ToString()}", ExtensionName);
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
