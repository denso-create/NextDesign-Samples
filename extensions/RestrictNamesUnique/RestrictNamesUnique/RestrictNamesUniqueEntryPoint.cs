using System;
using System.Windows;
using RestrictNamesUnique.Events;
using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using NextDesign.Extension;

namespace RestrictNamesUnique
{
    /// <summary>
    /// エクステンションのエントリポイントです
    /// </summary>
    public class RestrictNamesUniqueEntryPoint : ExtensionBase
    {
        /// <summary>
        /// 重複チェックを有効にするためのタグ名（共通定義）
        /// </summary>
        /// メタモデルで対象フィールドのタグに設定することで、重複チェックを有効にします。
        internal const string c_TagName_IsUniqueNameEnforced = "IsUniqueNameEnforced";

        /// <summary>
        /// アクティベート時の処理です。
        /// </summary>
        protected override void OnActivate()
        {
            // イベント登録：OnFieldChanged イベント
            ExtensionPoints.Events.AddModelEvent().RegisterOnFieldChanged<ModelFieldChanged>();

            Context.App.Output.WriteLine("system", "RestrictNamesUnique エクステンションがアクティベートされました。");
        }
    }
}
