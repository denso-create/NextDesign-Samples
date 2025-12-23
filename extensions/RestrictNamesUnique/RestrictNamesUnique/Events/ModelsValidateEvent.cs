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
            // onValidate は全モデルに対して発火するため、
            // ここでは対象モデル自身のみを検証します。
            var model = p.Model;
            var app = c.App;

            // 対象モデルに対する以前のエラーをクリアします。
            app.Errors.ClearErrorsAt(model);

            if (NameUniquenessRules.HasDuplicateName(model, out var owner, out var ownerField))
            {
                var message = NameUniquenessRules.CreateDuplicateNameMessage(model, ownerField);
                model.AddError("Name", "Error", "RestrictNamesUnique", message);
            }
        }
    }
}
