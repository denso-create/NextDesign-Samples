using NextDesign.Core;
using NextDesign.Desktop;
using NextDesign.Desktop.ExtensionPoints;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using IprojMigrationTool.Properties;

namespace IprojMigrationTool.Commands
{
    /// <summary>
    /// プロジェクトの部分ロード設定の移行処理を行うコマンドハンドラです。
    /// </summary>
    internal class PartialLoadMigrationCommand : CommandHandlerBase
    {
        /// <summary>
        /// Enterpriseエディションの識別ID
        /// </summary>
        private static readonly HashSet<string> c_EnterpriseEditionIds = new HashSet<string> { "Ent.Dsgn", "Ent.Arch" };

        /// <summary>
        /// コマンドを実行します。
        /// </summary>
        /// <param name="c">コマンド実行のコンテキスト情報。</param>
        /// <param name="p">コマンド実行のパラメータ。</param>
        protected override void OnExecute(ICommandContext c, ICommandParams p)
        {
            var message = string.Empty;
            var projectPath = string.Empty;

            // 1. 開始条件のチェック
            // ・Enterprise エディション
            var workspace = App.Workspace;
            var project = workspace.CurrentProject;
            if (!CheckEnterpriseEdition())
            {
                message = Messages.PartialLoadMigrationEnterpriseOnly;
                this.ShowOutputMessage(message);
                return;
            }
            // ・プロジェクト拡張子
            var ext = (project != null) ? Path.GetExtension(project.Path) : null;
            if ((ext != null) && (!string.Equals(ext, ".nproj")))
            {
                message = Messages.NotNprojExtension;
                this.ShowOutputMessage(message);
                return;
            }
            // ・ダーティ状態
            if ((project != null) && (project.HasUnsavedChanges()))
            {
                message = Messages.UnsavedProjectChanges;
                this.ShowOutputMessage(message);
                return;
            }

            //2. 対象プロジェクトを特定する。
            // ・開いていない場合はファイル選択ダイアログで指定
            // ・開いている場合はそのプロジェクトを記憶して閉じる
            var filter = Messages.FileDialogNprojFilterDescription + @"(*.nproj)|*.nproj";
            projectPath = (project == null) ? App.Window.UI.ShowOpenFileDialog(filter: filter) : project.Path;
            if (string.IsNullOrEmpty(projectPath))
            {
                // キャンセル
                return;
            }
            workspace.CloseProject();

            // 3. 開始メッセージを出力
            var nuserPath = Path.ChangeExtension(projectPath, ".nuser");
            message = string.Format(Messages.PartialLoadMigrationStartMessage, nuserPath);
            this.OutputMessage(message);

            //4. 対象プロジェクトと同じフォルダに nuser ファイルがあれば、手動ロード設定の拡張子をimdl->nmdl に変更する。
            var result = ConvertPartialLoadSettings(nuserPath);
            if (!result)
            {
                message = Messages.PartialLoadMigrationFailed;
                this.ShowOutputMessage(message);
                return;
            }

            //5. 対象プロジェクトを開く。
            message = string.Format(Messages.PartialLoadMigrationOpenProject, projectPath);
            this.OutputMessage(message);
            App.Workspace.OpenProject(projectPath);
            App.Window.EditorPage.ActiveNavigator = "Project";

            // 6. 完了メッセージを表示
            message = Messages.PartialLoadMigrationCompleted;
            this.ShowOutputMessage(message);
        }

        /// <summary>
        /// 現在のエディションがEnterpriseエディションか判定します。
        /// </summary>
        /// <returns>Enterpriseエディションの場合はtrue、それ以外はfalseです。</returns>
        private bool CheckEnterpriseEdition()
        {
            var edition = App.EditionId;
            return c_EnterpriseEditionIds.Contains(edition);
        }

        /// <summary>
        /// 指定されたnuserファイルの手動ロード設定を.imdlから.nmdlに変換します。
        /// </summary>
        /// <param name="nuserPath">変換対象のnuserファイルのパス。</param>
        /// <returns>変換処理に成功したらtrue、失敗したらfalseです。</returns>
        private bool ConvertPartialLoadSettings(string nuserPath)
        {
            try
            {
                if (!File.Exists(nuserPath))
                {
                    // 対象ファイルが存在しない場合
                    var message = string.Format(Messages.PartialLoadNotFound, nuserPath);
                    this.OutputMessage(message);
                    return true;
                }

                // ファイルを読み込む
                // ・BOM付きUTF-8 エンコーディング
                string text = File.ReadAllText(nuserPath, Encoding.UTF8);

                // ".imdl" を ".nmdl" に置換
                string pattern = @"(""FilePath""\s*:\s*""[^""]*?)\.imdl("")";
                string replaced = Regex.Replace(text, pattern, "$1.nmdl$2");

                // 変更がある場合のみ書き戻す
                if (!string.Equals(text, replaced, StringComparison.Ordinal))
                {
                    File.WriteAllText(nuserPath, replaced, Encoding.UTF8);
                }
            }
            catch (Exception ex)
            {
                this.OutputMessage(ex.Message);
                return false;
            }

            return true;
        }
    }
}
