using System.Linq;
using System.Collections.Generic;
using NextDesign.Core;
using NextDesign.Core.EditingCapabilities;
using NextDesign.Desktop;
using NextDesign.Extension;

namespace ShapeHighlightingSample
{
    public class ShapeHighlightingEntryPoint : IExtension
    {
        // 作業中のテキストを強調表示する書式です
        private Dictionary<StyleAttributes, object> workingTextAttribute
            = new Dictionary<StyleAttributes, object>()
            {
                { StyleAttributes.IsBold, true},
                { StyleAttributes.IsUnderline, true}
            };

        // 作業中のシェイプを強調表示する書式です
        private Dictionary<StyleAttributes, object> workingShapeAttribute
            = new Dictionary<StyleAttributes, object>()
            { 
                { StyleAttributes.ForeColor, "Red"},
                { StyleAttributes.BorderColor, "Red"}
            };

        /// <summary>
        /// テキストのスタイル値を取得するコールバック関数です
        /// </summary>
        private object GetTextStyle(IShape shape, TextTypes textType, string textPath, IModel model, IStyleProperty styleProperty)
        {
            object outValue;
            if (workingTextAttribute.TryGetValue(styleProperty.Attribute, out outValue))
            {
                // 「TBD」が名称に含まれると太字、下線にします。
                if (model.Name.Contains("TBD"))
                {
                    return outValue;
                }
            }
            // 太字、下線以外の書式は変更しないため、styleProperty.CurrentValueを返します。
            return styleProperty.CurrentValue;
        }

        /// <summary>
        /// シェイプのスタイル値を取得するコールバック関数です
        /// </summary>
        private object GetShapeStyle(IEditorElement element, IModel model, IStyleProperty styleProperty)
        {
            object outValue;
            if (workingShapeAttribute.TryGetValue(styleProperty.Attribute, out outValue))
            {
                // 「TBD」が名称に含まれるとフォント色と枠線色を赤にします。
                if (model.Name.Contains("TBD"))
                {
                    return outValue;
                }
            }

            // フォント色と枠線色以外の書式は変更しないため、styleProperty.CurrentValueを返します。
            return styleProperty.CurrentValue;
        }

        /// <summary>
        /// エクステンションを活性化します
        /// </summary>
        /// <param name="context">実行コンテキスト</param>
        public void Activate(IContext context)
        {
            // 条件付き書式を適用する対象の要素定義を取得します
            // 対象は、
            // ダイアグラム「機能構造図」の「Subsystem」です
            IElementDef targetDefinition = GetTargetDefinition(context, "SystemStructureModel", "機能構造図", "SubSystem");

            // コールバック関数を登録します
            // タイトルの文字色は、テキストではなくシェイプのスタイルで変更します。
            var viewDefinitions = context.App.Workspace.CurrentProject.Profile.ViewDefinitions;
            viewDefinitions.RegisterGetStyleCallback(targetDefinition, GetShapeStyle);
            viewDefinitions.RegisterGetTextStyleCallback(targetDefinition, TextTypes.Title, GetTextStyle);
        }

        /// <summary>
        /// エクステンションを非活性化します
        /// </summary>
        /// <param name="context">実行コンテキスト</param>
        public void Deactivate(IContext context)
        {
            // 登録したコールバック関数を解除します
            IElementDef targetDefinition = GetTargetDefinition(context, "SystemStructureModel", "機能構造図", "SubSystem");
            var viewDefinitions = context.App.Workspace.CurrentProject.Profile.ViewDefinitions;
            viewDefinitions.UnregisterStyleCallback(targetDefinition);
        }

        /// <summary>
        /// 書式変更対象を取得します
        /// </summary>
        private IElementDef GetTargetDefinition(IContext context, string diagramClassName, string diagramName, string targetClassName)
        {
            var profile = context.App.Workspace.CurrentProject.Profile;

            // カレントプロジェクトから名称で対象の要素定義を取得します。
            var diagramClass = profile.Metamodels.GetClass(diagramClassName);
            var diagramDefinition = profile.ViewDefinitions.FindEditorDefByClass(diagramClass, diagramName).GetItem(0);
            var targetClass = profile.Metamodels.GetClass(targetClassName);
            var targetDefinition = profile.ViewDefinitions.FindElementDefByClass(diagramDefinition, targetClass).GetItem(0);
            return targetDefinition;
        }
    }
}
