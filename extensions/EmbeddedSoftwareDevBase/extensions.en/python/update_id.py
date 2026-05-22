"""Function: Update ID

This command reassigns the IDs of the selected model and its descendants to be unique in bulk.
IDs are assigned uniquely to each process.

Processing Overview
    - Retrieve the models to be updated.
    - Find the maximum value of existing IDs from models that are not being updated.
    - Start with the maximum value of the calculated ID + 1 and assign IDs sequentially.
    - The results will be notified via a dialog box and an added error message.
"""

# =======================================
# Importing external files and modules
# =======================================
from typing import TYPE_CHECKING, List, Tuple  # TYPE_CHECKING and types for annotations.
import re        # Modules for using regular expressions
import utils      # General-purpose function
import metamodel  # Metamodel information such as class names

# Importing nd outside main.py causes runtime errors.
# Therefore, import only during type checking.
if TYPE_CHECKING:
    from nd import *

# =======================================
# User-defined settings (parameters)
# You can edit this area to change the target of the operation or the message.
# =======================================

# ---------------------------------------
# Data structure definition
# ---------------------------------------

# A structure that centrally manages the information necessary to update the ID for each process.
class ProcessIdConfig:
    def __init__(self, root_classes: List[str], start_classes: List[str], target_classes: List[str], prefix: str) -> None:
        self.root_classes = root_classes      # An array of class names that serve as the root of the process (used to retrieve all models for each process).
        self.start_classes = start_classes    # An array of starting class names (used to determine the selection model for each process)
        self.target_classes = target_classes  # An array of class names to be updated (used to determine which IDs should be updated)
        self.prefix = prefix                  # ID prefix (e.g., "SYRQ-")

# ---------------------------------------
# Array of process information
# Define the information for each process.
# You can add new steps by adding elements to this array.
# ---------------------------------------
PROCESS_ID_CONFIGS = [
    # System Requirement Analysis Process
    ProcessIdConfig(
        root_classes=[metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS],
        start_classes=[metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS, metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, metamodel.CLASS_NAME_SYSTEM_REQUIREMENT],
        target_classes=[metamodel.CLASS_NAME_SYSTEM_REQUIREMENT],
        prefix="SYRQ-"
    ),
    # Software Requirement Analysis Process
    ProcessIdConfig(
        root_classes=[metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS],
        start_classes=[metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT],
        target_classes=[metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT],
        prefix="SWRQ-"
    ),
    # Software Component Test Process
    ProcessIdConfig(
        root_classes=[metamodel.CLASS_NAME_SOFTWARE_COMPONENT_TEST],
        start_classes=[metamodel.CLASS_NAME_SOFTWARE_COMPONENT_TEST, metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST, metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST],
        target_classes=[metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST],
        prefix="SWCT-"
    ),
    # Software Integration Test Process
    ProcessIdConfig(
        root_classes=[metamodel.CLASS_NAME_SOFTWARE_INTEGRATION_TEST],
        start_classes=[metamodel.CLASS_NAME_SOFTWARE_INTEGRATION_TEST, metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST, metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST],
        target_classes=[metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST],
        prefix="SWIT-"
    ),
    # Software Test Process
    ProcessIdConfig(
        root_classes=[metamodel.CLASS_NAME_SOFTWARE_TEST],
        start_classes=[metamodel.CLASS_NAME_SOFTWARE_TEST, metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST, metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_TEST],
        target_classes=[metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_TEST],
        prefix="SWTT-"
    )
]

# ---------------------------------------
# Definition related to ID
# ---------------------------------------
UPDATE_ID_DIGITS = 6  # Number of digits in the ID

# ---------------------------------------
# Messages (user notifications)
# This is the text displayed when adding a dialog box or error message.
# ---------------------------------------
DIALOG_MSG_NO_UPDATE_TARGET_SELECTED = "Please select the model with an ID, or the ancestor model of the model with an ID, in the editor."
DIALOG_MSG_HAS_FAILED_ID = "There is a model whose ID update failed.\nPlease check the error window."
DIALOG_NO_ID_UPDATED = "There were no models that were eligible for update."
ERROR_TITLE_UPDATE_ID = "ID update"
ERROR_MSG_SUCCESS_UPDATE_ID = "{0} has been set."
ERROR_MSG_FAILED_UPDATE_ID = "The sequence number exceeded the maximum value, so the values were cleared."

# =======================================
# Main processing function
# The function defined here is linked to the Command in manifest.json.
# =======================================
def update_id(context: "ICommandContext", parameters: "ICommandParams") -> None:
    """Reassigns IDs in bulk for the selected models and their descendants.
    This is a command handler linked to the Command in manifest.json.
    """
    # 1. Obtain the selection model and create an array of selection models for each process.
    # Gets the model currently selected in the editor.
    selected_models = utils.get_selected_models(context)
    
    # For each step, we extract only the "selected models that correspond to the starting class (StartClasses)" and group them into an array.
    # Example: If only one Software Requirement model is selected,
    #    selected_models_by_process = [[], [Software Requirement model], []]
    selected_models_by_process = [
        [model for model in selected_models if model.AsIn(classNames=process.start_classes)]
        for process in PROCESS_ID_CONFIGS
    ]

    # 2. Check if at least one model corresponding to the starting class has been selected.
    if not any(models for models in selected_models_by_process):
        # If not selected, a dialog box will appear and the operation will end.
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_UPDATE_TARGET_SELECTED)
        return
    
    # 3. Update the ID for each process.
    # Clear all existing errors.
    context.App.Errors.ClearErrors()

    # Retrieves the model directly under the project.
    root_children = list(context.App.Workspace.CurrentProject.DesignModel.GetChildren())

    # 4. Execute the ID update process for each step.
    for config, selected in zip(PROCESS_ID_CONFIGS, selected_models_by_process):
        # Retrieve the model directly under the project for each process.
        process_root_models = [model for model in root_children if model.AsIn(classNames=config.root_classes)]

        # The ID update process will be executed.
        _update_ids_for_process(
            config,
            selected,
            process_root_models
        )

    # 5. We will notify you of the processing results.
    _show_result_notification(context.App.Errors, context.App.Window)

# =======================================
# Sub processing function
# =======================================
def _update_ids_for_process(process_info: ProcessIdConfig, selected_models: List["IModel"], root_models: List["IModel"]) -> None:
    """ID update function for one step
    The IDs of the selected model and its descendant models within the process will be updated.
    The maximum value of existing IDs is obtained from models that are not targeted,
    and IDs are assigned starting from the maximum value + 1,
    so that they are in order from top to bottom in the Model Navigator.
    If the ID exceeds the maximum value that can be set, an error will occur and an empty string will be set.

    Args:
        process_info: Process information
        selected_models: Selection model
        root_models: Model of the target process root
    """
    # 1. Retrieve all models that correspond to the class to be updated within the process.
    all_target_class_models = []
    for model in root_models:
        for child in model.GetAllChildren():
            if child.AsIn(classNames=process_info.target_classes):
                all_target_class_models.append(child)
    
    # 2. Retrieve the model to be updated.
    target_models, other_models = _split_models_into_target_and_others(all_target_class_models, selected_models, process_info.target_classes)

    # 3. Obtain the maximum ID value from the models that are not to be updated.
    max_id = get_max_id(other_models, metamodel.FIELD_NAME_ID, process_info.prefix)

    # 4. Update the IDs.
    updated_models, error_models = set_sequential_ids(
        target_models,
        max_id + 1,
        process_info.prefix
    )

    # 5. Grant notifications.
    for model in updated_models:
        # Successful models will have errors (type = information) added to them.
        new_id = model.GetFieldString(metamodel.FIELD_NAME_ID)
        model.AddError(metamodel.FIELD_NAME_ID, "Information", ERROR_TITLE_UPDATE_ID, ERROR_MSG_SUCCESS_UPDATE_ID.format(new_id))
    for model in error_models:
        # For models that have errors, an error (type=error) will be added.
        model.AddError(metamodel.FIELD_NAME_ID, "Error", ERROR_TITLE_UPDATE_ID, ERROR_MSG_FAILED_UPDATE_ID)

def _split_models_into_target_and_others(models: List["IModel"], selected_models: List["IModel"], target_class_names: List[str]) -> Tuple[List["IModel"], List["IModel"]]:
    """Function to determine which models should be updated and which should not.
    Divide them into the following two categories.
    - Models to be updated: The selected model and its descendant models that fall under the target class of the specified process.
    - Models not included in the update: All models that fall under the target class of the specified process, excluding those listed above.

    Args:
        models: All models
        selected_models: Selected models
        target_class_names: Array of target class names
    Returns:
        Models to be updated, models not to be updated
    """
    # This retrieves the models from the selected model and its descendants that belong to the target class.
    selected_with_children_ids = set()
    for model in selected_models:
        for child in [model] + list(model.GetAllChildren()):
            if child.AsIn(classNames=target_class_names):
                selected_with_children_ids.add(child.Id)

    # Separate the models into those that will be updated and those that will not.
    target_models = []
    other_models = []
    for model in models:
        if model.Id in selected_with_children_ids:
            target_models.append(model)
        else:
            other_models.append(model)

    return target_models, other_models

def get_max_id(models: List["IModel"], field_name: str, prefix: str) -> int:
    """ID Maximum Value Calculation Function
    Retrieve the maximum ID value from the received models.

    Args:
        models: Model
        field_name: ID field name
        prefix: ID prefix
    Returns:
        Maximum ID
    """
    models_list = list(models)
    if not models_list:
        # If the received model is empty, it returns 0.
        return 0

    # This retrieves the maximum value of IDs that match the naming convention.
    # This generates a regular expression from the prefix and number of digits.
    regex_pattern = f"^{re.escape(prefix)}(?P<num>[0-9]{{{UPDATE_ID_DIGITS}}})$"
    regex = re.compile(regex_pattern)

    max_id = 0
    for model in models_list:
        id_str = model.GetFieldString(field_name)

        # Use regular expressions to check if the naming convention matches.
        match = regex.match(id_str)
        if not match:
            # If the naming convention is not followed, it will be ignored.
            continue

        # This function extracts the numerical portion from the ID string and converts it to an integer.
        # For example, in the case of "SYRQ-000123", "000123" is extracted and converted to 123.
        num = int(match.group("num"))
        if num > max_id:
            max_id = num

    return max_id

def set_sequential_ids(target_models: List["IModel"], start_id_number: int, prefix: str) -> Tuple[List["IModel"], List["IModel"]]:
    """Sequential ID setting function
    The specified value will be used as the initial value, and sequential IDs will be assigned to all models.
    If the ID exceeds the maximum value, an empty string will be set to the model's ID.

    Args:
        target_models: Model to update
        start_id_number: Starting ID value
        prefix: ID prefix
    Returns:
        Successful models, models that failed due to exceeding the maximum value
    """
    updated_models = []
    error_models = []
    next_id_number = start_id_number

    max_id_number = 10 ** UPDATE_ID_DIGITS

    # Assign an ID to each model.
    for model in target_models:
        if next_id_number >= max_id_number:
            # If the ID exceeds the maximum value, an empty string will be set.
            model.SetField(metamodel.FIELD_NAME_ID, "")
            error_models.append(model)
            continue

        # A new ID will be generated.
        new_id = f"{prefix}{next_id_number:0{UPDATE_ID_DIGITS}d}"
        current_id = model.GetFieldString(metamodel.FIELD_NAME_ID)

        if current_id != new_id:
            # If the current ID is different from the original, set a new ID.
            model.SetField(metamodel.FIELD_NAME_ID, new_id)
            updated_models.append(model)

        next_id_number += 1

    return updated_models, error_models

def _show_result_notification(errors: "IErrors", window: "IWorkspaceWindow") -> None:
    """Result notification function
    Send you a notification based on the processing result.
    An error window will be displayed, and a dialog box notification will be sent depending on the processing result.

    Args:
        errors: Error information
        window: Window object for UI operation
    """
    # This retrieves whether or not there are any errors.
    has_error = bool(list(errors.Errors))
    has_changed = bool(list(errors.Informations))

    # An error window will be displayed.
    if has_error or has_changed:
        window.IsInformationPaneVisible = True
        window.ActiveInfoWindow = "Error"

    # Send user notifications based on the processing results.
    if has_error:
        window.UI.ShowInformationDialog(DIALOG_MSG_HAS_FAILED_ID)
    elif not has_changed:
        window.UI.ShowInformationDialog(DIALOG_NO_ID_UPDATED)
