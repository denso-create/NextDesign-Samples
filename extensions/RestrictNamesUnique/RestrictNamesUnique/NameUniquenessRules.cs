using NextDesign.Core;
using System.Linq;

namespace RestrictNamesUnique
{
    /// <summary>
    /// 名前の一意性チェック共通ルール
    /// </summary>
    internal static class NameUniquenessRules
    {
        /// <summary>
        /// 重複チェックを有効にするためのタグ名（共通定義）
        /// </summary>
        internal const string c_TagName_IsUniqueNameEnforced = "IsUniqueNameEnforced";

        /// <summary>
        /// この拡張で使用するエラーカテゴリ名（共通定義）
        /// </summary>
        internal const string c_ErrorCategory_RestrictNamesUnique = "Error.RestrictNamesUnique";

        /// <summary>
        /// モデルがこのルールに違反しているかどうかを判定します。
        /// 対象外（親なし、タグなし、デフォルト名など）の場合は false を返します。
        /// </summary>
        internal static bool ValidateModel(IModel model, out IModel owner, out IField ownerField)
        {
            owner = null;
            ownerField = null;

            if (!TryGetValidationContext(model, out owner, out ownerField))
            {
                return false;
            }

            return HasDuplicateName(model, owner, ownerField);
        }

        /// <summary>
        /// ルール違反時に表示／登録するエラーメッセージを生成します。
        /// </summary>
        internal static string CreateErrorMessage(IModel model, IField ownerField)
        {
            return $"同じ名前のモデル '{model.Name}' がフィールド '{ownerField.DisplayName}' に既に存在します。";
        }

        /// <summary>
        /// チェック対象となるコンテキストを取得します。
        /// </summary>
        private static bool TryGetValidationContext(IModel model, out IModel owner, out IField ownerField)
        {
            owner = model.Owner;
            ownerField = null;

            if (owner == null)
            {
                return false;
            }

            ownerField = model.GetOwnerField();
            if (ownerField == null)
            {
                return false;
            }

            if (!IsTargetField(ownerField))
            {
                return false;
            }

            if (IsDefaultName(model))
            {
                return false;
            }

            return true;
        }

        /// <summary>
        /// 同一フィールドに同じ名前の兄弟モデルが存在するかどうかを判定します。
        /// </summary>
        private static bool HasDuplicateName(IModel model, IModel owner, IField ownerField)
        {
            var children = owner.GetFieldValues(ownerField.Name);
            if (children == null)
            {
                return false;
            }

            return children.Any(child => child.Id != model.Id && child.Name == model.Name);
        }

        /// <summary>
        /// 重複チェック対象のフィールドかどうかを判定します。
        /// </summary>
        private static bool IsTargetField(IField field)
        {
            var tagValue = field.GetTagValue(c_TagName_IsUniqueNameEnforced);
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
        private static bool IsDefaultName(IModel model)
        {
            var nameFieldDef = model.Metaclass.GetField("Name");
            if (nameFieldDef == null)
            {
                return false;
            }

            var defaultValue = nameFieldDef.DefaultValue?.ToString();

            if (string.IsNullOrEmpty(defaultValue))
            {
                defaultValue = model.Metaclass.DisplayName;
            }

            return string.Equals(model.Name, defaultValue);
        }
    }
}
