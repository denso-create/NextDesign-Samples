using IprojMigrationTool.Properties;
using NextDesign.Core;
using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Input;

namespace IprojMigrationTool.Commands
{
    /// <summary>
    /// iprojプロジェクトの移行処理を行うコマンドハンドラです。
    /// </summary>
    internal class IProjMigrationCommand : CommandHandlerBase
    {
        /// <summary>
        /// コマンドを実行します。
        /// </summary>
        /// <param name="c">コマンド実行のコンテキスト情報。</param>
        /// <param name="p">コマンド実行のパラメータ。</param>
        protected override void OnExecute(ICommandContext c, ICommandParams p)
        {
            var message = string.Empty;

            // 1. 開始条件のチェック
            // ・対象プロジェクトを特定
            // ・開いていない場合はファイル選択ダイアログで指定
            var workspace = App.Workspace;
            var project = workspace.CurrentProject;
            if (project == null)
            {
                var filter = Messages.FileDialogIprojFilterDescription + @"(*.iproj)|*.iproj";
                var projectPath = App.Window.UI.ShowOpenFileDialog(filter: filter);
                if (string.IsNullOrEmpty(projectPath))
                {
                    // キャンセル
                    return;
                }
                project = workspace.OpenProject(projectPath);
            }
            // ・バックアップ確認
            message = Messages.ConfirmBackupProjectCompleted;
            if (!App.Window.UI.ShowConfirmDialog(message, ExtensionName))
            {
                // キャンセル
                return;
            }
            // ・プロジェクト拡張子
            var ext = Path.GetExtension(project.Path);
            if (!string.Equals(ext, ".iproj"))
            {
                message = Messages.NotIprojExtension;
                this.ShowOutputMessage(message);
                return;
            }
            // ・ダーティ状態
            if (project.HasUnsavedChanges())
            {
                message = Messages.UnsavedProjectChanges;
                this.ShowOutputMessage(message);
                return;
            }
            // ・ファイル存在と読み取り専用属性の確認
            if (!CheckProjectFilesStatus(project))
            {
                message = Messages.ErrorCheckProjectFilesStatus;
                this.ShowOutputMessage(message);
                return;
            }

            // 2. 開始メッセージを出力
                message = string.Format(Messages.IprojMigrationStartMessage, project.Path);
            this.OutputMessage(message);

            try
            {
                // マウスポインタを処理中に変更
                Mouse.OverrideCursor = Cursors.Wait;

                // 3. モデルファイル分割の状態などを保持
                SaveProjectFilesInfo(c, project);

                // 4. プロジェクトファイルを開きなおして読み取り専用属性を反映
                project = ReopenProject(project);

                // 5. 未ロードのモデルユニットをロード
                LoadAllModelFiles(project);

                // 6. nproj 保存パスを決定して保存
                var nprojPath = Path.ChangeExtension(project.Path, ".nproj");
                message = string.Format(Messages.SavingNproj, nprojPath);
                this.OutputMessage(message);
                var saveResult = workspace.SaveProjectAs(nprojPath, project);
                if (!saveResult)
                {
                    message = Messages.NprojSaveFailed;
                    this.ShowOutputMessage(message);
                    return;
                }

                // 7. モデルファイルの分割状態を復元
                RestoreModelFiles(c, project);

                // 8. ユーザーに別途対処が必要な事項を通知
                NotifyUserActions(c, project);

                // 9. 移行元ファイル（iproj, iprof, imdl）を削除
                CleanupProjectFiles(c);

                // 10. プロジェクトファイルを開きなおして読み取り専用属性を反映
                project = ReopenProject(project);
            }
            finally
            {
                // マウスポインタを元に戻す
                Mouse.OverrideCursor = null;
            }

            // 11. 完了メッセージを表示
            message = Messages.IprojMigrationCompletedMessage;
            App.Window.EditorPage.ActiveNavigator = "Project";
            this.ShowOutputMessage(message);
        }

        /// <summary>
        /// プロジェクト構成ファイルの状態を確認する。
        /// ・移管対象のモデルファイルが存在するか
        /// ・移管対象のファイルが読み取り専用になっていないか
        /// </summary>
        /// <param name="project"></param>
        /// <returns></returns>
        private bool CheckProjectFilesStatus(IProject project)
        {
            var result = true;
            var message = string.Empty;

            var modelUnits = project.UnitManager.ModelUnits;
            foreach (var modelUnit in modelUnits)
            {
                if ((modelUnit.Type == "Project") ||
                    (modelUnit.Type == "Profile") ||
                    (modelUnit.Type == "Model" && !modelUnit.IsExternalUnit))
                {
                    if (!modelUnit.PhysicalFileExits)
                    {
                        // ファイルが存在しない
                        message = string.Format(Messages.TargetFileNotExist1, modelUnit.UnitPath);
                        this.OutputMessage(message);
                        result = false;
                    }
                    else if (modelUnit.IsReadonly)
                    {
                        // ファイルが読み取り専用
                        message = string.Format(Messages.TargetFileIsReadonly1, modelUnit.UnitPath);
                        this.OutputMessage(message);
                        result = false;
                    }
                }
            }

            return result;
        }

        /// <summary>
        /// プロジェクトファイルを開きなおす。
        /// ・読み取り専用属性を反映するため
        /// </summary>
        /// <param name="project"></param>
        private IProject ReopenProject(IProject project)
        {
            var workspace = App.Workspace;
            var projectPath = workspace.CurrentProject.Path;
            workspace.CloseProject();
            return workspace.OpenProject(projectPath);
        }

        /// <summary>
        /// 参照登録以外のモデルファイルをすべてロードします。
        /// </summary>
        /// <param name="project">対象のプロジェクト。</param>
        private void LoadAllModelFiles(IProject project)
        {
            var unitManager = project.UnitManager;
            var notLoadedUnits = unitManager.ModelUnits.Where(u => !u.Loaded).ToList();
            if (notLoadedUnits.Any())
            {
                foreach (var unit in notLoadedUnits)
                {
                    if (!unit.IsExternalUnit)
                    {
                        var message = string.Format(Messages.LoadingModelFile, unit.Name);
                        this.OutputMessage(message);
                        App.Workspace.LoadModelUnits(project, new[]{ unit });
                    }
                }
            }
        }

        /// <summary>
        /// プロジェクトのプロファイルユニットのパスを取得します。
        /// </summary>
        /// <param name="project">対象のプロジェクト。</param>
        /// <returns>プロファイルユニットの絶対パス。プロファイルが存在しない場合は空文字列です。</returns>
        private string GetProfilePath(IProject project)
        {
            var profileUnit = project.Profile.ProfileUnit;
            return (profileUnit.Type == "Profile") ? profileUnit.AbsolutePath : string.Empty;
        }

        /// <summary>
        /// プロジェクトのファイル構成をコマンドコンテキストに保存します。
        /// </summary>
        /// <param name="c">コマンド実行のコンテキスト情報。</param>
        /// <param name="project">対象のプロジェクト。</param>
        private void SaveProjectFilesInfo(ICommandContext c, IProject project)
        {
            var message = string.Empty;

            // モデルファイルの構成情報を収集
            var modelFileInfoList = new List<ModelFileInfo>();
            var modelFiles = project.UnitManager.ModelUnits.Where(u => (u.Type == "Model")).ToList();
            foreach (var modelFile in modelFiles)
            {
                modelFileInfoList.Add(new ModelFileInfo(modelFile));

                // 参照登録されたモデルファイルは書き換えをガード
                if ((modelFile.IsExternalUnit) && (File.Exists(modelFile.AbsolutePath)))
                {
                    // 読み取り専用属性を設定
                    File.SetAttributes(modelFile.AbsolutePath, File.GetAttributes(modelFile.AbsolutePath) | FileAttributes.ReadOnly);
                }
            }

            // ファイル構成をコマンドコンテキストに保持
            c.SetProperty("iprojPath", project.Path);
            c.SetProperty("iprofPath", GetProfilePath(project));
            c.SetProperty("ModelFileInfo", modelFileInfoList);
        }

        /// <summary>
        /// コマンドコンテキストからモデルファイル情報を取得し、モデルファイルの分割状態を復元します。
        /// </summary>
        /// <param name="c">コマンド実行のコンテキスト情報。</param>
        /// <param name="project">対象のプロジェクト。</param>
        private void RestoreModelFiles(ICommandContext c, IProject project)
        {
            var modelFileInfoList = c.GetProperty("ModelFileInfo") as List<ModelFileInfo>;
            foreach (var target in modelFileInfoList)
            {
                if (target.ModelUnitIsExternalUnit)
                {
                    // 参照登録されたモデルファイルの読み取り専用属性を復元
                    if (!target.ModelUnitIsReadonly && File.Exists(target.ModelUnitAbsolutePath))
                    {
                        // 読み取り専用属性だけを外す
                        var attributes = File.GetAttributes(target.ModelUnitAbsolutePath);
                        attributes &= ~FileAttributes.ReadOnly;
                        File.SetAttributes(target.ModelUnitAbsolutePath, attributes);
                    }
                }
                else
                {
                    // 参照登録以外のモデルファイル
                    var message = string.Format(Messages.DividingModelFile, target.ModelUnitName);
                    this.OutputMessage(message);

                    var model = project.GetModelById(target.ModelId);
                    var folderPath = Path.GetDirectoryName(target.ModelUnitPath);
                    project.UnitManager.SplitModelUnit(model, target.ModelUnitName, folderPath);
                }
            }
        }

        /// <summary>
        /// 移行元のプロジェクトファイル及び関連ファイルを削除します。
        /// </summary>
        /// <param name="c">コマンド実行のコンテキスト情報。</param>
        private void CleanupProjectFiles(ICommandContext c)
        {
            var iprojPath = c.GetProperty("iprojPath") as string;
            var iprofPath = c.GetProperty("iprofPath") as string;
            var modelFileInfoList = c.GetProperty("ModelFileInfo") as List<ModelFileInfo>;

            // iproj
            DeleteFile(iprojPath);

            // iprof
            if (!string.IsNullOrEmpty(iprofPath))
            {
                DeleteFile(iprofPath);
            }

            // imdl（参照登録除く）
            foreach (var modelFile in modelFileInfoList)
            {
                if (!modelFile.ModelUnitIsExternalUnit)
                {
                    DeleteFile(modelFile.ModelUnitAbsolutePath);
                }
            }
        }

        /// <summary>
        /// 指定ファイルを削除します（例外処理あり）
        /// </summary>
        /// <param name="path"></param>
        private void DeleteFile(string path)
        {
            try
            {
                File.Delete(path);
            }
            catch (Exception ex)
            {
                var message = string.Format(Messages.SourceFileDeleteFailed, ex.Message);
                Output.WriteLine(ExtensionName, message);
            }
        }

        /// <summary>
        /// ユーザーに別途対処が必要な事項を通知します。
        /// </summary>
        /// <param name="c">コマンドコンテキスト。</param>
        private void NotifyUserActions(ICommandContext c, IProject project)
        {
            var message = string.Empty;

            //- プロファイルがファイル分割されている
            var iprofPath = c.GetProperty("iprofPath") as string;
            if (!string.IsNullOrEmpty(iprofPath))
            {
                message = string.Format(Messages.ProfileFileSplitInfo, iprofPath);
                this.OutputMessage(message);

                // プロファイルファイル名とプロジェクトのプロファイル名が異なる場合は通知
                var iprofName = Path.GetFileNameWithoutExtension(iprofPath);
                var profileName = project.Profile.Name;
                if (iprofName != profileName)
                {
                    message = string.Format(Messages.ProfileNameDifferenceInfo2, profileName, Path.GetFileName(iprofPath));
                    this.OutputMessage(message);
                }
            }

            //- 参照登録されているモデルファイルがある
            var referencedModelFiles = project.UnitManager.ModelUnits.Where(u => (u.Type == "Model") && (u.IsExternalUnit)).ToList();
            foreach (var referencedModelFile in referencedModelFiles)
            {
                message = string.Format(Messages.ExternalModelFileInfo, referencedModelFile.UnitPath);
                this.OutputMessage(message);
            }

            //- プロファイル参照が利用されている
            var packages = project.Profile.RootPackage.GetAllSubPackages().Where(p => p.ProfileReference != null).ToList();
            foreach (var package in packages)
            {
                message = string.Format(Messages.ProfileReferenceInfo, package.Uri);
                this.OutputMessage(message);
            }

            // 構成管理ファイルの拡張子変更コマンド一覧を出力
            OutputGitSvnMvCommands(c);
        }

        /// <summary>
        /// 構成管理ファイルの拡張子変更コマンド一覧をgit-svn-mv-commands.txtへ出力します。
        /// </summary>
        /// <param name="c">コマンドコンテキスト。</param>
        private void OutputGitSvnMvCommands(ICommandContext c)
        {
            var iprojPath = c.GetProperty("iprojPath") as string;
            var iprofPath = c.GetProperty("iprofPath") as string;
            var modelFileInfoList = c.GetProperty("ModelFileInfo") as List<ModelFileInfo>;

            var projectFolder = Path.GetDirectoryName(iprojPath);
            var commandFilePath = Path.Combine(projectFolder, "git-svn-mv-commands.txt");

            try
            {
                var gitCommands = GenerateGitSvnMvCommands("git mv", iprojPath, iprofPath, modelFileInfoList);
                var svnCommands = GenerateGitSvnMvCommands("svn mv", iprojPath, iprofPath, modelFileInfoList);

                var commands = new List<string>();
                commands.Add("# ==== Git Commands ====");
                commands.AddRange(gitCommands);
                commands.Add("");  // 空行区切り
                commands.Add("# ==== SVN Commands ====");
                commands.AddRange(svnCommands);

                // BOMなしUTF8で出力
                var utf8withoutBom = new UTF8Encoding(false);
                File.WriteAllLines(commandFilePath, commands, utf8withoutBom);

                var message = string.Format(Messages.OutputGitSvnMvCommandsCompleted, commandFilePath);
                this.OutputMessage(message);
            }
            catch (Exception ex)
            {
                var message = string.Format(Messages.OutputGitSvnMvCommandsFailed, ex.Message);
                this.OutputMessage(message);
            }
        }

        /// <summary>
        /// 構成管理ファイルの拡張子変更コマンド一覧を生成します。
        /// </summary>
        /// <param name="commandName">実行コマンド名（例："git mv"、"svn mv"）。</param>
        /// <param name="iprojPath">元プロジェクトファイルパス。</param>
        /// <param name="iprofPath">元プロファイルファイルパス（存在しなければnullまたは空文字）。</param>
        /// <param name="modelFileInfoList">モデルファイル情報リスト。</param>
        /// <returns>移動コマンド文字列リスト。</returns>
        private List<string> GenerateGitSvnMvCommands(
            string commandName,
            string iprojPath,
            string iprofPath,
            List<ModelFileInfo> modelFileInfoList)
        {
            var commands = new List<string>();
            var baseDir = Path.GetDirectoryName(iprojPath) ?? "";

            // iprojファイルの相対パスと新ファイル名
            var relativeIproj = Path.GetRelativePath(baseDir, iprojPath);
            var nprojPath = Path.ChangeExtension(relativeIproj, ".nproj");
            commands.Add($"{commandName} \"{relativeIproj}\" \"{nprojPath}\"");

            // iprofファイルがあれば同様に相対パスで追加
            if (!string.IsNullOrEmpty(iprofPath))
            {
                var relativeIprof = Path.GetRelativePath(baseDir, iprofPath);
                var nprofPath = Path.ChangeExtension(relativeIprof, ".nprof");
                commands.Add($"{commandName} \"{relativeIprof}\" \"{nprofPath}\"");
            }

            // 参照登録されたモデルファイルも相対パスで
            foreach (var modelFile in modelFileInfoList)
            {
                if (!modelFile.ModelUnitIsExternalUnit)
                {
                    var relativeMdl = Path.GetRelativePath(baseDir, modelFile.ModelUnitPath);
                    var nmdlPath = Path.ChangeExtension(relativeMdl, ".nmdl");
                    commands.Add($"{commandName} \"{relativeMdl}\" \"{nmdlPath}\"");
                }
            }

            return commands;
        }
    }

    /// <summary>
    /// モデルファイル情報を保持します。
    /// </summary>
    internal class ModelFileInfo
    {
        /// <summary>
        /// モデルのIDを取得します。
        /// </summary>
        public string ModelId { get; }

        /// <summary>
        /// モデルユニットの名前を取得します。
        /// </summary>
        public string ModelUnitName { get; }

        /// <summary>
        /// モデルユニットの相対パスを取得します。
        /// </summary>
        public string ModelUnitPath { get; }

        /// <summary>
        /// モデルユニットの絶対パスを取得します。
        /// </summary>
        public string ModelUnitAbsolutePath { get; }

        /// <summary>
        /// 参照登録か否かを取得します。
        /// </summary>
        public bool ModelUnitIsExternalUnit { get; }

        /// <summary>
        /// 読み取り専用か否かを取得します。
        /// </summary>
        public bool ModelUnitIsReadonly { get; }

        /// <summary>
        /// モデルファイル情報の新しいインスタンスを初期化します。
        /// </summary>
        /// <param name="modelUnit">外部ユニットでないモデルユニット。</param>
        public ModelFileInfo(IModelUnit modelUnit)
        {
            ModelId = modelUnit.TopElementId;
            ModelUnitName = modelUnit.Name;
            ModelUnitPath = modelUnit.UnitPath;
            ModelUnitAbsolutePath = modelUnit.AbsolutePath;
            ModelUnitIsExternalUnit = modelUnit.IsExternalUnit;
            ModelUnitIsReadonly = modelUnit.IsReadonly;
        }
    }
}
