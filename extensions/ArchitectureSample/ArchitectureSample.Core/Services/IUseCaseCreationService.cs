using System.Collections.Generic;
using NextDesign.Core;

namespace ArchitectureSample.Core.Services
{
    /// <summary>
    /// ユースケースを作成するサービスのインターフェース定義
    /// </summary>
    public interface IUseCaseCreationService
    {
        /// <summary>
        /// ユースケースを作成する
        /// </summary>
        /// <param name="owner">作成したユースケースを所有させるモデル</param>
        /// <param name="names">作成するユースケースにつける名前</param>
        /// <returns>作成したユースケースのコレクション</returns>
        IEnumerable<IModel> CreateUseCases(IModel owner, IEnumerable<string> names);
    }
}