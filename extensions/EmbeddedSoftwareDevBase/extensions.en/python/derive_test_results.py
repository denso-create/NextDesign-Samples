"""Function: Derives Test Result models.

This function creates Test Result Group/Test Result with the same hierarchical structure 
as the Test Case Group selected in the main editor, all under the Test Result Group selected in the sub-editor.
Sets up the derivation relationship from Test Case to Test Result.
General Information model will be added to the created Test Result Group.

Processing Overview
    - This checks if the selected model is invalid.
    - Retrieves the Test Case Group from which the derivation originated.
    - The source Test Case Group is recursively scanned and added to the Test Result Group.
"""

# =======================================
# Importing external files and modules
# =======================================
from typing import TYPE_CHECKING  # TYPE_CHECKING for type-only nd import.
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
# Array of process information
# Define the information for each process.
# You can add new steps by adding elements to this array.
# ---------------------------------------
DERIVE_TARGET_PROCESS_CLASS_NAMES = [
    # Software Test Process
    metamodel.TestProcessClassNames(
        process_class=metamodel.CLASS_NAME_SOFTWARE_TEST,
        test_cases_group_class=metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST,
        test_case_class=metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_TEST,
        test_results_group_class=metamodel.CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_TEST,
        test_result_class=metamodel.CLASS_NAME_TEST_RESULT_SOFTWARE_TEST,
    ),
    # Software Component Test Process
    metamodel.TestProcessClassNames(
        process_class=metamodel.CLASS_NAME_SOFTWARE_COMPONENT_TEST,
        test_cases_group_class=metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST,
        test_case_class=metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST,
        test_results_group_class=metamodel.CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_COMPONENT_TEST,
        test_result_class=metamodel.CLASS_NAME_TEST_RESULT_SOFTWARE_COMPONENT_TEST,
    ),
    # Software Integration Test Process
    metamodel.TestProcessClassNames(
        process_class=metamodel.CLASS_NAME_SOFTWARE_INTEGRATION_TEST,
        test_cases_group_class=metamodel.CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST,
        test_case_class=metamodel.CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST,
        test_results_group_class=metamodel.CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_INTEGRATION_TEST,
        test_result_class=metamodel.CLASS_NAME_TEST_RESULT_SOFTWARE_INTEGRATION_TEST,
    )
]

# ---------------------------------------
# Messages (user notifications)
# This is the text displayed when adding a dialog box or error message.
# ---------------------------------------
# Message to display in the dialog box
DIALOG_MSG_NO_SELECTED_TEST_CASE_GROUP = "Please select the source Test Case group in the main editor."
DIALOG_MSG_HAS_MULTIPLE_CLASSES = "Please select the same type for all Test Case Group used for derivation."
DIALOG_MSG_SUB_EDITOR_INVALID = "In the sub-editor, select one Test Result Group to which the derived model will be added."
DIALOG_MSG_DIFFERENT_PROCESSES_SELECTED = "The process for the selected Test Case Group and the Test Result Group is different."

# Derivation process notification
ERROR_TITLE_DERIVE_TEST_RESULTS = "Derives Test Result models"
ERROR_MSG_TEST_RESULTS_CREATED = "A model has been created."

# =======================================
# Main processing function
# The function defined here is linked to the Command in manifest.json.
# =======================================
def derive_test_results(context: "ICommandContext", parameters: "ICommandParams") -> None:
    """Creates a similar structure in the selected Test Result Group,
    based on the selected Test Case Group in the main editor.
    This is a command handler linked to the Command in manifest.json.
    """
    # 1. Retrieve the model currently selected in the main editor and sub-editor.
    # Retrieves the model and Test Case Group currently selected in the main editor.
    test_cases_group_classes = [p.test_cases_group_class for p in DERIVE_TARGET_PROCESS_CLASS_NAMES]
    selected_models_main = utils.get_selected_models_in_main_editor(context)
    selected_test_cases_groups = [model for model in selected_models_main if model.AsIn(classNames=test_cases_group_classes)]

    # Gets the currently selected model in the sub-editor.
    selected_models_sub = utils.get_selected_models_in_sub_editor(context)

    # 2. Verify that the correct model is selected. If incorrect, display a dialog box and exit.
    # 2.1. Ensure that at least one Test Case Group is selected in the main editor.
    if not selected_test_cases_groups:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_SELECTED_TEST_CASE_GROUP)
        return

    # 2.2. All Test Case Group selected in the main editor must be of the same type.
    first = selected_test_cases_groups[0] if selected_test_cases_groups else None
    if not all(model.ClassName == first.ClassName for model in selected_test_cases_groups):
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_HAS_MULTIPLE_CLASSES)
        return

    # 2.3. The sub-editor is displayed, and there is one model selected in the sub-editor.
    if not context.App.Window.EditorPage.IsSubEditorVisible or len(selected_models_sub) != 1:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_SUB_EDITOR_INVALID)
        return

    # This retrieves the process to which the currently selected Test Case Group in the main editor belongs.
    representative = selected_test_cases_groups[0] if selected_test_cases_groups else None
    target_process = next(
        (process for process in DERIVE_TARGET_PROCESS_CLASS_NAMES if process.test_cases_group_class == representative.ClassName),
        None
    )
    process_root = representative.FindOwnerByClass(target_process.process_class)

    # 2.4. The class selected in the sub-editor must correspond to the class selected in the main editor.
    if selected_models_sub[0].ClassName != target_process.test_results_group_class:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DIFFERENT_PROCESSES_SELECTED)
        return

    # 3. Obtain the source and destination of the derivation.
    # Retrieves the Test Case Group from which the derivation originated.
    src_groups = []
    utils.collect_selected_root_models(process_root, selected_test_cases_groups, [target_process.test_cases_group_class], src_groups)

    # Retrieves the derived Test Result Group.
    dst_group = selected_models_sub[0]

    # 4. Perform the derivation.
    # The contents of the error window will be cleared before execution.
    context.App.Errors.ClearErrors()

    # The source Test Case Group is recursively traversed, and a similar structure is created under the Test Result Group.
    for src_group in src_groups:
        new_model = dst_group.AddNewModel(metamodel.FIELD_NAME_TEST_RESULTS_SUB_GROUPS, target_process.test_results_group_class)
        new_model.SetField(metamodel.FIELD_NAME_NAME, src_group.Name)

        # Information notifications are registered in the child model added directly under the derived model.
        new_model.AddError(metamodel.FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_TEST_RESULTS, ERROR_MSG_TEST_RESULTS_CREATED)

        _derive_child_test_results(src_group, new_model, target_process)

# =======================================
# Sub processing function
# =======================================
def _derive_child_test_results(
    test_cases_group: "IModel",
    test_results_group: "IModel",
    target_process: metamodel.TestProcessClassNames
) -> None:
    """Function for deriving Test result for descendants.
    Create a structure similar to the source Test Case Group under the destination Test Result Group.
    However, we will add a General Information model to the Test Result Group.

    Args:
        test_cases_group: Source Test Case Group
        test_results_group: Destination Test Result Group
        target_process: Class name of the target process
    """
    # Add the General Information model to the Test Result Group.
    test_results_group.AddNewModel(metamodel.FIELD_NAME_TEST_RESULTS_SUMMARY, metamodel.CLASS_NAME_TEST_RESULTS_SUMMARY)

    # Scan the child models of the derived Test Case Group.
    children = test_cases_group.GetChildren()
    for model in children:
        if model.As(target_process.test_cases_group_class):
            # Add a Test Result Group to the Test Result Group.
            new_model = test_results_group.AddNewModel(metamodel.FIELD_NAME_TEST_RESULTS_SUB_GROUPS, target_process.test_results_group_class)
            new_model.SetField(metamodel.FIELD_NAME_NAME, model.Name)

            # Derive descendant models starting from the added model.
            _derive_child_test_results(model, new_model, target_process)
        elif model.As(target_process.test_case_class):
            # Add the Test Result to the Test Result Group.
            new_model = test_results_group.AddNewModel(metamodel.FIELD_NAME_TEST_RESULTS, target_process.test_result_class)
            new_model.SetField(metamodel.FIELD_NAME_NAME, model.Name)
            new_model.SetField(metamodel.FIELD_NAME_TEST_CASES, model)
        else:
            # Ignore everything except Test Case Group and Test Case.
            pass
