using NextDesign.Core;
using System;
using System.Collections.Generic;
using System.Text;

namespace ArchitectureSample.Core.Services
{
    public interface IUseCaseCreationService
    {
        IEnumerable<IModel> CreateUseCases(IModel owner, IEnumerable<string> names);
    }
}
