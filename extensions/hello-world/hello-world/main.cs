// コマンドハンドラの公開関数
public void SayHello(ICommandContext context,ICommandParams paramemters)
{
	App.Window.UI.ShowInformationDialog("Hello !", "Hello World");
}