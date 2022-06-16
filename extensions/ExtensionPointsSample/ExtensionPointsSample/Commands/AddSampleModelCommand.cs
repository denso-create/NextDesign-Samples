using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using System;
using System.Collections.Generic;
using System.Text;
using System.Windows;
using ExtensionPointsSample.Models;

namespace ExtensionPointsSample.Commands
{
    /// <summary>
    /// SampleModelの追加 コマンドの実装です。
    /// </summary>
    public class AddSampleModelCommand : CommandHandlerBase
    {
        /// <summary>
        /// コマンドの実行
        /// </summary>
        /// <param name="c"></param>
        /// <param name="p"></param>
        protected override void OnExecute(ICommandContext c, ICommandParams p)
        {
            var m = CurrentModel.AddNewModel("SampleModel", "SampleModel");
            var useCaseModel = new SampleModel(m);

            // フィールドを設定します
            useCaseModel.Initialize();
        }

        /// <summary>
        /// コマンド実行可否の実装（任意です）
        /// </summary>
        /// <returns></returns>
        protected override bool OnCanExecute()
        {
            return CurrentModel?.ClassName == "Packages";
        }
    }
}
