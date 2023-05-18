using System.Collections.Generic;
using System.Linq;
using NPOI.SS.UserModel;
using NextDesign.Desktop;

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
                if ((cellValues.Count >= 1) && (! string.IsNullOrWhiteSpace(cellValues[0])))
                {
                    var layer = CreateLayerDto();
                    layer.Name = cellValues[0];                                                 // A列：名前
                    layer.Responsibility = (cellValues.Count >= 3) ? cellValues[2] : "";        // C列：責務
                    layerList.Add(layer);
                    owner = layer.Children;
                }
                // ------------------------------------------------------
                // B列に値があれば「コンポーネント」のデータとして読み込みます。
                // ------------------------------------------------------
                else if ((cellValues.Count >= 2) && (! string.IsNullOrWhiteSpace(cellValues[1])))
                {
                    var component = CreateComponentDto();
                    component.Name = cellValues[1];				                                // B列：名前
                    component.Responsibility = (cellValues.Count >= 3) ? cellValues[2] : "";    // C列：責務
                    owner?.Add(component);
                }
            } while (rowIndex++ < worksheet.LastRowNum);

            return layerList;
        }

        /// <summary>
        /// 全ての列のセル値を文字列型で取得します。
        /// </summary>
        private IList<string> GetStringCellValues(IRow row)
        {
            var cells = new List<string>();
            if (row == null)
            {
                return cells;
            }

            for (var colIndex = 0; colIndex < row.LastCellNum; colIndex++)
            {
                var cell = row.GetCell(colIndex);
                var stringValue = GetStringCellValue(cell);
                cells.Add(stringValue);
            }
            return cells;
        }

        /// <summary>
        /// セル値を全て文字列として取得する
        /// </summary>
        /// <param name="cell">Cellオブジェクト</param>
        /// <returns>結果文字列</returns>
        /// <remarks>
        /// https://csharp.programmer-reference.com/npoi-cellvalue-getstring/
        /// </remarks>
        public string GetStringCellValue(ICell cell)
        {
            string stringValue = "";
            if (cell == null)
            {
                return stringValue;
            }

            var cellType = (cell.CellType == CellType.Formula) ? cell.CachedFormulaResultType: cell.CellType;
            switch (cellType)
            {
                case CellType.String:
                    //文字型
                    stringValue = cell.StringCellValue;
                    break;
                case CellType.Numeric:
                    if (DateUtil.IsCellDateFormatted(cell))
                    {
                        //日付型
                        stringValue = cell.DateCellValue.ToString("yyyy/MM/dd");
                    }
                    else
                    {
                        //数値型
                        stringValue = cell.NumericCellValue.ToString();
                    }
                    break;
                case CellType.Boolean:
                    //真偽型
                    stringValue = cell.BooleanCellValue.ToString();
                    break;
                case CellType.Blank:
                    //ブランク
                    stringValue = "";
                    break;
                case CellType.Error:
                    //エラー
                    stringValue = cell.ErrorCellValue.ToString();
                    break;
                default:
                    break;
            }

            return stringValue;
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
