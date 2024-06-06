using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using NPOI.SS.UserModel;
using NPOI.SS.Util;
using NPOI.XSSF.UserModel;

namespace ExcelExtension
{
    /// <summary>
    /// Excelファイルからデータを読み込むクラス
    /// </summary>
    /// <remarks>
    /// Excelファイルの操作にはオープンソースの NPOI を利用しています。
    /// https://github.com/tonyqus/npoi/blob/master/README.md
    /// https://qiita.com/hukatama024e/items/37427f2578a8987645dd
    /// </remarks>
    public class ExcelHandler
    {
        /// <summary>
        /// Excelファイルからデータを読み込みます。
        /// </summary>
        /// <param name="filePath">対象ファイルのパス</param>
        public ModelDto Read(string filePath)
        {
            var dto = ModelDto.CreateSoftwareStructureDto();
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
                    var layer = ModelDto.CreateLayerDto();
                    layer.Name = cellValues[0];                                                 // A列：名前
                    layer.Responsibility = (cellValues.Count >= 3) ? cellValues[2] : "";        // C列：責務
                    dto.Children.Add(layer);
                    owner = layer.Children;
                }
                // ------------------------------------------------------
                // B列に値があれば「コンポーネント」のデータとして読み込みます。
                // ------------------------------------------------------
                else if ((cellValues.Count >= 2) && (! string.IsNullOrWhiteSpace(cellValues[1])))
                {
                    var component = ModelDto.CreateComponentDto();
                    component.Name = cellValues[1];				                                // B列：名前
                    component.Responsibility = (cellValues.Count >= 3) ? cellValues[2] : "";    // C列：責務
                    owner?.Add(component);
                }
            } while (rowIndex++ < worksheet.LastRowNum);

            workbook.Close();
            return dto;
        }

        /// <summary>
        /// Excelファイルへデータを書き出します。
        /// </summary>
        /// <param name="filePath">対象ファイルのパス</param>
        /// <param name="modelDto">書き出すデータ</param>
        public void Write(string filePath, ModelDto modelDto)
        {
            var columnHeaders = new List<string>();

            // ------------------------------------------------------
            // Excelファイルに新規シートを作成します。
            // ------------------------------------------------------
            IWorkbook workbook;
            if (File.Exists(filePath))
            {
                var inputStream = new FileStream(filePath, FileMode.Open);
                workbook = WorkbookFactory.Create(inputStream);
                inputStream.Close();
            }
            else
            {
                workbook = new XSSFWorkbook();
            }
            var sheet = CreateNewSheet(workbook, modelDto.Name);

            // ------------------------------------------------------
            // データの階層構造に従ってシートに行を出力します。
            // ------------------------------------------------------
            const int layerColumnIndex = 0;
            const int componentColumnIndex = 1;
            const int responsibilityColumnIndex = 2;
            const int columnHeaderRowIndex = 0;

            // 第1階層の「レイヤ」を出力します。
            int rowIndex = columnHeaderRowIndex + 1;				// 2行目から開始
            columnHeaders.Add(modelDto.ChildrenClassDisplayName);	// 列タイトル：メタモデルでのクラスの表示名
            foreach (var layer in modelDto.Children)
            {
                WriteCell(sheet, rowIndex, layerColumnIndex, layer.Name);
                WriteCell(sheet, rowIndex, responsibilityColumnIndex, layer.Responsibility);
                rowIndex++;

                // 第2階層の「コンポーネント」を出力します。
                if (columnHeaders.Count < 2)
                {
                    columnHeaders.Add(layer.ChildrenClassDisplayName);  // 列タイトル：メタモデルでのクラスの表示名
                }
                foreach (var component in layer.Children)
                {
                    WriteCell(sheet, rowIndex, componentColumnIndex, component.Name);
                    WriteCell(sheet, rowIndex, responsibilityColumnIndex, component.Responsibility);
                    rowIndex++;
                }
            }

            // ------------------------------------------------------
            // タイトル行を書き込みます。
            // ------------------------------------------------------
            for (var i = 0; i < columnHeaders.Count; i++)
            {
                WriteCell(sheet, columnHeaderRowIndex, i, columnHeaders[i]);
            }

            // ------------------------------------------------------
            // ファイルに保存します。
            // ------------------------------------------------------
            var fileStream = File.Create(filePath);
            workbook.Write(fileStream);
            workbook.Close();
            fileStream.Close();
        }

        /// <summary>
        /// 既存シートと名前が重複しない新規シートを作成します。
        /// </summary>
        /// <param name="workbook">対象ワークブック</param>
        /// <param name="baseSheetName">シート名</param>
        /// <returns>新規作成されたシート</returns>
        private ISheet CreateNewSheet(IWorkbook workbook, string baseSheetName)
        {
            baseSheetName = WorkbookUtil.CreateSafeSheetName(baseSheetName);
            var newSheetName = baseSheetName;
            var sheet = workbook.GetSheet(newSheetName);
            if (sheet != null)
            {
                // 既存シートと異なる名前の新規シートを作成します。
                for (var i = 2; i < 100; i++)
                {
                    newSheetName = string.Format(baseSheetName + " ({0})", i);
                    sheet = workbook.GetSheet(newSheetName);
                    if (sheet == null)
                    {
                        break;
                    }
                }
            }
            if (sheet != null)
            {
                throw new Exception("新規シートを作成できませんでした。");
            }

            // 指定された名前で新規シートを作成します。
            sheet = workbook.CreateSheet(newSheetName);
            return sheet;
        }

        /// <summary>
        /// 全ての列のセル値を文字列型で取得します。
        /// </summary>
        /// <param name="row">対象行</param>
        /// <returns>セルごとの文字列のリスト</returns>
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
        private string GetStringCellValue(ICell cell)
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
                        stringValue = cell.DateCellValue?.ToString("yyyy/MM/dd");
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
        /// シート上のセルに文字列を書き込みます。
        /// </summary>
        /// <param name="sheet">シート</param>
        /// <param name="rowIndex">行インデックス</param>
        /// <param name="columnIndex">列インデックス</param>
        /// <param name="value">文字列</param>
        /// <see cref="https://poi.apache.org/apidocs/dev/org/apache/poi/ss/usermodel/Cell.html"/>
        private void WriteCell(ISheet sheet, int rowIndex, int columnIndex, string value)
        {
            var row = sheet.GetRow(rowIndex) ?? sheet.CreateRow(rowIndex);
            var cell = row.GetCell(columnIndex) ?? row.CreateCell(columnIndex);
            cell.SetCellValue(value);
        }
    }
}
