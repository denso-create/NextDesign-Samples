"""Function: Aggregates Test Results

The test results are aggregated and the fields are updated for the General Information of the selected model and all models under it.
When the General Information is updated, an error (Type: Information) is added to the corresponding General Information model.

Processing Overview
    - Check if the target model is selected.
    - Retrieves the target test result group.
    - The data for the target test result group is aggregated from the lowest level downwards, and the General Information is updated.
"""

# =======================================
# Importing external files and modules
# =======================================
from typing import TYPE_CHECKING, List  # TYPE_CHECKING and types for annotations.
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

# A structure for aggregating test results.
class TestResultsCounts:
    def __init__(self) -> None:
        self.planned = 0   # Number of planned test cases
        self.actual = 0    # Actual number of test cases
        self.ok = 0        # Number of OK test cases
        self.ng = 0        # Number of Failed test cases
        self.not_run = 0   # Number of unexecuted test cases
        self.excluded = 0  # Number of excluded test cases

# ---------------------------------------
# Array of process information
# Define the information for each process.
# You can add new steps by adding elements to this array.
# ---------------------------------------
COUNT_TARGET_PROCESS_CLASS_NAMES = [
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
DIALOG_MSG_NO_GROUP_OR_SUMMARY_SELECTED = "Please select the Test Result Group or General Information in the editor."
DIALOG_MSG_NO_UPDATED_SUMMARY = "There were no models that were eligible for update."
ERROR_TITLE_UPDATE_TEST_RESULTS_SUMMARY = "Aggregates Test Results"
ERROR_MSG_UPDATED_TEST_CASE_COUNTS = "The number of test cases has been updated."

# =======================================
# Main processing function
# The function defined here is linked to the Command in manifest.json.
# =======================================
def count_test_results(context: "ICommandContext", parameters: "ICommandParams") -> None:
    """Aggregates test results and updates fields in the General Information
    of the selected model and all models under it.
    This is a command handler linked to the Command in manifest.json.
    """
    # 1. Retrieve the model that corresponds to the target class from the models currently selected in the editor.
    target_classes = [p.test_results_group_class for p in COUNT_TARGET_PROCESS_CLASS_NAMES] + [metamodel.CLASS_NAME_TEST_RESULTS_SUMMARY]
    selected_models = [model for model in utils.get_selected_models(context) if model.AsIn(classNames=target_classes)]

    # 2. Verify that the model corresponding to the target class is selected.
    if not selected_models:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_GROUP_OR_SUMMARY_SELECTED)
        return

    # 3. Retrieve the process to which the selected model belongs.
    representative = selected_models[0]
    target_process = next(
        process for process in COUNT_TARGET_PROCESS_CLASS_NAMES
        if representative.FindOwnerByClass(process.process_class) is not None
    )
    process_root = representative.FindOwnerByClass(target_process.process_class)

    # 4. Retrieve the target Test Result Group.
    target_groups = _get_target_test_results_groups(process_root, selected_models, target_process.test_results_group_class)

    # 5. Update the General Information of child models.
    context.App.Errors.ClearErrors()
    for target_group in target_groups:
        _count_and_update_summary(target_group, target_process)

    # 6. Output the results.
    errors = list(context.App.Workspace.CurrentProject.GetAllErrorsWithChildren())
    if errors:
        # If any changes occur, an error window will be displayed.
        context.App.Window.IsInformationPaneVisible = True
        context.App.Window.ActiveInfoWindow = "Error"
    else:
        # If there are no changes, a dialog box will notify you.
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_UPDATED_SUMMARY)

# =======================================
# Sub processing function
# =======================================
def _get_target_test_results_groups(root: "IModel", selected_models: List["IModel"], target_class: str) -> List["IModel"]:
    """Function to retrieve target Test Result Group
    This retrieves the selected group/general information that does not have an ancestor in the selected group.
    Search recursively from the root model.

    Args:
        root: Search root model
        selected_models: Selection model group
        target_class: Class name of the target group
    Returns:
        List of results
    """
    results = []

    if root in selected_models:
        # If selected, it will be added to the results.
        results.append(root)
        return results

    test_results_summary = next(
        (model for model in root.GetChildren() if model.As(metamodel.CLASS_NAME_TEST_RESULTS_SUMMARY)),
        None
    )
    if test_results_summary is not None and test_results_summary in selected_models:
        # If "General Information" is selected, the test results group will be added to the results.
        results.append(root)
        return results

    # If no model is selected, child models are recursively explored.
    children_group = [model for model in root.GetChildren() if model.As(target_class)]
    for group in children_group:
        child_results = _get_target_test_results_groups(group, selected_models, target_class)
        results.extend(child_results)

    return results

def _count_and_update_summary(test_result_group: "IModel", target_process: metamodel.TestProcessClassNames) -> TestResultsCounts:
    """Test result aggregation and general information update function
    For all General Information under the target Test Result Group, the test results will be aggregated and updated.

    Args:
        test_result_group: Target test result group
        target_process: Target process class name
    Returns:
        List of results
    """
    counter = TestResultsCounts()

    # The subgroups are aggregated and updated first, and then the results are added together.
    children_groups = [model for model in test_result_group.GetChildren() if model.As(target_process.test_results_group_class)]
    for group in children_groups:
        child_counts = _count_and_update_summary(group, target_process)
        counter.planned += child_counts.planned
        counter.actual += child_counts.actual
        counter.ok += child_counts.ok
        counter.ng += child_counts.ng
        counter.not_run += child_counts.not_run
        counter.excluded += child_counts.excluded

    # Aggregate the direct test results.
    children_test_cases = [model for model in test_result_group.GetChildren() if model.As(target_process.test_result_class)]
    for test_case in children_test_cases:
        status = test_case.GetFieldString(metamodel.FIELD_NAME_TEST_RESULTS_STATUS)

        if status != metamodel.FIELD_VALUE_STATUS_EXCLUDED:
            counter.planned += 1
        if status == metamodel.FIELD_VALUE_STATUS_OK or status == metamodel.FIELD_VALUE_STATUS_NG:
            counter.actual += 1
        if status == metamodel.FIELD_VALUE_STATUS_OK:
            counter.ok += 1
        if status == metamodel.FIELD_VALUE_STATUS_NG:
            counter.ng += 1
        if status == metamodel.FIELD_VALUE_STATUS_NOT_RUN:
            counter.not_run += 1
        if status == metamodel.FIELD_VALUE_STATUS_EXCLUDED:
            counter.excluded += 1

    # Update the General Information.
    summary = next(
        (model for model in test_result_group.GetChildren() if model.As(metamodel.CLASS_NAME_TEST_RESULTS_SUMMARY)),
        None
    )
    if summary is not None:
        # The field will be updated.
        summary.SetField(metamodel.FIELD_NAME_PLANNED_TEST_CASES, counter.planned)
        summary.SetField(metamodel.FIELD_NAME_ACTUAL_TEST_CASES, counter.actual)
        summary.SetField(metamodel.FIELD_NAME_OK_TEST_CASES, counter.ok)
        summary.SetField(metamodel.FIELD_NAME_NG_TEST_CASES, counter.ng)
        summary.SetField(metamodel.FIELD_NAME_NOT_RUN_TEST_CASES, counter.not_run)
        summary.SetField(metamodel.FIELD_NAME_EXCLUDED_TEST_CASES, counter.excluded)

        # Add an error (Type: Information).
        summary.AddError(metamodel.FIELD_NAME_NAME, "Information", ERROR_TITLE_UPDATE_TEST_RESULTS_SUMMARY, ERROR_MSG_UPDATED_TEST_CASE_COUNTS)

    return counter
