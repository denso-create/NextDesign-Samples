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
    public class ModelFieldChanged : ModelsFieldChangedEventHandlerBase
    {
        /// <summary>
        /// イベントハンドラの処理です。
        /// </summary>
        protected override void OnHandle(IEventContext c, ModelFieldChangedEventParams p)
        {
            var model = p.Model;
            var owner = model.Owner;

            // 親モデルが存在しない（ルートモデルなど）場合はチェックしない
            if (owner == null)
            {
                return;
            }

            // 自分が所属しているフィールド（所有関連）を取得
            var ownerField = model.GetOwnerField();
            if (ownerField == null)
            {
                return;
            }

            // 対象フィールドか判定（タグチェック）
            if (!IsTargetField(ownerField))
            {
                return;
            }

            // 現在の名前がデフォルト値と同じならチェックしない
            if (IsDefaultName(model))
            {
                return;
            }

            // 重複チェック
            if (HasDuplicateName(model, owner, ownerField))
            {
                // エラーメッセージを表示
                App.Window.UI.ShowMessageBox($"同じ名前のモデル '{model.Name}' がフィールド '{ownerField.DisplayName}' に既に存在します。", "エラー");

                // 変更をキャンセル
                p.Cancel();
            }
        }

        /// <summary>
        /// 重複チェック対象のフィールドかどうかを判定します。
        /// </summary>
        private bool IsTargetField(IField field)
        {
            var tagValue = field.GetTagValue(RestrictNamesUniqueEntryPoint.c_TagName_IsUniqueNameEnforced);
            if (string.IsNullOrEmpty(tagValue))
            {
                return false;
            }

            bool isEnforced;
            return bool.TryParse(tagValue, out isEnforced) && isEnforced;
        }

        /// <summary>
        /// 現在のモデル名がデフォルト値（またはクラス表示名）と同じかどうかを判定します。
        /// </summary>
        private bool IsDefaultName(IModel model)
        {
            var nameFieldDef = model.Metaclass.GetField("Name");
            if (nameFieldDef == null)
            {
                return false;
            }

            var defaultValue = nameFieldDef.DefaultValue?.ToString();

            // デフォルト値が未設定の場合は、クラスの表示名をデフォルト値とみなす
            if (string.IsNullOrEmpty(defaultValue))
            {
                defaultValue = model.Metaclass.DisplayName;
            }

            return string.Equals(model.Name, defaultValue);
        }

        /// <summary>
        /// 同一フィールドに同じ名前の兄弟モデルが存在するかどうかを判定します。
        /// </summary>
        private bool HasDuplicateName(IModel model, IModel owner, IField ownerField)
        {
            // そのフィールドに格納されている兄弟要素を取得
            var children = owner.GetFieldValues(ownerField.Name);
            if (children == null)
            {
                return false;
            }

            // 自分自身以外で、同じ名前を持つモデルを検索
            return children.Any(child => child.Id != model.Id && child.Name == model.Name);
        }
    }
}
