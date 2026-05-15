// =======================================
// Function: Update ID
// =======================================
//
// This command reassigns the IDs of the selected model and its descendants to be unique in bulk.
// IDs are assigned uniquely to each process.
//
// Processing Overview
//   - Retrieve the models to be updated.
//   - Find the maximum value of existing IDs from models that are not being updated.
//   - Start with the maximum value of the calculated ID + 1 and assign IDs sequentially.
//   - The results will be notified via a dialog box and an added error message.
//
// Notes
//   The processing is implemented using LINQ (Any, Where, Select, SelectMany, Except, Max, ToArray, ToList, ToHashSet).
//   For more information on LINQ, please see below.
//   Overview of LINQ: https://learn.microsoft.com/en-us/dotnet/csharp/linq/
//   API Reference: https://learn.microsoft.com/en-us/dotnet/api/system.linq.enumerable


// =======================================
// Importing external files and namespaces
// =======================================
#load "utils.cs"     // General-purpose function
#load "metamodel.cs" // Metamodel information such as class names
using System.Text.RegularExpressions; // Namespace for using regular expressions

// =======================================
// User-defined settings (parameters)
// You can edit this area to change the target of the operation or the message.
// =======================================

// ---------------------------------------
// Array of process information
// Define the information for each process.
// You can add new steps by adding elements to this array.
// ---------------------------------------
ProcessIdConfig[] PROCESS_ID_CONFIGS = new ProcessIdConfig[]
{
    // System Requirement Analysis Process
    new ProcessIdConfig
    {
        RootClasses     = new[] {CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS},
        StartClasses    = new[] {CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS, CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, CLASS_NAME_SYSTEM_REQUIREMENT},
        TargetClasses   = new[] {CLASS_NAME_SYSTEM_REQUIREMENT},
        Prefix = "SYRQ-"
    },

    // Software Requirement Analysis Process
    new ProcessIdConfig
    {
        RootClasses     = new[] {CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS},
        StartClasses    = new[] {CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS, CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP, CLASS_NAME_SOFTWARE_REQUIREMENT},
        TargetClasses   = new[] {CLASS_NAME_SOFTWARE_REQUIREMENT},
        Prefix = "SWRQ-"
    },

    // Software Component Test Process
    new ProcessIdConfig
    {
        RootClasses     = new[] {CLASS_NAME_SOFTWARE_COMPONENT_TEST},
        StartClasses    = new[] {CLASS_NAME_SOFTWARE_COMPONENT_TEST, CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST, CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST},
        TargetClasses   = new[] {CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST},
        Prefix = "SWCT-"
    },

    // Software Integration Test Process
    new ProcessIdConfig
    {
        RootClasses     = new[] {CLASS_NAME_SOFTWARE_INTEGRATION_TEST},
        StartClasses    = new[] {CLASS_NAME_SOFTWARE_INTEGRATION_TEST, CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST, CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST},
        TargetClasses   = new[] {CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST},
        Prefix = "SWIT-"
    },

    // Software Test Process
    new ProcessIdConfig
    {
        RootClasses     = new[] {CLASS_NAME_SOFTWARE_TEST},
        StartClasses    = new[] {CLASS_NAME_SOFTWARE_TEST, CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST, CLASS_NAME_TEST_CASE_SOFTWARE_TEST},
        TargetClasses   = new[] {CLASS_NAME_TEST_CASE_SOFTWARE_TEST},
        Prefix = "SWTT-"
    }
};

// ---------------------------------------
// Definition related to ID
// ---------------------------------------
int UPDATE_ID_DIGITS = 6; // Number of digits in the ID

// ---------------------------------------
// Messages (user notifications)
// This is the text displayed when adding a dialog box or error message.
// ---------------------------------------
string DIALOG_MSG_NO_UPDATE_TARGET_SELECTED = "Please select the model with an ID, or the ancestor model of the model with an ID, in the editor.";
string DIALOG_MSG_HAS_FAILED_ID = "There is a model whose ID update failed.\nPlease check the error window.";
string DIALOG_NO_ID_UPDATED = "There were no models that were eligible for update.";
string ERROR_TITLE_UPDATE_ID = "ID update";
string ERROR_MSG_SUCCESS_UPDATE_ID = "{0} has been set."; //By setting it to {0}, it can be replaced with a variable later.
string ERROR_MSG_FAILED_UPDATE_ID = "The sequence number exceeded the maximum value, so the values were cleared.";

// =======================================
// Main processing function
// The function defined here is linked to the Command in manifest.json.
// =======================================
public void UpdateId(ICommandContext context, ICommandParams parameters)
{
    // 1. Obtain the selection model and create an array of selection models for each process.
    // Gets the model currently selected in the editor.
    var selectedModels = GetSelectedModels(context);

    // For each step, we extract only the "selected models that correspond to the starting class (StartClasses)" and group them into an array.
    // Example: If only one Software Requirement model is selected,
    //    selectedModelsByProcess = {[], [Software Requirement model], []}
    var selectedModelsByProcess = PROCESS_ID_CONFIGS
        .Select(process =>
            // This process extracts only the selected models that correspond to StartClasses.
            selectedModels.Where(model => model.AsIn(process.StartClasses)))
        .ToArray();

    // 2. Check if at least one model corresponding to the starting class has been selected.
    if (!selectedModelsByProcess.Any(arr => arr.Any()))
    {
        // If not selected, a dialog box will appear and the operation will end.
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_UPDATE_TARGET_SELECTED);
        return;
    }

    // 3. Update the ID for each process.
    // Clear all existing errors.
    context.App.Errors.ClearErrors();

    // Retrieves the model directly under the project.
    var rootChildren = context.App.Workspace.CurrentProject.GetRootChildren();

    // 4. Execute the ID update process for each step.
    for (int i = 0; i < PROCESS_ID_CONFIGS.Length; i++)
    {
        // Retrieve the model directly under the project for each process.
        var processRootModels = rootChildren.Where(model => model.AsIn(PROCESS_ID_CONFIGS[i].RootClasses)).ToList();

        // The ID update process will be executed.
        UpdateIdsForProcess(
            PROCESS_ID_CONFIGS[i],
            selectedModelsByProcess[i],
            processRootModels
        );
    }

    // 5. We will notify you of the processing results.
    ShowResultNotification(context.App.Errors, context.App.Window);
}

// =======================================
// Sub processing function
// =======================================

// ---------------------------------------
// ID update function for one step
// The IDs of the selected model and its descendant models within the process will be updated.
// The maximum value of existing IDs is obtained from models that are not targeted, 
// and IDs are assigned starting from the maximum value + 1, 
// so that they are in order from top to bottom in the Model Navigator.
// If the ID exceeds the maximum value that can be set, an error will occur and an empty string will be set.
// Arguments: Process information, selection model, model of the target process root
// ---------------------------------------
private void UpdateIdsForProcess(
    ProcessIdConfig processInfo,
    IEnumerable<IModel> selectedModels,
    IEnumerable<IModel> rootModels
    )
{
    // 1. Retrieve all models that correspond to the class to be updated within the process.
    var allTargetClassModels = rootModels
        .SelectMany(model => model.GetAllChildren()) // Retrieves descendant models from all models.
        .Where(model => model.AsIn(processInfo.TargetClasses)) // Only the target class will be extracted.
        .ToList();

    // 2. Retrieve the model to be updated.
    var (targetModels, otherModels) = SplitModelsIntoTargetAndOthers(allTargetClassModels, selectedModels, processInfo.TargetClasses);

    // 3. Obtain the maximum ID value from the models that are not to be updated.
    var maxId = GetMaxId(otherModels, FIELD_NAME_ID, processInfo.Prefix);

    // 4. Update the IDs.
    var (updatedModels, errorModels) = SetSequentialIds(
        targetModels,
        maxId + 1,
        processInfo.Prefix
    );

    // 5. Grant notifications.
    foreach (var model in updatedModels)
    {
        // Successful models will have errors (type = information) added to them.
        var newId = model.GetFieldString(FIELD_NAME_ID);
        model.AddError(FIELD_NAME_ID, "Information", ERROR_TITLE_UPDATE_ID, string.Format(ERROR_MSG_SUCCESS_UPDATE_ID, newId));
    }
    foreach (var model in errorModels)
    {
        // For models that have errors, an error (type=error) will be added.
        model.AddError(FIELD_NAME_ID, "Error", ERROR_TITLE_UPDATE_ID, ERROR_MSG_FAILED_UPDATE_ID);
    }
}

// ---------------------------------------
// Function to determine which models should be updated and which should not.
// Divide them into the following two categories.
// - Models to be updated: The selected model and its descendant models that fall under the target class of the specified process.
// - Models not included in the update: All models that fall under the target class of the specified process, excluding those listed above.
// Arguments: All models, selected models, array of target class names
// Return values: Models to be updated, models not to be updated
// ---------------------------------------
private (IEnumerable<IModel>, IEnumerable<IModel>) SplitModelsIntoTargetAndOthers(
    IEnumerable<IModel> models,
    IEnumerable<IModel> selectedModels,
    string[] targetClassNames
    )
{
    // This retrieves the models from the selected model and its descendants that belong to the target class.
    var selectedWithChildren = selectedModels
        .SelectMany(model => model.GetAllChildren().Prepend(model)) // Retrieves the collection of the selected model and its descendant models.
        .Where(model => model.AsIn(targetClassNames)).ToHashSet(); // This extracts only the relevant classes and removes duplicates.

    // Separate the models into those that will be updated and those that will not.
    var targetModels = new List<IModel>();
    var otherModels = new List<IModel>();
    foreach (var model in models)
    {
        if (selectedWithChildren.Contains(model))
        {
            targetModels.Add(model);
        }
        else
        {
            otherModels.Add(model);
        }
    }

    return (targetModels, otherModels);
}

// ---------------------------------------
// ID Maximum Value Calculation Function
// Retrieve the maximum ID value from the received models.
// Arguments: Model, ID field name, ID prefix
// Return value: Maximum ID
// ---------------------------------------
private int GetMaxId(IEnumerable<IModel> models, string fieldName, string prefix)
{
    if (!models.Any())
    {
        // If the received model is empty, it returns 0.
        return 0;
    }

    // This retrieves the maximum value of IDs that match the naming convention.
    // This generates a regular expression from the prefix and number of digits.
    var regexPattern = $"^{Regex.Escape(prefix)}(?<num>[0-9]{{{UPDATE_ID_DIGITS}}})$";
    var regex = new Regex(regexPattern);

    var maxId = models.Max(model =>
    {
        var id = model.GetFieldString(fieldName);

        // Use regular expressions to check if the naming convention matches.
        var match = regex.Match(id);
        if (!match.Success)
        {
            // If the naming convention is not followed, it will be ignored.
            return 0;
        }

        // This function extracts the numerical portion from the ID string and converts it to an integer.
        // For example, in the case of "SYRQ-000123", "000123" is extracted and converted to 123.
        return int.Parse(match.Groups["num"].Value);
    });

    return maxId;
}

// ---------------------------------------
// Sequential ID setting function
// The specified value will be used as the initial value, and sequential IDs will be assigned to all models.
// If the ID exceeds the maximum value, an empty string will be set to the model's ID.
// Arguments: Model to update, starting ID value, ID prefix
// Return values: Successful models, models that failed due to exceeding the maximum value
// ---------------------------------------
private (List<IModel> updatedModels, List<IModel> errorModels) SetSequentialIds(
    IEnumerable<IModel> targetModels,
    int startIdNumber,
    string prefix
    )
{
    var updatedModels = new List<IModel>();
    var errorModels = new List<IModel>();
    int nextIdNumber = startIdNumber;

    int maxIdNumber = (int)Math.Pow(10, UPDATE_ID_DIGITS);

    // Assign an ID to each model.
    foreach (IModel model in targetModels)
    {
        if (nextIdNumber >= maxIdNumber)
        {
            // If the ID exceeds the maximum value, an empty string will be set.
            model.SetField(FIELD_NAME_ID, string.Empty);
            errorModels.Add(model);
            continue;
        }

        // A new ID will be generated.
        var newId = prefix + nextIdNumber.ToString($"D{UPDATE_ID_DIGITS}");
        var currentId = model.GetFieldString(FIELD_NAME_ID);

        if (currentId != newId)
        {
            // If the current ID is different from the original, set a new ID.
            model.SetField(FIELD_NAME_ID, newId);
            updatedModels.Add(model);
        }

        nextIdNumber++;
    }

    return (updatedModels, errorModels);
}

// ---------------------------------------
// Result notification function
// Send you a notification based on the processing result.
// An error window will be displayed, and a dialog box notification will be sent depending on the processing result.
// Arguments: Error information, window object for UI operation
// ---------------------------------------
private void ShowResultNotification(IErrors errors, IWorkspaceWindow window)
{
    // This retrieves whether or not there are any errors.
    var hasError = errors.Errors.Any();
    var hasChanged = errors.Informations.Any();

    // An error window will be displayed.
    if (hasError || hasChanged)
    {
        window.IsInformationPaneVisible = true;
        window.ActiveInfoWindow = "Error";
    }

    // Send user notifications based on the processing results.
    if (hasError)
    {
        window.UI.ShowInformationDialog(DIALOG_MSG_HAS_FAILED_ID);
    }
    else if (!hasChanged)
    {
        window.UI.ShowInformationDialog(DIALOG_NO_ID_UPDATED);
    }
}

// =======================================
// Data structure definition
// =======================================

// A structure that centrally manages the information necessary to update the ID for each process.
private struct ProcessIdConfig
{
    public string[] RootClasses;    // An array of class names that serve as the root of the process (used to retrieve all models for each process).
    public string[] StartClasses;   // An array of starting class names (used to determine the selection model for each process)
    public string[] TargetClasses;  // An array of class names to be updated (used to determine which IDs should be updated)
    public string Prefix;           // ID prefix (e.g., "SYRQ-")
}