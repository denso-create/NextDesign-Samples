using NextDesign.Core;
using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;

namespace ExtensionPointsSample.Models
{
    /// <summary>
    /// SampleModel
    /// </summary>
    public class SampleModel
    {
        /// <summary>
        /// モデル情報
        /// </summary>
        private IModel m_Model;

        /// <summary>
        /// コンストラクタ
        /// </summary>
        /// <param name="m"></param>
        public SampleModel(IModel m)
        {
            m_Model = m;
        }

        /// <summary>
        /// 初期化処理
        /// </summary>
        public void Initialize()
        {
            m_Model.SetField("Name", "SampleModel - made by command");
            m_Model.SetField("Description", "This model was added by the command.");
        }
    }
}