using NextDesign.Core;
using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using RestrictNamesUnique;
using System.Linq;

namespace RestrictNamesUnique.Events
{
    /// <summary>
    /// モデル検証イベントハンドラ（onValidate）
    /// </summary>
    public class ModelsValidateEvent : ModelsValidateEventHandlerBase
    {
        /// <summary>
        /// イベントハンドラの処理です。
        /// イベント対象モデルに対して名前の重複チェックを行います。
        /// </summary>
        protected override void OnHandle(IEventContext c, ModelOnValidateEventParams p)
        {
            // onValidate はモデルごとに発火するため、
            // ここでは対象モデル自身のみを検証します。
            var model = p.Model;

            // 対象モデルに対する以前のエラーをクリアします。
            App.Errors.RemoveErrors(App.Errors.FindErrorOfModelByCategory(model, NameUniquenessRules.c_ErrorCategory_RestrictNamesUnique));

            if (NameUniquenessRules.HasDuplicateName(model, out var owner, out var ownerField))
            {
                var message = NameUniquenessRules.CreateDuplicateNameMessage(model, ownerField);
                var error = model.AddError("Name", "Error", "RestrictNamesUnique", message);
                error.Category = NameUniquenessRules.c_ErrorCategory_RestrictNamesUnique;
            }
        }
    }
}
