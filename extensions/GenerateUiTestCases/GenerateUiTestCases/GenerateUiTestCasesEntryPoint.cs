using NextDesign.Desktop;
using NextDesign.Extension;
using System;
using System.Linq;
using System.Windows;

namespace GenerateUiTestCases
{
    /// <summary>
    /// エクステンションのエントリポイントです
    /// </summary>
    public class GenerateUiTestCasesEntryPoint : IExtension
    {
        /// <summary>
        /// アプリケーション
        /// </summary>
        private IApplication App { get; set; }

        #region Activate/Deactivate

        /// <summary>
        /// エクステンションの初期化時の処理です。
        /// </summary>
        /// <param name="context">エクステンションのコンテキストです。</param>
        public void Activate(IContext context)
        {
            App = context.App;
        }

        /// <summary>
        /// エクステンションの終了前の処理です。
        /// </summary>
        /// <param name="context">エクステンションのコンテキストです。</param>
        public void Deactivate(IContext context)
        {
        }

        #endregion


        #region Commands

        /// <summary>
        /// UI画面の操作仕様から動作確認のためのテストケースを自動作成します。
        /// </summary>
        /// <param name="c">コマンドコンテキスト</param>
        /// <param name="p">コマンドパラメータ</param>
        public void GenerateUiTestCases(ICommandContext c, ICommandParams p)
        {
            // 前提条件を確認します。
            var project = App.Workspace.CurrentProject;
            var uiModel = App.Window.EditorPage?.CurrentEditorView?.Editor?.Model;
            if ((uiModel == null) || (! uiModel.As("UiWindow")))
            {
                App.Window.UI.ShowMessageBox("対象のUI画面を表示させてから実行してください。");
                return;
            }
            var testGroupModel = project.FindChildrenByClass("TestGroup", recursive: true).FirstOrDefault();
            if (testGroupModel == null)
            {
                App.Window.UI.ShowMessageBox("テストグループを作成してから実行してください。");
                return;
            }

            // モデルエディタに表示されているUI画面の中からUI部品の操作仕様を抽出します。
            var operationModels = uiModel.FindChildrenByClass("OperationSpec", recursive: true);

            // 操作仕様に対応したテストケースを作成します。
            foreach (var operationModel in operationModels)
            {
                var testCaseModel = testGroupModel.AddNewModel("TestCases", "TestCase");
                
                // 操作仕様に基づいてテストケースの名前と期待値を設定します。
                var uiElementName = operationModel.Owner.Name;          // UI部品の名前
                var operation = operationModel.Name;                    // 操作
                var action = operationModel.GetFieldString("Action");   // 動作

                var testCaseLabel = $"{uiElementName}・{operation}";    // テストケースの名前
                var expectedValue = $"{uiElementName}が{operation}されると、{action}";  // 期待値
                testCaseModel.SetField("Name", testCaseLabel);
                testCaseModel.SetField("ExpectedValue", expectedValue);

                // 操作仕様とテストケース間にトレース関連（導出関連）を結びます。
                testCaseModel.Relate("input_OperationSpec", operationModel);
            }
        }

        #endregion

    }
}
