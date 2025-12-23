using NextDesign.Core;
using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using RestrictNamesUnique;
using System.Linq;

namespace RestrictNamesUnique.Events
{
    /// <summary>
    /// モデルフィールド変更イベントハンドラ
    /// </summary>
    public class ModelsFieldChangedEvent : ModelsFieldChangedEventHandlerBase
    {
        /// <summary>
        /// イベントハンドラの処理です。
        /// </summary>
        protected override void OnHandle(IEventContext c, ModelFieldChangedEventParams p)
        {
            var model = p.Model;
            
            // 共通ルールで重複チェック（対象外の場合は false を返す）
            if (NameUniquenessRules.HasDuplicateName(model, out var owner, out var ownerField))
            {
                // エラーメッセージを表示
                var message = NameUniquenessRules.CreateDuplicateNameMessage(model, ownerField);
                App.Window.UI.ShowMessageBox(message, "エラー");

                // 変更をキャンセル
                p.Cancel();
            }
            else
            {
                // 以前のエラーをクリア
                App.Errors.RemoveErrors(App.Errors.FindErrorOfModelByCategory(model, NameUniquenessRules.c_ErrorCategory_RestrictNamesUnique));
            }
        }
    }
}
