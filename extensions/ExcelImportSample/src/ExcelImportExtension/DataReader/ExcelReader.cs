using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using NPOI.SS.UserModel;

namespace ExcelImportExtension.DataReader
{
	/// <summary>
	/// Excelファイルからデータを読み込むクラス
	/// </summary>
	/// <remarks>
	/// Excelファイルの操作にはオープンソースの NPOI を利用しています。
	/// https://github.com/tonyqus/npoi/blob/master/README.md
	/// https://qiita.com/hukatama024e/items/37427f2578a8987645dd
	/// </remarks>
	public class ExcelReader
	{
		/// <summary>
		/// Excelファイルからデータを読み込みます。
		/// </summary>
		public IList<ModelDto> Read(string filePath)
		{
			IList<ModelDto> layerList = new List<ModelDto>();
			IList<ModelDto> owner = null;

			// ------------------------------------------------------
			// Excelファイルを開いて「ソフト構造」シートを取得します。
			// ------------------------------------------------------
			var workbook = WorkbookFactory.Create(filePath);
			var worksheet = workbook.GetSheet("ソフト構造");

			// ------------------------------------------------------
			// Excelシートから各行を読み込みます。
			// ------------------------------------------------------
			int rowIndex = 1;	// 2行目から開始
			do
			{
				var row = worksheet.GetRow(rowIndex);
				var cellValues = GetStringCellValues(row);

				// 空行が見つかれば読み込みを終了します。
				if (!cellValues.Any() || cellValues.All(v => string.IsNullOrEmpty(v)))
				{
					break;
				}

				// ------------------------------------------------------
				// A列に値があれば「レイヤ」のデータとして読み込みます。
				// ------------------------------------------------------
				if (cellValues[0].Length > 0)
				{
					var layer = CreateLayerDto();
					layer.Name = cellValues[0];             // A列：名前
					layer.Responsibility = cellValues[2];   // C列：責務
					layerList.Add(layer);
					owner = layer.Children;
				}
				// ------------------------------------------------------
				// B列に値があれば「コンポーネント」のデータとして読み込みます。
				// ------------------------------------------------------
				else if (cellValues[1].Length > 0)
				{
					var component = CreateComponentDto();
					component.Name = cellValues[1];				// B列：名前
					component.Responsibility = cellValues[2];   // C列：責務
					owner?.Add(component);
				}
			} while (rowIndex++ < worksheet.LastRowNum);

			return layerList;
		}

		/// <summary>
		/// Excelファイルを選択するダイアログを表示します。
		/// </summary>
		public string ShowFileSelectDialog()
		{
			OpenFileDialog openFileDialog = new OpenFileDialog
			{
				Filter = "Excel Files (*.xls, *.xlsx)|*.xls;*.xlsx"
			};

			if (openFileDialog.ShowDialog() != DialogResult.OK)
			{
				return null;
			}

			return openFileDialog.FileName;
		}

		/// <summary>
		/// 全ての列のセル値を文字列型で取得します。
		/// </summary>
		private IList<string> GetStringCellValues(IRow row)
		{
			var cells = new List<string>();
			for (var colIndex = 0; colIndex < row.LastCellNum; colIndex++)
			{
				cells.Add(row.GetCell(colIndex).StringCellValue);
			}
			return cells;
		}

		/// <summary>
		/// 「レイヤ」のメタモデルに合わせてデータを作成します。
		/// </summary>
		private ModelDto CreateLayerDto()
		{
			return new ModelDto()
			{
				ClassName = "SoftwareLayer",
				ChildrenFieldName = "Components"
			};
		}

		/// <summary>
		/// 「コンポーネント」のメタモデルに合わせてデータを作成します。
		/// </summary>
		private ModelDto CreateComponentDto()
		{
			return new ModelDto()
			{
				ClassName = "SoftwareComponent",
				ChildrenFieldName = "Functions"
			};
		}
	}
}
