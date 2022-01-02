using System;
using CustomUISample.View.Editor;
using CustomUISample.View.Inspector;
using CustomUISample.View.Navigator;
using CustomUISample.ViewModel.Editor;
using CustomUISample.ViewModel.Inspector;
using CustomUISample.ViewModel.Navigator;
using NextDesign.Extension;
using NextDesign.Desktop;
using NextDesign.Desktop.CustomUI;

namespace CustomUISample
{
	public class CustomUISampleEntryPoint : IExtension
	{
		/// <summary>
		/// エクステンション活性化時の処理
		/// </summary>
		/// <param name="context"></param>
		public void Activate(IContext context)
		{
			var registry = context.App.CustomUI;
			var extensionName = context.ExtensionInfo.Name;

			// カスタムエディタの登録
			var customEditorDescriptor = new CustomEditorDescriptor(
				typeof(CustomEditorViewModel).FullName,
				CustomEditorViewModel.DefinitionDescriptor
			);
			registry.RegisterCustomEditor<CustomEditorViewModel, CustomEditor>(extensionName, customEditorDescriptor);

			// カスタムインスペクタの登録
			var customInspectorDescriptor = new CustomInspectorDescriptor(
				typeof(CustomInspector).FullName,
				"カスタムインスペクタ",
				(CustomInspectorDescriptor.DisplayOrderNodeShapeDefinition + 1)
			);
			registry.RegisterCustomInspector<CustomInspectorViewModel, CustomInspector>(extensionName, customInspectorDescriptor);

			// カスタムナビゲータの登録
			// モデルナビゲータとプロダクトラインの間に表示します
			var customNavigatorDescriptor = new CustomNavigatorDescriptor(
				typeof(CustomNavigator).FullName,
				"カスタムナビゲータ",
				(CustomNavigatorDescriptor.DisplayOrderModel + 1),
				@"pack://application:,,,/NextDesign;component/Resources/Images/ModelNavigator.png"
			);
			registry.RegisterCustomNavigator<CustomNavigatorViewModel, CustomNavigator>(extensionName, customNavigatorDescriptor);
		}

		/// <summary>
		/// エクステンション非活性化時の処理
		/// </summary>
		/// <param name="context"></param>
		public void Deactivate(IContext context)
		{
			var registry = context.App.CustomUI;
			var extensionName = context.ExtensionInfo.Name;

			// カスタムUIの登録解除
			registry.UnRegisterAllCustomUIs(extensionName);
		}
	}
}
