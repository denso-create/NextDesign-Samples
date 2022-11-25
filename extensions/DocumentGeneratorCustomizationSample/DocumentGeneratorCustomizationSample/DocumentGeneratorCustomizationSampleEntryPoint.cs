using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using NextDesign.Desktop;
using NextDesign.Desktop.DocumentGenerator;
using NextDesign.Desktop.DocumentGenerator.Word;
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
                config.RegisterAfterContentsGeneration(OnAfterContentsGeneration);
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
        /// ドキュメントの全コンテンツ生成後のコールバック関数です。
        /// </summary>
        /// <param name="p">ドキュメントの全コンテンツ生成後パラメータ</param>
        private void OnAfterContentsGeneration(IAfterContentsGenerationParams p)
        {
            // 対象コンテンツがページの場合のみ処理する
            var pageContents = p.DocumentContent.GetAllContents().OfType<IPageContent>();
            foreach (var pageContent in pageContents)
            {
                // ドキュメントフォームのビューに対してのみ、未設定項目の除去処理を実施
                var formViews = pageContent.Views.Where(v => v.Editor?.EditorType == "DocumentForm");
                foreach (var view in formViews)
                {
                    RemoveEmptyItems(view.Items);
                }
            }
        }

        /// <summary>
        /// ビュー上の未設定項目を除去します。
        /// </summary>
        /// <param name="items">コンテンツ要素</param>
        private void RemoveEmptyItems(IList<IViewItemContent> items)
        {
            // 未設定項目を探索して除去する
            var removeItems = new ObservableCollection<IViewItemContent>();
            foreach (var item in items)
            {
                switch (item.Control.ContentType)
                {
                    case DocumentContentTypes.Text:
                    case DocumentContentTypes.RichText:
                        // テキスト、リッチテキストは、未設定の場合、項目を削除する
                        var ctl = item.Control as IValueContent;
                        if (String.IsNullOrEmpty(ctl.Text))
                        {
                            removeItems.Add(item);
                        }
                        break;

                    case DocumentContentTypes.Table:
                    case DocumentContentTypes.List:
                        // グリッド、リストは、子要素がない場合、項目を削除する
                        if (item.Control.ViewItem.Items.Count == 0)
                        {
                            removeItems.Add(item);
                        }
                        break;

                    default:
                        break;
                }
            }

            // 上記で走査した未設定項目を削除する
            foreach (var item in removeItems)
            {
                items.Remove(item);
            }

            // グループ化された要素、リスト要素に対しては、再帰的に未設定項目の除去処理を実施する
            var nestedItems = items.Where(i => 
                i.Control.ContentType == DocumentContentTypes.Group ||
                i.Control.ContentType == DocumentContentTypes.List ||
                i.Control.ContentType == DocumentContentTypes.ListItem
            );
            foreach (var item in nestedItems)
            {
                RemoveEmptyItems(item.Items);
            }
        }

        #endregion
    }
}
