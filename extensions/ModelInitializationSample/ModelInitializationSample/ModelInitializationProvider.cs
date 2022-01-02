using System;
using System.Collections.Generic;
using System.Text;
using NextDesign.Core;
using NextDesign.Core.EditingCapabilities;
using NextDesign.Desktop;

namespace ModelInitializationSample
{
    class ModelInitializationProvider : IModelInitializationProvider
    {
        /// <summary>
        /// 初期化処理の対象にするメタモデルを設定します
        /// </summary>
        /// <param name="context"></param>
        public void InitializeProvider(IModelInitializationProviderInitializationContext context)
        {
            // 「UseCase」を初期化処理の対象として登録します
            IClass usecaseClass = context.Project.Profile.Metamodels.FindClassesByName("UseCase").GetItem(0);
            if (usecaseClass != null)
            {
                context.RegisterClass(usecaseClass);
            }
        }

        /// <summary>
        /// 指定したメタモデルの生成時に初期化処理を実行します
        /// </summary>
        /// <param name="initializeParams"></param>
        public void InitializeFields(ModelInitializationParams initializeParams)
        {
            // モデルの複製の場合は何もしません
            if (initializeParams.IsCloned)
            {
                return;
            }
            // ユースケースには必ず「基本シナリオ」を定義する設計ルールに対して、自動で子モデルを生成します
            var model = initializeParams.Model;
            var scenario = model.AddNewModel("Scenarios", "Scenario");
            scenario.SetField("Name", "基本シナリオ");

        }
    }
}
