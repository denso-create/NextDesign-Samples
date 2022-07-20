using NextDesign.Core;
using System;
using System.Collections.Generic;
using System.Text;

namespace ArchitectureSample.Core.Services.Impl
{
    internal class UseCaseCreationService : IUseCaseCreationService
    {
        /// <inheritdoc/>
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
