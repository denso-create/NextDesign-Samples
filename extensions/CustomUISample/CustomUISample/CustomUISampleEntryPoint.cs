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
		/// �G�N�X�e���V�������������̏���
		/// </summary>
		/// <param name="context"></param>
		public void Activate(IContext context)
		{
			var registry = context.App.CustomUI;
			var extensionName = context.ExtensionInfo.Name;

			// �J�X�^���G�f�B�^�̓o�^
			var customEditorDescriptor = new CustomEditorDescriptor(
				typeof(CustomEditorViewModel).FullName,
				CustomEditorViewModel.DefinitionDescriptor
			);
			registry.RegisterCustomEditor<CustomEditorViewModel, CustomEditor>(extensionName, customEditorDescriptor);

			// �J�X�^���C���X�y�N�^�̓o�^
			var customInspectorDescriptor = new CustomInspectorDescriptor(
				typeof(CustomInspector).FullName,
				"�J�X�^���C���X�y�N�^",
				(CustomInspectorDescriptor.DisplayOrderNodeShapeDefinition + 1)
			);
			registry.RegisterCustomInspector<CustomInspectorViewModel, CustomInspector>(extensionName, customInspectorDescriptor);

			// �J�X�^���i�r�Q�[�^�̓o�^
			// ���f���i�r�Q�[�^�ƃv���_�N�g���C���̊Ԃɕ\�����܂�
			var customNavigatorDescriptor = new CustomNavigatorDescriptor(
				typeof(CustomNavigator).FullName,
				"�J�X�^���i�r�Q�[�^",
				(CustomNavigatorDescriptor.DisplayOrderModel + 1),
				@"pack://application:,,,/NextDesign;component/Resources/Images/ModelNavigator.png"
			);
			registry.RegisterCustomNavigator<CustomNavigatorViewModel, CustomNavigator>(extensionName, customNavigatorDescriptor);
		}

		/// <summary>
		/// �G�N�X�e���V�����񊈐������̏���
		/// </summary>
		/// <param name="context"></param>
		public void Deactivate(IContext context)
		{
			var registry = context.App.CustomUI;
			var extensionName = context.ExtensionInfo.Name;

			// �J�X�^��UI�̓o�^����
			registry.UnRegisterAllCustomUIs(extensionName);
		}
	}
}
