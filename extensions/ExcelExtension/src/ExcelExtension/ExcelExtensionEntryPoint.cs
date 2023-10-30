using NextDesign.Desktop;
using NextDesign.Extension;
using NextDesign.Core;
using System;
using System.Windows;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace ExcelExtension
{
    /// <summary>
    /// エクステンションのエントリポイントです
    /// </summary>
    public class ExcelExtensionEntryPoint : IExtension
    {
        /// <summary>
        /// アプリケーション
        /// </summary>
        private IApplication App { get; set; }

        #region Activate/Deactivate

        /// <summary>
        /// エクステンションの初期化時の処理です。
        /// </summary>
        /// <param name="context">エクステンションのコンテキストです。</param>
        public void Activate(IContext context)
        {
            App = context.App;
        }

        /// <summary>
        /// エクステンションの終了前の処理です。
        /// </summary>
        /// <param name="context">エクステンションのコンテキストです。</param>
        public void Deactivate(IContext context)
        {
            // Nothing
        }

        #endregion


        #region Commands

        /// <summary>
        /// Excelインポートボタンの処理を実行する。
        /// </summary>
        public void Import(ICommandContext context, ICommandParams parameters)
        {
            try
            {
                // ---------------------------------------------------
                // インポート先が「ソフト構造」であることをチェックします。
                // ---------------------------------------------------
                var targetModel = App.Window.EditorPage.CurrentModel;
                if (!targetModel.ClassName.Equals("SoftwareStructureModel"))
                {
                    App.Window.UI.ShowInformationDialog(
                        "ソフト構造モデルを表示させてから実行してください。",
                        "Excel Extension"
                    );
                    return;
                }

                // ---------------------------------------------------
                // Excel ファイルを選択します。
                // ---------------------------------------------------
                var filter = "Excel Files (*.xls, *.xlsx)|*.xls;*.xlsx";
                var filePath = App.Window.UI.ShowOpenFileDialog(filter: filter);
                if (string.IsNullOrEmpty(filePath))
                {
                    return;
                }

                // ---------------------------------------------------
                // Excel ファイルからデータを読み込みます。
                // ---------------------------------------------------
                var excelHandler = new ExcelHandler();
                var softwareStructureDto = excelHandler.Read(filePath);

                // ---------------------------------------------------
                // 読み込んだデータを Next Design に書き込みます。
                // ---------------------------------------------------
                var modelBuilder = new SoftwareStructureModelHandler();
                foreach (var child in softwareStructureDto.Children)
                {
                    modelBuilder.AddStructuredModel(targetModel, softwareStructureDto.ChildrenFieldName, child);
                }

                // ---------------------------------------------------
                // 完了メッセージを表示します。
                // ---------------------------------------------------
                App.Window.UI.ShowInformationDialog(
                    "Excel ファイルをインポートしました。",
                    "Excel Extension"
                );
            }
            catch (System.Exception ex)
            {
                ShowOutputPane();
                App.Output.WriteLine("デフォルト", ex.Message);
            }
        }

        /// <summary>
        /// Excelエクスポートボタンの処理を実行する。
        /// </summary>
        public void Export(ICommandContext context, ICommandParams parameters)
        {
            try
            {
                // ---------------------------------------------------
                // エクスポート対象が「ソフト構造」であることをチェックします。
                // ---------------------------------------------------
                var targetModel = App.Window.EditorPage.CurrentModel;
                if (!targetModel.ClassName.Equals("SoftwareStructureModel"))
                {
                    App.Window.UI.ShowInformationDialog(
                        "ソフト構造モデルを表示させてから実行してください。",
                        "Excel Extension"
                    );
                    return;
                }

                // ---------------------------------------------------
                // Excel ファイルを選択します。
                // ---------------------------------------------------
                var filter = "Excel Files (*.xlsx)|*.xlsx";
                var filePath = App.Window.UI.ShowSaveFileDialog(filter: filter);
                if (string.IsNullOrEmpty(filePath))
                {
                    return;
                }

                // ---------------------------------------------------
                // ソフト構造のモデルから出力データを読み込みます。
                // ---------------------------------------------------
                var modelBuilder = new SoftwareStructureModelHandler();
                var dto = modelBuilder.FetchStructuredModel(targetModel);

                // ---------------------------------------------------
                // 読み込んだデータを Excel ファイルに書き込みます。
                // ---------------------------------------------------
                var excelHandler = new ExcelHandler();
                excelHandler.Write(filePath, dto);

                // ---------------------------------------------------
                // 完了メッセージを表示します。
                // ---------------------------------------------------
                App.Window.UI.ShowInformationDialog(
                    "Excel ファイルにエクスポートしました。",
                    "Excel Extension"
                );
            }
            catch (System.Exception ex)
            {
                ShowOutputPane();
                App.Output.WriteLine("デフォルト", ex.Message);
            }
        }

        #endregion

        #region Private methods

        /// <summary>
        /// 情報ウィンドウを表示する。
        /// </summary>
        private void ShowOutputPane()
        {
            App.Window.IsInformationPaneVisible = true;
            App.Window.ActiveInfoWindow = "Output";
        }

        #endregion
    }
}
