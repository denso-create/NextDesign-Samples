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
        /// アクティベート時の処理です。
        /// </summary>
        protected override void OnActivate()
        {
            // モデル編集時の即時チェック（OnFieldChanged）
            ExtensionPoints.Events.AddModelEvent().RegisterOnFieldChanged<ModelsFieldChangedEvent>();

            // 検証実行時のチェック（OnValidate）
            ExtensionPoints.Events.AddModelEvent().RegisterOnValidate<ModelsValidateEvent>();

            // 拡張機能のアクティベート確認メッセージの出力
            Context.App.Output.WriteLine("system", "RestrictNamesUnique エクステンションがアクティベートされました。");
        }
    }
}
