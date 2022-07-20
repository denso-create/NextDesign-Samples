using ArchitectureSample.Core;
using ArchitectureSample.Core.Services;
using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using System;
using System.Collections.Generic;
using System.Text;
using System.Windows;

namespace ArchitectureSample.Commands
{
    /// <summary>
    /// ユースケースを作成します
    /// </summary>
    public class CreateUseCasesCommand : CommandHandlerBase
    {
        /// <summary>
        /// コマンドの実行
        /// </summary>
        /// <param name="c"></param>
        /// <param name="p"></param>
        protected override void OnExecute(ICommandContext c, ICommandParams p)
        {
            // ファクトリからサービスを取得します
            var service = SampleServiceFactory.Get<IUseCaseCreationService>();

            // サービスを呼び出します
            service.CreateUseCases(CurrentModel, new[] { "ユースケース1", "ユースケース2", "ユースケース2" });

            UI.ShowMessageBox("ユースケースを作成しました。", ExtensionName);
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
