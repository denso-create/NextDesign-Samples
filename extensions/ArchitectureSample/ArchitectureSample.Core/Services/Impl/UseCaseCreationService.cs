using System.Collections.Generic;
using NextDesign.Core;

namespace ArchitectureSample.Core.Services.Impl
{
    /// <summary>
    /// ユースケースを作成するサービスの実装
    /// </summary>
    internal class UseCaseCreationService : IUseCaseCreationService
    {
        /// <inheritdoc />
        public IEnumerable<IModel> CreateUseCases(IModel owner, IEnumerable<string> names)
        {
            var createdModels = new List<IModel>();

            foreach (var name in names)
            {
                var model = owner.AddNewModel("UseCases", "UseCase");
                model.SetField("Name", name);
                createdModels.Add(model);
            }

            return createdModels;
        }
    }
}