// =======================================
// Function: Extracts the affected areas of the Interface.
// =======================================
//
// Starting with the selected Software Component or provided Interface, 
// the system searches for affected Software Components and Interfaces 
// and registers the search results.
// If you are viewing the diagram in the editor, the connectors that form the path of the affected areas will also be registered in the search results.
//
// Processing Overview
//   - Verify that the model selected in the editor is the class you are investigating.
//   - This retrieves connectors from the ER diagram currently displayed in the editor.
//   - The system searches for affected areas within the model under investigation using a stack-based approach and registers them in the search results.
//   - The search results will be notified to the user.
//
// Notes
//   The processing is implemented using LINQ (Any, Skip, FirstOrDefault, Distinct, ToList).
//   For more information on LINQ, please see below.
//   Overview of LINQ: https://learn.microsoft.com/en-us/dotnet/csharp/linq/
//   API Reference: https://learn.microsoft.com/en-us/dotnet/api/system.linq.enumerable


// =======================================
// Importing external files and namespaces
// =======================================
#load "utils.cs"     // General-purpose function
#load "metamodel.cs" // Metamodel information such as class names

// =======================================
// User-defined settings (parameters)
// You can edit this area to change the target of the operation or the message.
// =======================================

// ---------------------------------------
// Name of the class being investigated
// This defines the class names of the models that can be selected as the starting point for the investigation.
// ---------------------------------------
string[] SEARCH_TARGET_CLASSES = new string[]
{
    CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT,
    CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN
};

// ---------------------------------------
// Definition of search results
// ---------------------------------------
string SEARCH_NAME = "Interface impact areas";
string SEARCH_MATCH_TYPE = "match";

// Field names to set in search results
string SEARCH_FIELD_ORIGIN = "Name";
string SEARCH_FIELD_INTERFACE = "Name";
string SEARCH_FIELD_COMPONENT = "Name";
string SEARCH_FIELD_CONNECTOR = null; // Specifying null will register the result in the search results without specifying any fields.

// Message to set in search results
string SEARCH_MSG_ORIGIN = "This is the starting model.";
string SEARCH_MSG_INTERFACE = "This is an interface affected by {0}."; // The name of the starting model is assigned to {0}.
string SEARCH_MSG_COMPONENT = "This is a software component affected by {0}.";
string SEARCH_MSG_CONNECTOR = "These are connectors for {0} and {1}."; // The name of the model to be searched is assigned to {0}, and the name of the model affected is assigned to {1}.

// ---------------------------------------
// Messages (user notifications)
// This is the text displayed when adding a dialog box or error message.
// ---------------------------------------
string DIALOG_MSG_INVALID_SEARCH_TARGET_SELECTION = "Please select only one starting Interface or Software Component in the editor.";
string DIALOG_MSG_NO_IMPACT = "There were no connected elements.";

// =======================================
// Main processing function
// The function defined here is linked to the Command in manifest.json.
// =======================================
public void SearchImpactedComponentsAndInterfaces(ICommandContext context, ICommandParams parameters)
{
    // 1. Obtain the model to be investigated.
    var selectedModels = GetSelectedModels(context).ToList();

    // This retrieves the models from the selected models that correspond to the class being investigated.
    var searchRootModel = selectedModels.FirstOrDefault(model => model.AsIn(SEARCH_TARGET_CLASSES));

    // 2. Verify that the selected model is a single model and belongs to the class being investigated.
    if (selectedModels.Count != 1 || searchRootModel == null)
    {
        // If the conditions are not met, a dialog box will be displayed and the program will terminate.
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_INVALID_SEARCH_TARGET_SELECTION);
        return;
    }

    // 3. Retrieve connectors from the diagram currently open in the editor and index them so that they can be searched by start and end point model.
    var diagram = context.App.Window.EditorPage?.CurrentEditorView.Editor as IDiagram;
    var connectorLookup = CreateConnectorLookup(diagram);

    // 4. Clear existing search results and start the search.
    var searchManager = context.App.Search;
    var search = searchManager.Create();
    searchManager.ClearResults();
    search.BeginSearch(SEARCH_NAME, SEARCH_MATCH_TYPE);

    // 5. Explore the affected areas from the starting point model.
    var visited = new HashSet<IModel>();
    SearchImpact(searchRootModel, visited, search, connectorLookup);

    // Ending the search.
    search.EndSearch();

    // 6. Notify the user of the results.
    if (searchManager.AllResults.Skip(1).Any())
    {
        // If there are other models affected besides the starting model, activate the search window.
        context.App.Window.IsInformationPaneVisible = true;
        context.App.Window.ActiveInfoWindow = "SearchResult";
    }
    else
    {
        // If no models other than the starting model are affected, the search results will be cleared.
        searchManager.ClearResults();

        // A dialog box will notify you that there are no affected models.
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_IMPACT);
    }
}

// =======================================
// Sub processing function
// =======================================

// ---------------------------------------
// Influence detection function
// The starting model is registered in the search results, and the models set in the corresponding field are searched for as affected areas.
// During the search, the connectors that form the pathway to the affected areas are also registered in the search results.
// To traverse the model step by step, we use a stack instead of recursion as a measure against stack overflow.
// Arguments: Starting model, set of visited models, search object, connector index
// ---------------------------------------
private void SearchImpact(IModel searchRootModel, HashSet<IModel> visited, ISearch search, Dictionary<(string, string), List<IConnector>> connectorLookup)
{
    // Prepare a stack to trace the affected areas, and add the starting model first.
    var stack = new Stack<(IModel impactedModel, IModel searchModel)>();
    stack.Push((searchRootModel, null));

    // Trace the affected areas until the stack is empty.
    var isFirst = true;
    while (stack.Count > 0)
    {
        // Retrieve the next model to be investigated from the stack.
        var (impactedModel, searchModel) = stack.Pop();

        // The connector between the parent model and the new model will be registered in the search results.
        SearchConnectorsBetween(searchModel, impactedModel, connectorLookup, search);

        // Ignore if you have already visited.
        if (visited.Contains(impactedModel)) continue;

        // The search result message and the next target for exploration are determined based on the class of the model being investigated.
        string message;
        string fieldName;
        var nextTargetModels = new List<IModel>();
        if (impactedModel.As(CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT))
        {
            // In the case of an Interface.
            message = string.Format(SEARCH_MSG_INTERFACE, searchRootModel.Name);
            fieldName = SEARCH_FIELD_INTERFACE;

            // Obtain the following model to be investigated.
            nextTargetModels.AddRange(impactedModel.GetFieldValues(FIELD_NAME_USED_BY_COMPONENTS));
            nextTargetModels.AddRange(impactedModel.GetFieldValues(FIELD_NAME_DELEGATED_INTERFACES));
        }
        else if (impactedModel.As(CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN))
        {
            // In the case of Software Component.
            message = string.Format(SEARCH_MSG_COMPONENT, searchRootModel.Name);
            fieldName = SEARCH_FIELD_COMPONENT;

            // Obtain the following model to be investigated.
            nextTargetModels.AddRange(impactedModel.GetFieldValues(FIELD_NAME_INTERFACE_FUNCTIONS));
            nextTargetModels.AddRange(impactedModel.GetFieldValues(FIELD_NAME_INTERFACE_DATA));
        }
        else
        {
            // Classes that are not included will be ignored.
            continue;
        }

        if (isFirst)
        {
            // If it's the starting model, change the message.
            message = SEARCH_MSG_ORIGIN;
            fieldName = SEARCH_FIELD_ORIGIN;
            isFirst = false;
        }

        // Register this in the search results.
        search.AddSearchResult(impactedModel, fieldName, message);

        // Add this to my visited list.
        visited.Add(impactedModel);

        // Add the following models to the stack. Remove duplicates using Distinct.
        foreach (var nextTarget in nextTargetModels.Distinct())
        {
            stack.Push((nextTarget, impactedModel));
        }
    }
}

// ---------------------------------------
// Connector lookup function between models
// The system searches the index for connectors that link the two models, and if found, registers them in the search results.
// Arguments: Model 1, Model 2, Connector Index, Search Object
// ---------------------------------------
private void SearchConnectorsBetween(IModel searchModel, IModel impactedModel, Dictionary<(string, string), List<IConnector>> connectorLookup, ISearch search)
{
    if (searchModel == null || impactedModel == null) return;

    // Search for the connector that connects the two models using the connector index.
    var key = (searchModel.Id, impactedModel.Id);
    if (connectorLookup.TryGetValue(key, out var connectors))
    {
        // The found connectors will be added to the search results.
        foreach (var connector in connectors)
        {
            var message = string.Format(SEARCH_MSG_CONNECTOR, searchModel.Name, impactedModel.Name);
            search.AddSearchResult(connector.Model, SEARCH_FIELD_CONNECTOR, message);
        }
    }
}

// ---------------------------------------
// Connector index creation function
// Retrieve connectors from the diagram and create an index using the combination of start and end point models as the key.
// The starting and ending points can be in either direction; registration is done bidirectionally.
// If the diagram is null, it returns an empty index.
// Argument: Diagram
// Return value: Connector index
// ---------------------------------------
private Dictionary<(string, string), List<IConnector>> CreateConnectorLookup(IDiagram diagram)
{
    var connectorLookup = new Dictionary<(string, string), List<IConnector>>();

    if (diagram == null)
    {
        // If the diagram is null, it returns an empty index.
        return connectorLookup;
    }

    // The system scans the connectors in the diagram and creates an index using the start-end model combination as the key.
    foreach (var connector in diagram.Connectors)
    {
        var startId = connector.StartPoint.Model.Id;
        var endId = connector.EndPoint.Model.Id;

        // Create a key for both directions.
        var key1 = (startId, endId);
        var key2 = (endId, startId);

        // Create a list using the combination of start and end points as the key.
        // Connectors with the same start and end points are added to the same key list.
        if (!connectorLookup.ContainsKey(key1))
        {
            connectorLookup[key1] = new List<IConnector>();
        }
        if (!connectorLookup.ContainsKey(key2))
        {
            connectorLookup[key2] = new List<IConnector>();
        }

        // Add the connector to the list.
        connectorLookup[key1].Add(connector);
        connectorLookup[key2].Add(connector);
    }

    return connectorLookup;
}