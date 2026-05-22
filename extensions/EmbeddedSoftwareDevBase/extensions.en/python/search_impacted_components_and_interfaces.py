"""Function: Extracts the affected areas of the Interface.

Starting with the selected Software Component or provided Interface, 
the system searches for affected Software Components and Interfaces 
and registers the search results.
If you are viewing the diagram in the editor, the connectors that form the path of the affected areas will also be registered in the search results.

Processing Overview
    - Verify that the model selected in the editor is the class you are investigating.
    - This retrieves connectors from the ER diagram currently displayed in the editor.
    - The system searches for affected areas within the model under investigation using a stack-based approach and registers them in the search results.
    - The search results will be notified to the user.
"""

# =======================================
# Importing external files and modules
# =======================================
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple  # TYPE_CHECKING and types for annotations.
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
# Name of the class being investigated
# This defines the class names of the models that can be selected as the starting point for the investigation.
# ---------------------------------------
SEARCH_TARGET_CLASSES = [
    metamodel.CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT,
    metamodel.CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN
]

# ---------------------------------------
# Definition of search results
# ---------------------------------------
SEARCH_NAME = "Interface impact areas"
SEARCH_MATCH_TYPE = "match"

# Field names to set in search results
SEARCH_FIELD_ORIGIN = "Name"
SEARCH_FIELD_INTERFACE = "Name"
SEARCH_FIELD_COMPONENT = "Name"
SEARCH_FIELD_CONNECTOR = None  # Specifying None will register the result in the search results without specifying any fields.

# Message to set in search results
SEARCH_MSG_ORIGIN = "This is the starting model."
SEARCH_MSG_INTERFACE = "This is an interface affected by {0}."      # The name of the starting model is assigned to {0}.
SEARCH_MSG_COMPONENT = "This is a software component affected by {0}."
SEARCH_MSG_CONNECTOR = "These are connectors for {0} and {1}."      # The name of the model to be searched is assigned to {0}, and the name of the model affected is assigned to {1}.

# ---------------------------------------
# Messages (user notifications)
# This is the text displayed when adding a dialog box or error message.
# ---------------------------------------
DIALOG_MSG_INVALID_SEARCH_TARGET_SELECTION = "Please select only one starting Interface or Software Component in the editor."
DIALOG_MSG_NO_IMPACT = "There were no connected elements."

# =======================================
# Main processing function
# The function defined here is linked to the Command in manifest.json.
# =======================================
def search_impacted_components_and_interfaces(context: "ICommandContext", parameters: "ICommandParams") -> None:
    """Searches for affected models from the selected Software Component or Interface
    and registers them in the search results.
    This is a command handler linked to the Command in manifest.json.
    """
    # 1. Obtain the model to be investigated.
    selected_models = utils.get_selected_models(context)

    # This retrieves the models from the selected models that correspond to the class being investigated.
    search_root_model = next(
        (model for model in selected_models if model.AsIn(classNames=SEARCH_TARGET_CLASSES)),
        None
    )

    # 2. Verify that the selected model is a single model and belongs to the class being investigated.
    if len(selected_models) != 1 or search_root_model is None:
        # If the conditions are not met, a dialog box will be displayed and the program will terminate.
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_INVALID_SEARCH_TARGET_SELECTION)
        return

    # 3. Retrieve connectors from the diagram currently open in the editor and index them so that they can be searched by start and end point model.
    diagram = None
    if context.App.Window.EditorPage and context.App.Window.EditorPage.CurrentEditorView:
        diagram = context.App.Window.EditorPage.CurrentEditorView.Editor
    connector_lookup = _create_connector_lookup(diagram)

    # 4. Clear existing search results and start the search.
    search_manager = context.App.Search
    search = search_manager.Create()
    search_manager.ClearResults()
    search.BeginSearch(SEARCH_NAME, SEARCH_MATCH_TYPE)

    # 5. Explore the affected areas from the starting point model.
    visited = set()
    _search_impact(search_root_model, visited, search, connector_lookup)

    # Ending the search.
    search.EndSearch()

    # 6. Notify the user of the results.
    all_results = list(search_manager.AllResults)
    if len(all_results) > 1:
        # If there are other models affected besides the starting model, activate the search window.
        context.App.Window.IsInformationPaneVisible = True
        context.App.Window.ActiveInfoWindow = "SearchResult"
    else:
        # If no models other than the starting model are affected, the search results will be cleared.
        search_manager.ClearResults()

        # A dialog box will notify you that there are no affected models.
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_IMPACT)

# =======================================
# Sub processing function
# =======================================
def _search_impact(
    search_root_model: "IModel",
    visited: Set[str],
    search: "ISearch",
    connector_lookup: Dict[Tuple[str, str], List["IConnector"]]
) -> None:
    """Influence detection function
    The starting model is registered in the search results, and the models set in the corresponding field are searched for as affected areas.
    During the search, the connectors that form the pathway to the affected areas are also registered in the search results.
    To traverse the model step by step, we use a stack instead of recursion as a measure against stack overflow.

    Args:
        search_root_model: Starting model
        visited: Set of visited models
        search: Search object
        connector_lookup: Connector index
    """
    # Prepare a stack to trace the affected areas, and add the starting model first.
    stack = [(search_root_model, None)]

    # Trace the affected areas until the stack is empty.
    is_first = True
    while stack:
        # Retrieve the next model to be investigated from the stack.
        impacted_model, search_model = stack.pop()

        # The connector between the parent model and the new model will be registered in the search results.
        _search_connectors_between(search_model, impacted_model, connector_lookup, search)

        # Ignore if you have already visited.
        if impacted_model.Id in visited:
            continue

        # The search result message and the next target for exploration are determined based on the class of the model being investigated.
        next_target_models = []
        if impacted_model.As(metamodel.CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT):
            # In the case of an Interface.
            message = SEARCH_MSG_INTERFACE.format(search_root_model.Name)
            field_name = SEARCH_FIELD_INTERFACE

            # Obtain the following model to be investigated.
            next_target_models.extend(list(impacted_model.GetFieldValues(metamodel.FIELD_NAME_USED_BY_COMPONENTS)))
            next_target_models.extend(list(impacted_model.GetFieldValues(metamodel.FIELD_NAME_DELEGATED_INTERFACES)))
        elif impacted_model.As(metamodel.CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN):
            # In the case of Software Component.
            message = SEARCH_MSG_COMPONENT.format(search_root_model.Name)
            field_name = SEARCH_FIELD_COMPONENT

            # Obtain the following model to be investigated.
            next_target_models.extend(list(impacted_model.GetFieldValues(metamodel.FIELD_NAME_INTERFACE_FUNCTIONS)))
            next_target_models.extend(list(impacted_model.GetFieldValues(metamodel.FIELD_NAME_INTERFACE_DATA)))
        else:
            # Classes that are not included will be ignored.
            continue

        if is_first:
            # If it's the starting model, change the message.
            message = SEARCH_MSG_ORIGIN
            field_name = SEARCH_FIELD_ORIGIN
            is_first = False

        # Register this in the search results.
        search.AddSearchResult(impacted_model, field_name, message)

        # Add this to my visited list.
        visited.add(impacted_model.Id)

        # Add the following models to the stack. Remove duplicates.
        seen = set()
        for next_target in next_target_models:
            if next_target.Id not in seen:
                seen.add(next_target.Id)
                stack.append((next_target, impacted_model))

def _search_connectors_between(
    search_model: Optional["IModel"],
    impacted_model: Optional["IModel"],
    connector_lookup: Dict[Tuple[str, str], List["IConnector"]],
    search: "ISearch"
) -> None:
    """Connector lookup function between models
    The system searches the index for connectors that link the two models, and if found, registers them in the search results.

    Args:
        search_model: Model 1
        impacted_model: Model 2
        connector_lookup: Connector Index
        search: Search Object
    """
    if search_model is None or impacted_model is None:
        return

    # Search for the connector that connects the two models using the connector index.
    key = (search_model.Id, impacted_model.Id)
    connectors = connector_lookup.get(key)
    if connectors:
        # The found connectors will be added to the search results.
        for connector in connectors:
            message = SEARCH_MSG_CONNECTOR.format(search_model.Name, impacted_model.Name)
            search.AddSearchResult(connector.Model, SEARCH_FIELD_CONNECTOR, message)

def _create_connector_lookup(diagram: Optional["IDiagram"]) -> Dict[Tuple[str, str], List["IConnector"]]:
    """Connector index creation function
    Retrieve connectors from the diagram and create an index using the combination of start and end point models as the key.
    The starting and ending points can be in either direction; registration is done bidirectionally.
    If the diagram is null, it returns an empty index.

    Args:
        diagram: Diagram
    Returns:
        Connector index
    """
    connector_lookup = {}

    if diagram is None:
        # If the diagram is null, it returns an empty index.
        return connector_lookup

    # If the diagram does not have a Connectors property, return an empty index.
    connectors = getattr(diagram, 'Connectors', None)
    if connectors is None:
        return connector_lookup

    # The system scans the connectors in the diagram and creates an index using the start-end model combination as the key.
    for connector in connectors:
        start_id = connector.StartPoint.Model.Id
        end_id = connector.EndPoint.Model.Id

        # Create a key for both directions.
        key1 = (start_id, end_id)
        key2 = (end_id, start_id)

        # Create a list using the combination of start and end points as the key.
        # Connectors with the same start and end points are added to the same key list.
        connector_lookup.setdefault(key1, []).append(connector)
        connector_lookup.setdefault(key2, []).append(connector)

    return connector_lookup
