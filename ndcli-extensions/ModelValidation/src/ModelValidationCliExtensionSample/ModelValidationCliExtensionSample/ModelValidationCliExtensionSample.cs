using NextDesign.Cli.ExtensionFramework;
using DensoCreate.Cli.Framework;
using NextDesign.Core.Runtime;
using NextDesign.Core;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace ModelValidate.CliExtension
{
    /// <summary>
    /// モデル検証を提供するエクステンションです
    /// </summary>
    public class ModelValidateExtension : ExtensionBase
    {
        /// <summary>
        /// コンストラクタ
        /// </summary>
        public ModelValidateExtension()
            : base("NextDesign.ModelValidate")
        {
        }
    }

    /// <summary>
    /// モデル検証コマンド
    /// </summary>
    public class ModelValidateCommand : Command
    {
        /// <summary>
        /// コンストラクタ
        /// </summary>
        public ModelValidateCommand()
            : base("ModelValidate", new string[] { "MV", "mv" }, "モデル検証を実行するコマンドです")
        {
            // コマンドのオプション定義
            // DensoCreate.Cli.Framework.CommandBase.AddOption<T>() メソッドを使用して定義します。
            // <T>: オプションの型
            // 第1引数: オプション名とエイリアス（例: "--projectPath", "-p"）の配列
            // 第2引数: オプションの説明（ヘルプ表示用）
            // 第3引数: 必須オプションかどうか（true: 必須, false: 任意）
            // ExistingOnly(): FileInfo型の場合、指定されたファイルが存在するかをチェックします。
            AddOption<FileInfo>(new string[] { "--projectPath", "-p" }, "プロジェクトファイルのパス", true).ExistingOnly();
            AddOption<bool>(new string[] { "--doModelValidate", "--model", "-m" }, "モデルの整合チェックを実行します");
            AddOption<bool>(new string[] { "--doFeatureValidate", "--feature", "-f" }, "フィーチャーの整合チェックを実行します");
            AddOption<bool>(new string[] { "--doConfigurationValidate", "--configuration", "-c" }, "コンフィグレーションの整合チェックを実行します");
            
            // コマンドハンドラの登録
            RegisterHandler(nameof(OnExecute));
        }

        /// <summary>
        /// コマンドハンドラの実行
        /// </summary>
        /// <param name="projectPath">プロジェクトファイルのパス</param>
        /// <param name="doModelValidate"></param>
        /// <param name="doFeatureValidate"></param>
        /// <param name="doConfigurationValidate"></param>
        private void OnExecute(FileInfo projectPath, bool doModelValidate = false, bool doFeatureValidate = false, bool doConfigurationValidate = false)
        {
            Console.WriteLine($"{Extension.Name}");
            Console.WriteLine($"  Project       : {projectPath}");
            Console.WriteLine($"  Model         : {(doModelValidate ? "Yes" : "Skip")}");
            Console.WriteLine($"  Feature       : {(doFeatureValidate ? "Yes" : "Skip")}");
            Console.WriteLine($"  Configuration : {(doConfigurationValidate ? "Yes" : "Skip")}");
            Console.WriteLine("");

            // プロジェクトを開く
            // DensoCreate.Cli.Framework.ExtensionBase.GetService<T>() メソッドで
            // NextDesign.Core.Runtime.IProjectService サービスを取得し、
            // IProjectService.OpenProject() メソッドを使用してプロジェクトを開きます。
            var projectService = GetService<IProjectService>();
            var project = projectService.OpenProject(projectPath.FullName);

            if (doModelValidate)
            {
                project.Validate();
                var errors = project.GetAllErrorsWithChildren();
                OutputErrors("Model", errors);
            }

            if (doFeatureValidate)
            {
                var fms = project.ProductLineModel.FeatureModels;
                foreach (var fm in fms) fm.Validate();
                var errors = fms.SelectMany(fm => fm.GetAllErrorsWithChildren());
                OutputErrors("FeatureModels", errors);
            }

            if (doConfigurationValidate)
            {
                project.ProductLineModel.ConfigurationModel.Validate();
                var errors = project.ProductLineModel.ConfigurationModel.GetAllErrorsWithChildren();
                OutputErrors("Configuration", errors);
            }
        }

        private void OutputErrors(string name, IEnumerable<IError> errors)
        {
            Console.WriteLine($"{name}({errors.Count()})");
            foreach (var error in errors.Take(10))
            {
                Console.WriteLine($"  [{error.Type}]({error.Category}) : {error.Message}");
            }

            if (errors.Count() > 10)
            {
                Console.WriteLine("  :");
            }

            Console.WriteLine("");
        }
    }
}
