using System;
using System.Collections.Generic;
using ArchitectureSample.Core.Services;
using ArchitectureSample.Core.Services.Impl;

namespace ArchitectureSample.Core
{
    /// <summary>
    /// サービスファクトリの実装です。
    /// </summary>
    public static class SampleServiceFactory
    {
        /// <summary>
        /// サービスのインターフェースに対する実装クラス
        /// </summary>
        private static IDictionary<Type, Type> m_Types = new Dictionary<Type, Type>();

        /// <summary>
        /// サービスを登録します
        /// </summary>
        /// <typeparam name="I">インターフェース</typeparam>
        /// <typeparam name="T">実装クラスの型</typeparam>
        public static void Register<I, T>()
        {
            m_Types.Add(typeof(I), typeof(T));
        }

        /// <summary>
        /// デフォルトのサービスを登録します
        /// </summary>
        public static void InitializeDefaults()
        {
            Register<IUseCaseCreationService, UseCaseCreationService>();
        }

        /// <summary>
        /// サービスインターフェースを要求してインスタンスを取得します。存在しない場合は例外を送出します。
        /// </summary>
        /// <typeparam name="I">要求インターフェース</typeparam>
        /// <returns>サービスインスタンス</returns>
        /// <exception cref="ArgumentException"></exception>
        public static I Get<I>() where I : class
        {
            if (!m_Types.TryGetValue(typeof(I), out var type))
            {
                throw new ArgumentException($"{typeof(I).Name}は対応していません。");
            }

            var service = Activator.CreateInstance(type) as I;
            return service;
        }
    }
}