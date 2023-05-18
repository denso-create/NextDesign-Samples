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

        /// <summary>
        /// 「ソフト構造」のメタモデルに合わせてデータを作成します。
        /// </summary>
        public static ModelDto CreateSoftwareStructureDto()
        {
            return new ModelDto()
            {
                ClassName = "SoftwareStructureModel",
                ChildrenFieldName = "Layers"
            };
        }

        /// <summary>
        /// 「レイヤ」のメタモデルに合わせてデータを作成します。
        /// </summary>
        public static ModelDto CreateLayerDto()
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
        public static ModelDto CreateComponentDto()
        {
            return new ModelDto()
            {
                ClassName = "SoftwareComponent",
                ChildrenFieldName = "Functions"
            };
        }
    }
}
