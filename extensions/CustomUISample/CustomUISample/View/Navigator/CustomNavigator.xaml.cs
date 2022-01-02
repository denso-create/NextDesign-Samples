using System;
using System.Collections.Generic;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using CustomUISample.ViewModel.Navigator;

namespace CustomUISample.View.Navigator
{
    /// <summary>
    /// CustomNavigator.xaml の相互作用ロジック
    /// </summary>
    public partial class CustomNavigator : UserControl
    {
        public CustomNavigator()
        {
            InitializeComponent();
        }

		/// <summary>
		/// ツリーの選択変更
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void TreeView_SelectedItemChanged(object sender, RoutedPropertyChangedEventArgs<object> e)
		{
			var vm = DataContext as CustomNavigatorViewModel;
			var itemVM = m_Tree.SelectedItem as CustomNavigatorItemViewModel;
			if (itemVM != null)
			{
				vm.SelectedItem = itemVM.Model;
			}
		}
	}
}
