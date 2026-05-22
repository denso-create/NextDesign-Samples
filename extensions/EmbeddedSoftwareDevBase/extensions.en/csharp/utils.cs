// =======================================
// General-purpose utility functions
// Define a general-purpose function that can be reused across different features.
// =======================================

// ---------------------------------------
// The model acquisition function currently selected in the editor
// Arguments: Command context
// Return value: The selected models (an empty collection if none are selected)
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
// The function for obtaining the model selected in the main editor
// Arguments: Command context
// Return value: The group of models currently selected in the main editor (an empty collection if none are selected)
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
// Model acquisition function selected in sub-editor
// Arguments: Command context
// Return value: The group of models currently selected in the sub-editor (an empty collection if none are selected).
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
// Selected Root Model Acquisition Function
// This retrieves the selected models that do not have any selected models as ancestors.
// Recursively search from the target model.
// Arguments: Model to search, selected model group, class name of the target model, list for storing results
// ---------------------------------------
private void CollectSelectedRootModels(IModel targetModel, List<IModel> selectedModels, string[] targetClasses, List<IModel> results)
{
    if (selectedModels.Contains(targetModel))
    {
        // If selected, it will be added to the results.
        results.Add(targetModel);
    }
    else
    {
        // If no model is selected, child models are recursively explored.
        var children = targetModel.GetChildren().Where(model => model.AsIn(targetClasses));
        foreach (var child in children)
        {
            CollectSelectedRootModels(child, selectedModels, targetClasses, results);
        }
    }
}