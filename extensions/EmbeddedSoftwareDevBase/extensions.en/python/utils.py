"""General-purpose utility functions

Define a general-purpose function that can be reused across different features.
"""

from typing import TYPE_CHECKING, List  # TYPE_CHECKING and types for annotations.

# Importing nd outside main.py causes runtime errors.
# Therefore, import only during type checking.
if TYPE_CHECKING:
    from nd import *

def get_selected_models(context: "ICommandContext") -> List["IModel"]:
    """The model acquisition function currently selected in the editor

    Args:
        context: Command context
    Returns:
        The selected models (an empty list if none are selected)
    """
    models = None
    if context.App.Window.EditorPage and context.App.Window.EditorPage.CurrentEditorView:
        models = context.App.Window.EditorPage.CurrentEditorView.SelectedModels

    if models is None:
        return []

    return list(models)

def get_selected_models_in_main_editor(context: "ICommandContext") -> List["IModel"]:
    """The function for obtaining the model selected in the main editor

    Args:
        context: Command context
    Returns:
        The group of models currently selected in the main editor (an empty list if none are selected)
    """
    models = None
    if context.App.Window.EditorPage and context.App.Window.EditorPage.MainEditorView:
        models = context.App.Window.EditorPage.MainEditorView.SelectedModels

    if models is None:
        return []

    return list(models)

def get_selected_models_in_sub_editor(context: "ICommandContext") -> List["IModel"]:
    """Model acquisition function selected in sub-editor

    Args:
        context: Command context
    Returns:
        The group of models currently selected in the sub-editor (an empty list if none are selected).
    """
    models = None
    if context.App.Window.EditorPage and context.App.Window.EditorPage.SubEditorView:
        models = context.App.Window.EditorPage.SubEditorView.SelectedModels

    if models is None:
        return []

    return list(models)

def collect_selected_root_models(
    target_model: "IModel",
    selected_models: List["IModel"],
    target_classes: List[str],
    results: List["IModel"]
) -> None:
    """Selected Root Model Acquisition Function
    This retrieves the selected models that do not have any selected models as ancestors.
    Recursively search from the target model.

    Args:
        target_model: Model to search
        selected_models: Selected model group
        target_classes: Class name of the target model
        results: List for storing results
    """
    if target_model in selected_models:
        # If selected, it will be added to the results.
        results.append(target_model)
    else:
        # If no model is selected, child models are recursively explored.
        children = [model for model in target_model.GetChildren() if model.AsIn(classNames=target_classes)]
        for child in children:
            collect_selected_root_models(child, selected_models, target_classes, results)
