"""Function: Derives Software Requirement models.

The Software Requirement Analysis or Software Requirement Group selected in the sub-editor 
will be used to create Software requirement Group/Software Requirement in bulk, 
with the same hierarchical structure as the System Requirement Group or System Requirement selected in the main editor, 
under the selected Software Requirement Analysis or Software Requirement Group.
This sets up the derivation relationship (higher-level System Requirement) from System Requirement to Software Requirement.
The Software Requirement you create will be automatically assigned an ID.

Processing Overview
    - This checks if the selected model is invalid.
    - Retrieves the System Requirement Group/System Requirement from which it was derived.
    - The system recursively scans the source of the derivation and creates Software Requirement Group/Software Requirement.
    - A sequential ID will be assigned to the created Software Requirement.
"""

# =======================================
# Importing external files and modules
# =======================================
from typing import TYPE_CHECKING, List  # TYPE_CHECKING and types for annotations.
import utils      # General-purpose function
import metamodel  # Metamodel information such as class names
from update_id import PROCESS_ID_CONFIGS, get_max_id, set_sequential_ids  # To assign an ID to the created model, we use an ID assignment function.

# Importing nd outside main.py causes runtime errors.
# Therefore, import only during type checking.
if TYPE_CHECKING:
    from nd import *

# =======================================
# User-defined settings (parameters)
# You can edit this area to change the target of the operation or the message.
# =======================================

# ---------------------------------------
# Messages (user notifications)
# This is the text displayed when adding a dialog box or error message.
# ---------------------------------------
# Message to display in the dialog box
DIALOG_MSG_DERIVE_SW_REQ_NO_SELECTED_SOURCE = "Please select the System Requirement Group or System Requirement from which you derived the request in the main editor."
DIALOG_MSG_DERIVE_SW_REQ_SUB_EDITOR_INVALID = "In the sub-editor, select one Software Requirement Analysis or Software Requirement Group to which the derived model will be added."
DIALOG_MSG_DERIVE_SW_REQ_HAS_ERROR = "Some models failed to create.\nPlease check the error window."

# Derivation process notification
ERROR_TITLE_DERIVE_SW_REQ = "Derives Software Requirement models"
ERROR_MSG_DERIVE_SW_REQ_CREATED = "A model has been created."
ERROR_MSG_DERIVE_SW_REQ_FAILED = "The Software Requirement model could not be created."
ERROR_MSG_DERIVE_SW_REQ_ID_OVERFLOW = "The value could not be set because the number of consecutive numbers exceeded the maximum value."

# =======================================
# Main processing function
# The function defined here is linked to the Command in manifest.json.
# =======================================
def derive_software_requirements(context: "ICommandContext", parameters: "ICommandParams") -> None:
    """Creates a similar structure in the selected Software Requirement Analysis or Software Requirement Group,
    based on the selected System Requirement Group/System Requirement in the main editor.
    This is a command handler linked to the Command in manifest.json.
    """
    # 1. Retrieve the model currently selected in the main editor and sub-editor.
    # Retrieves the currently selected model, System Requirement Group, and System Requirement in the main editor.
    selected_models_main = utils.get_selected_models_in_main_editor(context)
    selected_system_reqs = [
        model for model in selected_models_main
        if model.AsIn(classNames=[metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, metamodel.CLASS_NAME_SYSTEM_REQUIREMENT])
    ]

    # Gets the model currently selected in the sub-editor.
    selected_models_sub = utils.get_selected_models_in_sub_editor(context)

    # 2. Verify that the correct model is selected. If incorrect, display a dialog box and exit.
    # 2.1. One or more System Requirement Group or System Requirement must be selected in the main editor.
    if not selected_system_reqs:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_NO_SELECTED_SOURCE)
        return

    # 2.2. A sub-editor is displayed, one is selected, and it is either a Software requirement Analysis or a Software requirement Group.
    is_valid_sub_editor = (
        context.App.Window.EditorPage.IsSubEditorVisible
        and len(selected_models_sub) == 1
        and selected_models_sub[0].AsIn(classNames=[metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP])
    )

    if not is_valid_sub_editor:
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_SUB_EDITOR_INVALID)
        return

    # 3. Obtain the source and destination models.
    # We obtain the source model from which the model was derived. We then recursively explore using the System Requirement Analysis as the root.
    src_models = []
    src_process_root = selected_system_reqs[0].FindOwnerByClass(metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS)
    target_classes = [metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, metamodel.CLASS_NAME_SYSTEM_REQUIREMENT]
    utils.collect_selected_root_models(src_process_root, selected_system_reqs, target_classes, src_models)

    # Retrieve the derived model.
    dst_model = selected_models_sub[0]

    # 4. Obtain the maximum value of the IDs of existing Software Requirement.
    # The Software Requirement Analysis root to be derived will be used to obtain all Software Requirement below it.
    all_software_req_analyses = [
        model for model in context.App.Workspace.CurrentProject.DesignModel.GetChildren()
        if model.As(metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS)
    ]
    all_software_reqs = []
    for analysis in all_software_req_analyses:
        all_software_reqs.extend([
            model for model in analysis.GetAllChildren()
            if model.As(metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT)
        ])

    # Get the ID prefix for the software Requirement.
    # It is obtained from PROCESS_ID_CONFIGS defined in update_id.py.
    id_prefix = next(
        c.prefix for c in PROCESS_ID_CONFIGS
        if metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT in c.target_classes
    )

    # The maximum value of the ID is obtained from all retrieved Software Requirement.
    max_id = get_max_id(all_software_reqs, metamodel.FIELD_NAME_ID, id_prefix)

    # 5. Perform the derivation.
    # The contents of the error window will be cleared before execution.
    context.App.Errors.ClearErrors()

    # Prepare a list to collect the Software Requirement models you have created.
    created_software_requirements = []

    for src_model in src_models:
        # Trace the descendants of the source model and create a similar structure under the target model.
        if src_model.As(metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP):
            # The fields to be derived will vary depending on the class of the model being derived from.
            derivation_field_name = metamodel.FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS
            if dst_model.As(metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS):
                derivation_field_name = metamodel.FIELD_NAME_REQUIREMENTS_GROUP

            # Create a Software Requirement Group using the System Requirement Group as the source.
            new_model = dst_model.AddNewModel(derivation_field_name, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP)
            new_model.SetField(metamodel.FIELD_NAME_NAME, src_model.Name)

            # Information notifications are registered to the child model added directly under the selected model in the sub-editor.
            new_model.AddError(metamodel.FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_CREATED)

            # Recursively derive the descendants.
            _derive_child_software_requirements(src_model, new_model, created_software_requirements)
        elif src_model.As(metamodel.CLASS_NAME_SYSTEM_REQUIREMENT):
            if dst_model.As(metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS):
                # An error will be added because model creation is not possible when the source is a System Requirement and the target is a Software Requirement.
                src_model.AddError(metamodel.FIELD_NAME_NAME, "Error", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_FAILED)
                continue

            # Software Requirement are created using System Requirement as the source.
            new_model = dst_model.AddNewModel(metamodel.FIELD_NAME_SOFTWARE_REQUIREMENTS, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT)
            new_model.SetField(metamodel.FIELD_NAME_NAME, src_model.Name)
            new_model.SetField(metamodel.FIELD_NAME_INPUT_SYSTEM_REQUIREMENT, src_model)

            # Add the created Software Requirement to the list.
            created_software_requirements.append(new_model)

            # Information notifications are registered to the child model added directly under the selected model in the sub-editor.
            new_model.AddError(metamodel.FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_CREATED)

    # 6. Assign IDs to the created Software Requirement in bulk.
    updated_models, error_models = set_sequential_ids(
        created_software_requirements,
        max_id + 1,
        id_prefix
    )

    # Add notifications to the error model.
    for model in error_models:
        model.AddError(metamodel.FIELD_NAME_ID, "Error", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_ID_OVERFLOW)

    # 7. Display the error window.
    context.App.Window.IsInformationPaneVisible = True
    context.App.Window.ActiveInfoWindow = "Error"

    # 8. If an error occurs, a dialog box will be displayed.
    if list(context.App.Errors.Errors):
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_HAS_ERROR)

# =======================================
# Sub processing function
# =======================================
def _derive_child_software_requirements(src_group: "IModel", dst_group: "IModel", created_software_requirements: List["IModel"]) -> None:
    """Derivation function for descendant Software Requirement
    Create a structure under the target Software Requirement Group that is similar to the System Requirement Group from which the derivation originates.

    Args:
        src_group: Source System Requirement Group
        dst_group: Target Software Requirement Group
        created_software_requirements: List to store the created Software Requirement
    """
    # Scan the child models of the derived group.
    children = src_group.GetChildren()
    for model in children:
        if model.As(metamodel.CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP):
            # A Software Requirement Group is created based on the System Requirement Group.
            new_model = dst_group.AddNewModel(metamodel.FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP)
            new_model.SetField(metamodel.FIELD_NAME_NAME, model.Name)

            # Derive descendant models starting from the added model.
            _derive_child_software_requirements(model, new_model, created_software_requirements)
        elif model.As(metamodel.CLASS_NAME_SYSTEM_REQUIREMENT):
            # A Software Requirement is created based on System Requirement.
            new_model = dst_group.AddNewModel(metamodel.FIELD_NAME_SOFTWARE_REQUIREMENTS, metamodel.CLASS_NAME_SOFTWARE_REQUIREMENT)
            new_model.SetField(metamodel.FIELD_NAME_NAME, model.Name)
            new_model.SetField(metamodel.FIELD_NAME_INPUT_SYSTEM_REQUIREMENT, model)

            # Add the created Software Requirement to the list.
            created_software_requirements.append(new_model)
        else:
            # Ignore everything except the System Requirement Group and System Requirement.
            pass
