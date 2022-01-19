using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NextDesign.Extension;
using NextDesign.Core;
using NextDesign.Desktop;
using ExcelImportExtension.DataReader;
using ExcelImportExtension.ModelBuilder;

namespace ExcelImportExtension
{
	/// <summary>
	/// Excelインポートエクステンションのエントリーポイントとなるクラス
	/// </summary>
	public class ExcelImportExtension : IExtension
	{
		private IContext m_Context;

		/// <summary>
		/// Excelインポートボタンの処理を実行する。
		/// </summary>
		public void Run(ICommandContext context, ICommandParams parameters)
		{
			try
			{
				// ---------------------------------------------------
				// インポート先が「ソフト構造」であることをチェックします。
				// ---------------------------------------------------
				var targetModel = m_Context.App.Window.EditorPage.CurrentModel;
				if (!targetModel.ClassName.Equals("SoftwareStructureModel"))
				{
					m_Context.App.Window.UI.ShowInformationDialog(
						"ソフト構造モデルを表示させてから実行してください。",
						"Excel Import Extension"
					);
					return;
				}

				// ---------------------------------------------------
				// Excel ファイルを選択します。
				// ---------------------------------------------------
				var filter = "Excel Files (*.xls, *.xlsx)|*.xls;*.xlsx";
				var filePath = m_Context.App.Window.UI.ShowOpenFileDialog(filter: filter);
				if (string.IsNullOrEmpty(filePath))
				{
					return;
				}

				// ---------------------------------------------------
				// Excel ファイルからデータを読み込みます。
				// ---------------------------------------------------
				var excelReader = new ExcelReader();
				var layerDtos = excelReader.Read(filePath);

				// ---------------------------------------------------
				// 読み込んだデータを Next Design に書き込みます。
				// ---------------------------------------------------
				var modelBuilder = new SoftwareStructureModelBuilder();
				foreach (var layerDto in layerDtos)
				{
					modelBuilder.AddStructuredModel(targetModel, "Layers", layerDto);
				}

				// ---------------------------------------------------
				// 完了メッセージを表示します。
				// ---------------------------------------------------
				m_Context.App.Window.UI.ShowInformationDialog(
					"Excel ファイルをインポートしました。",
					"Excel Import Extension"
				);
			}
			catch (System.Exception ex)
			{
				ShowOutputPane();
				m_Context.App.Output.WriteLine("デフォルト", ex.Message);
			}
		}

		/// <summary>
		/// エクステンションを活性化する。
		/// </summary>
		/// <param name="context">実行コンテキスト</param>
		public void Activate(IContext context)
		{
			m_Context = context;
		}

		/// <summary>
		/// エクステンションを非活性化する。
		/// </summary>
		/// <param name="context">実行コンテキスト</param>
		public void Deactivate(IContext context)
		{
			// Nothing
		}

		private void ShowOutputPane()
		{
			m_Context.App.Window.IsInformationPaneVisible = true;
			m_Context.App.Window.ActiveInfoWindow = "Output";
		}
	}
}
