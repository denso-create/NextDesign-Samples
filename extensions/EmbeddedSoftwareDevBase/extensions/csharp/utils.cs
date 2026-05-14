// =======================================
// 汎用ユーティリティ関数群
// 異なる機能で使いまわせる汎用的な関数を定義します。
// =======================================

// ---------------------------------------
// 現在のエディタで選択中のモデル取得関数
// 引数：コマンドコンテキスト
// 戻り値：選択中のモデル群（選択されていない場合は空のコレクション）
// ---------------------------------------
private IEnumerable<IModel> GetSelectedModels(ICommandContext context)
{
    var models = context.App.Window.EditorPage?.CurrentEditorView?.SelectedModels;

    if (models == null || !models.Any())
    {
        return Enumerable.Empty<IModel>();
    }

    return models;
}

// ---------------------------------------
// メインエディタで選択中のモデル取得関数
// 引数：コマンドコンテキスト
// 戻り値：メインエディタで選択中のモデル群（選択されていない場合は空のコレクション）
// ---------------------------------------
private IEnumerable<IModel> GetSelectedModelsInMainEditor(ICommandContext context)
{
    var models = context.App.Window.EditorPage?.MainEditorView?.SelectedModels;

    if (models == null || !models.Any())
    {
        return Enumerable.Empty<IModel>();
    }

    return models;
}

// ---------------------------------------
// サブエディタで選択中のモデル取得関数
// 引数：コマンドコンテキスト
// 戻り値：サブエディタで選択中のモデル群（選択されていない場合は空のコレクション）
// ---------------------------------------
private IEnumerable<IModel> GetSelectedModelsInSubEditor(ICommandContext context)
{
    var models = context.App.Window.EditorPage?.SubEditorView?.SelectedModels;

    if (models == null || !models.Any())
    {
        return Enumerable.Empty<IModel>();
    }

    return models;
}

// ---------------------------------------
// 選択ルートモデル取得関数
// 選択されているモデルのうち、祖先に選択されたモデルを持たないものを取得します。
// 探索対象モデルから再帰的に探索します。
// 引数:探索対象モデル、選択モデル群、対象とするモデルのクラス名、結果格納用リスト
// ---------------------------------------
private void CollectSelectedRootModels(IModel targetModel, List<IModel> selectedModels, string[] targetClasses, List<IModel> results)
{
    if (selectedModels.Contains(targetModel))
    {
        // 選択中の場合は、結果に追加します。
        results.Add(targetModel);
    }
    else
    {
        // 選択中でない場合は、子モデルを再帰的に探索します。
        var children = targetModel.GetChildren().Where(model => model.AsIn(targetClasses));
        foreach (var child in children)
        {
            CollectSelectedRootModels(child, selectedModels, targetClasses, results);
        }
    }
}