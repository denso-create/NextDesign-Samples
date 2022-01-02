using System;
using System.Collections.Generic;
using System.Text;
using NextDesign.Core;
using NextDesign.Core.EditingCapabilities;
using NextDesign.Desktop;
using System.Linq;

namespace EditingCapability
{
	class ModelCreationProvider : IModelCreationProvider
	{
		public ModelCreatableResult GetCreatableClasses(ModelCreatableParams creatableParams)
		{
			// ユースケース以外は対象外のためnullを返し、Next Design標準に任せます
			var metaClass = creatableParams.Owner.Metaclass;
			var metamodels = creatableParams.Project.Profile.Metamodels;
			IClass requirementClass = metamodels.GetClass("UseCase");
			if (requirementClass != null)
			{
				if (!metaClass.IsClassOf(requirementClass))
				{
					return null;
				}
			}
			// 名称に「TBD」がないユースケースは特に制約をかけないためnullを返します
			if (!creatableParams.Owner.Name.Contains("TBD"))
			{
				return null;
			}

			// 名称に「TBD」があるユースケースは、条件不要で、シナリオのみ作成するルールにします
			var creatableResult = new ModelCreatableResult
			{
				Result = CapabilityResults.Success
			};

			// DefaultTypesにデフォルトの表示候補があるため、この中から必要なもののみを戻り値に詰めます
			foreach (var type in creatableParams.DefaultTypes)
			{
				// 条件は作成不要のため、それ以外のみをAddします
				if (!type.Value.First().Name.Contains("Condition"))
				{
					creatableResult.AddCreatableClasses(type.Key.Name, type.Value);
				}
			}

			return creatableResult;
		}
	}
}
