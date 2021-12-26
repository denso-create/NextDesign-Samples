using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NextDesign.Core;
using NextDesign.Desktop;
using ExcelImportExtension.DataReader;

namespace ExcelImportExtension.ModelBuilder
{
	/// <summary>
	/// Next Design にデータを書き込むクラス
	/// </summary>
	public class SoftwareStructureModelBuilder
	{
		/// <summary>
		/// Next Design に読み込んだデータを書き込みます。
		/// </summary>
		public IModel AddStructuredModel(IModel model, string childrenFieldName, ModelDto dto)
		{
			// -------------------------------------
			// Next Design にデータを追加します。
			// -------------------------------------
			var addedModel = model.AddNewModel(childrenFieldName, dto.ClassName);

			// -------------------------------------
			// データの項目値を設定します。
			// -------------------------------------
			addedModel.SetField("Name", dto.Name);
			addedModel.SetField("Responsibility", dto.Responsibility);

			// -------------------------------------
			// 続けて、下位階層のデータを追加します。
			// -------------------------------------
			foreach (var child in dto.Children)
			{
				AddStructuredModel(addedModel, dto.ChildrenFieldName, child);
			}

			return addedModel;
		}
	}
}
