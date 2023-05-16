using System.Collections.Generic;

namespace ExcelImportExtension.DataReader
{
    /// <summary>
    /// Excel ファイルから読み込んだデータを保持するクラス
    /// </summary>
    public class ModelDto
    {
        // 名前
        public string Name { get; set; }

        // 責務
        public string Responsibility { get; set; }

        // 階層配下の子要素のデータ
        public IList<ModelDto> Children { get; } = new List<ModelDto>();

        // メタモデルでのクラス名
        public string ClassName { get; set; }

        // 子要素を保持しているメタモデルでのフィールド名
        public string ChildrenFieldName { get; set; }
    }
}
