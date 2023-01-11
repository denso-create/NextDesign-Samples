using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using NextDesign.Desktop;
using NextDesign.Desktop.DocumentGenerator;
using NextDesign.Desktop.DocumentGenerator.Word;
using NextDesign.Desktop.DocumentGenerator.Html;
using NextDesign.Extension;

namespace DocumentGeneratorCustomizationSample
{
    /// <summary>
    /// エクステンションのエントリポイントです
    /// </summary>
    public class DocumentGeneratorCustomizationSampleEntryPoint : IExtension
    {
        #region フィールド

        /// <summary>
        /// アプリケーション
        /// </summary>
        private IApplication App { get; set; }

        #endregion

        #region Activate/Deactivate

        /// <summary>
        /// エクステンションの初期化処理です。
        /// </summary>
        /// <param name="context">エクステンションのコンテキストです。</param>
        public void Activate(IContext context)
        {
            App = context.App;

            // ドキュメント生成のカスタマイズ機能のコンフィグ設定の登録
            App.DocumentGeneratorCustomization.RegisterConfig(this, (context) =>
            {
                var config = new DocumentGenerationConfigs();

                // オプション設定
                var option = config.GetWordOptions();
                option.OrderByViewDefinition = true; // ドキュメントの出力順に、ビューの定義順を設定
                option.AutoFitTables = AutoFitBehavior.AutoFitToWindow; // テーブルの列幅の自動調整方法に、ウィンドウサイズに合わせて自動調整を設定

                // コールバック処理の登録
                config.RegisterBeforeContentWrite(OnBeforeContentWrite);
                return config;
            });
        }

        /// <summary>
        /// エクステンションの終了処理です。
        /// </summary>
        /// <param name="context">エクステンションのコンテキストです。</param>
        public void Deactivate(IContext context)
        {
            // ドキュメント生成のカスタマイズ機能のコンフィグ設定の抹消
            App.DocumentGeneratorCustomization.UnregisterConfig(this);
        }

        #endregion

        #region 内部メソッド

        /// <summary>
        /// ドキュメントのコンテンツの書き込み開始時のコールバック関数です。
        /// "(未設定)" の項目を非表示（または "-"）に変更します。
        /// </summary>
        /// <param name="p">ドキュメントのコンテンツの書き込み開始時パラメータ</param>

        private void OnBeforeContentWrite(IBeforeContentWriteParams p)
        {
            switch (p.DocumentContent.ContentType)
            {
                case DocumentContentTypes.Text:
                case DocumentContentTypes.RichText:
                    var valueContent = p.DocumentContent as IValueContent;
                    if (valueContent != null && String.IsNullOrEmpty(valueContent.Text))
                    {
                        p.Skip = true;
                        //SetEmptyTextContent(valueContent);      // "(未設定)" を "-" に置き換える場合は上記行をコメントアウトしてこちらを使用
                    }
                    break;

                case DocumentContentTypes.Table:
                case DocumentContentTypes.List:
                    var formControlContent = p.DocumentContent as IFormControlContent;
                    if (formControlContent != null && formControlContent.ViewItem.Items.Count < 1)
                    {
                        p.Skip = true;
                        //WriteEmptyItemsContent(p.Writer, formControlContent);    // "(未設定)" を "-" に置き換える場合はこの行を有効化
                    }
                    break;

                default:
                    break;
            }

            return;
        }

        /// <summary>
        /// ドキュメントフォーム上の空の文字列型フィールドとリッチテキスト型フィールドに対して "-" を設定する
        /// </summary>
        /// <param name="content">ドキュメントフォーム上の対象項目</param>
        public void SetEmptyTextContent(IValueContent content)
        {
            content.Text = (content is IRichTextContent) ? "<html><body><p>-</p></body></html>" : "-";
        }

        /// <summary>
        /// ドキュメントフォーム上の空のリストとグリッドに対してタイトルと "-" を出力する
        /// </summary>
        /// <param name="writer">ドキュメントのWriter</param>
        /// <param name="content">ドキュメントフォーム上の対象項目</param>
        private void WriteEmptyItemsContent(IDocumentWriter writer, IFormControlContent content)
        {
            // 出力形式に応じて項目のタイトルと "-" を出力
            if (writer is IWordWriter)
            {
                var wordWriter = writer as IWordWriter;
                wordWriter.SetHeadingStyleByOutlineLevel(content.ViewItem.OutlineLevel);
                wordWriter.WriteLine(content.Title);
                wordWriter.SetBodyStyleByOutlineLevel(content.ViewItem.OutlineLevel);
                wordWriter.WriteLine("-");
            }
            else if (writer is IHtmlWriter)
            {
                var htmlWriter = writer as IHtmlWriter;
                htmlWriter.WriteLine($"<p class=\"title\">{content.Title}</p>");
                htmlWriter.WriteLine("<p>-</p>");
            }
        }

        #endregion
    }
}
