using System.Collections.Generic;
// エクステンション開発で参照するAPIの名前空間の宣言です
using NextDesign.Extension;
using NextDesign.Core;
using NextDesign.Desktop;
using NextDesign.Core.EditingCapabilities;

namespace ParentEditorSelectionSample
{
    class ParentEditorSelectionProvider : IModelEditorSelectionProvider
    {
        // サブエディタ、インスペクタの表示モードを識別するIDを定義します
        private const string c_ParentCategoryId = "MyExtension.Parent";
        private const string c_TypeDetailCategoryId = "Uml.Interaction.TypeDetail";

        /// <summary>
        /// サブエディタ、インスペクタの表示モードの一覧を取得します
        /// </summary>
        public ModelEditorCategoriesResult GetCategories(ModelEditorCategoriesParams param)
        {
            var model = param.Model;

            // ガード
            if (model == null || model.Metaclass == null)
            {
                return null;
            }

            // 選択モデルに親がいなければ親表示を追加する必要がないためnullを返します
            // nullを返すと Next Design 標準の動作になります
            if (model.Owner == null)
            {
                return null;
            }

            // 表示モードのリストに親を表示するモードを追加します
            var categoryList = new List<ModelEditorCategory>();
            // アイコンや表示位置の指定がない場合は、表示モードを識別するためのIDと表示名称だけを指定します
            categoryList.Add(new ModelEditorCategory(c_ParentCategoryId, "親"));

            if (model.Metaclass.Name == "UmlInteractionLifeline" || model.Metaclass.Name == "UmlInteractionMessage")
            {
                // モデルがライフライン、メッセージの場合は、詳細（型）を追加します
                // 詳細の次に表示するため、DisplayOrderを指定します
                categoryList.Add(new ModelEditorCategory(c_TypeDetailCategoryId, "詳細 (型)", null, (ModelEditorCategory.c_DisplayOrderDetail + 1), true));
            }

            return new ModelEditorCategoriesResult(categoryList);
        }

        /// <summary>
        /// サブエディタ、インスペクタに表示する対象のモデルを取得します
        /// </summary>
        public ModelEditorSelectionResult GetModel(ModelEditorSelectionParams param)
        {
            var categoryId = param.CategoryId;
            if ((categoryId != c_ParentCategoryId) && (categoryId != c_TypeDetailCategoryId))
            {
                // 追加した親表示or詳細（型）のカテゴリID以外は処理しないのでnullを返します。
                // nullを返すと表示するエディタがない旨が表示されます
                return null;
            }

            var model = param.Model;

            // ガード
            if (model == null || model.Metaclass == null)
            {
                return null;
            }
            if (model.Owner == null)
            {
                return null;
            }

            if (categoryId == c_ParentCategoryId)
            {
                // 親モデルを取得し、返します
                var parentModel = model.Owner as IModel;
                return new ModelEditorSelectionResult(parentModel);
            }else if(categoryId == c_TypeDetailCategoryId)
            {
                // ライフラインorメッセージの型を取得し、返します
                switch (model)
                {
                    case ILifeline lifeline:
                        return new ModelEditorSelectionResult(lifeline.TypeModel);
                    case IMessage message:
                        return new ModelEditorSelectionResult(message.TypeModel);
                    default:
                        return null;
                }
            }
            return null;
        }
    }
}
