// =======================================
// Function: Derives Software Requirement models.
// =======================================
//
// The Software Requirement Analysis or Software Requirement Group selected in the sub-editor 
// will be used to create Software requirement Group/Software Requirement in bulk, 
// with the same hierarchical structure as the System Requirement Group or System Requirement selected in the main editor, 
// under the selected Software Requirement Analysis or Software Requirement Group.
// This sets up the derivation relationship (higher-level System Requirement) from System Requirement to Software Requirement.
// The Software Requirement you create will be automatically assigned an ID.
//
// Processing Overview
//   - This checks if the selected model is invalid.
//   - Retrieves the System Requirement Group/System Requirement from which it was derived.
//   - The system recursively scans the source of the derivation and creates Software Requirement Group/Software Requirement.
//   - A sequential ID will be assigned to the created Software Requirement.
//
// Notes
//   The processing is implemented using LINQ (Any, Where, Select, First, FirstOrDefault, ToList).
//   For more information on LINQ, please see below.
//   Overview of LINQ: https://learn.microsoft.com/en-us/dotnet/csharp/linq/
//   API Reference: https://learn.microsoft.com/en-us/dotnet/api/system.linq.enumerable


// =======================================
// Importing external files and namespaces
// =======================================
#load "utils.cs"     // General-purpose function
#load "metamodel.cs" // Metamodel information such as class names
#load "updateId.cs"  // To assign an ID to the created model, we use an ID assignment function.

// =======================================
// User-defined settings (parameters)
// You can edit this area to change the target of the operation or the message.
// =======================================

// ---------------------------------------
// Messages (user notifications)
// This is the text displayed when adding a dialog box or error message.
// ---------------------------------------
// Message to display in the dialog box
string DIALOG_MSG_DERIVE_SW_REQ_NO_SELECTED_SOURCE = "Please select the System Requirement Group or System Requirement from which you derived the request in the main editor.";
string DIALOG_MSG_DERIVE_SW_REQ_SUB_EDITOR_INVALID = "In the sub-editor, select one Software Requirement Analysis or Software Requirement Group to which the derived model will be added.";
string DIALOG_MSG_DERIVE_SW_REQ_HAS_ERROR = "Some models failed to create.\nPlease check the error window.";

// Derivation process notification
string ERROR_TITLE_DERIVE_SW_REQ = "Derives Software Requirement models";
string ERROR_MSG_DERIVE_SW_REQ_CREATED = "A model has been created.";
string ERROR_MSG_DERIVE_SW_REQ_FAILED = "The Software Requirement model could not be created.";
string ERROR_MSG_DERIVE_SW_REQ_ID_OVERFLOW = "The value could not be set because the number of consecutive numbers exceeded the maximum value.";

// =======================================
// Main processing function
// The function defined here is linked to the Command in manifest.json.
// =======================================
public void DeriveSoftwareRequirements(ICommandContext context, ICommandParams parameters)
{
    // 1. Retrieve the model currently selected in the main editor and sub-editor.
    // Retrieves the currently selected model, System Requirement Group, and System Requirement in the main editor.
    var selectedModelsMain = GetSelectedModelsInMainEditor(context).ToList();
    var selectedSystemReqs = selectedModelsMain
        .Where(model => model.AsIn(new[] { CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, CLASS_NAME_SYSTEM_REQUIREMENT }))
        .ToList();

    // Gets the model currently selected in the sub-editor.
    var selectedModelsSub = GetSelectedModelsInSubEditor(context).ToList();

    // 2. Verify that the correct model is selected. If incorrect, display a dialog box and exit.
    // 2.1. One or more System Requirement Group or System Requirement must be selected in the main editor.
    if (!selectedSystemReqs.Any())
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_NO_SELECTED_SOURCE);
        return;
    }

    // 2.2. A sub-editor is displayed, one is selected, and it is either a Software requirement Analysis or a Software requirement Group.
    var isValidSubEditor =
        context.App.Window.EditorPage.IsSubEditorVisible &&
        selectedModelsSub.Count == 1 &&
        selectedModelsSub.First().AsIn(new[] { CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS, CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP });

    if (!isValidSubEditor)
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_SUB_EDITOR_INVALID);
        return;
    }

    // 3. Obtain the source and destination models.
    // We obtain the source model from which the model was derived. We then recursively explore using the System Requirement Analysis as the root.
    var srcModels = new List<IModel>();
    var srcProcessRoot = selectedSystemReqs.First().FindOwnerByClass(CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS);
    var targetClasses = new[] { CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP, CLASS_NAME_SYSTEM_REQUIREMENT };
    CollectSelectedRootModels(srcProcessRoot, selectedSystemReqs, targetClasses, srcModels);

    // Retrieve the derived model.
    var dstModel = selectedModelsSub.First();

    // 4. Obtain the maximum value of the IDs of existing Software Requirement.
    // The Software Requirement Analysis root to be derived will be used to obtain all Software Requirement below it.
    var allSoftwareReqAnalyses = context.App.Workspace.CurrentProject.GetRootChildren()
        .Where(model => model.As(CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS));
    var allSoftwareReqs = allSoftwareReqAnalyses
        .SelectMany(analysis => analysis.GetAllChildren().Where(model => model.As(CLASS_NAME_SOFTWARE_REQUIREMENT)));

    // Get the ID prefix for the software Requirement.
    // It is obtained from PROCESS_ID_CONFIGS defined in updateId.cs.
    var idPrefix = PROCESS_ID_CONFIGS
        .First(c => c.TargetClasses.Contains(CLASS_NAME_SOFTWARE_REQUIREMENT))
        .Prefix;

    // The maximum value of the ID is obtained from all retrieved Software Requirement.
    var maxId = GetMaxId(allSoftwareReqs, FIELD_NAME_ID, idPrefix);

    // 5. Perform the derivation.
    // The contents of the error window will be cleared before execution.
    context.App.Errors.ClearErrors();

    // Prepare a list to collect the Software Requirement models you have created.
    var createdSoftwareRequirements = new List<IModel>();

    foreach (var srcModel in srcModels)
    {
        // Trace the descendants of the source model and create a similar structure under the target model.
        if (srcModel.As(CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP))
        {
            // The fields to be derived will vary depending on the class of the model being derived from.
            var derivationFieldName = FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS;
            if (dstModel.As(CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS))
            {
                derivationFieldName = FIELD_NAME_REQUIREMENTS_GROUP;
            }

            // Create a Software Requirement Group using the System Requirement Group as the source.
            var newModel = dstModel.AddNewModel(derivationFieldName, CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP);
            newModel.SetField(FIELD_NAME_NAME, srcModel.Name);

            // Information notifications are registered to the child model added directly under the selected model in the sub-editor.
            newModel.AddError(FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_CREATED);

            // Recursively derive the descendants.
            DeriveChildSoftwareRequirements(srcModel, newModel, createdSoftwareRequirements);
        }
        else if (srcModel.As(CLASS_NAME_SYSTEM_REQUIREMENT))
        {
            if (dstModel.As(CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS))
            {
                // An error will be added because model creation is not possible when the source is a System Requirement and the target is a Software Requirement.
                srcModel.AddError(FIELD_NAME_NAME, "Error", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_FAILED);
                continue;
            }

            // Software Requirement are created using System Requirement as the source.
            var newModel = dstModel.AddNewModel(FIELD_NAME_SOFTWARE_REQUIREMENTS, CLASS_NAME_SOFTWARE_REQUIREMENT);
            newModel.SetField(FIELD_NAME_NAME, srcModel.Name);
            newModel.SetField(FIELD_NAME_INPUT_SYSTEM_REQUIREMENT, srcModel);

            // Add the created Software Requirement to the list.
            createdSoftwareRequirements.Add(newModel);

            // Information notifications are registered to the child model added directly under the selected model in the sub-editor.
            newModel.AddError(FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_CREATED);
        }
    }

    // 6. Assign IDs to the created Software Requirement in bulk.
    var (updatedModels, errorModels) = SetSequentialIds(
        createdSoftwareRequirements,
        maxId + 1,
        idPrefix
    );

    // Add notifications to the error model.
    foreach (var model in errorModels)
    {
        model.AddError(FIELD_NAME_ID, "Error", ERROR_TITLE_DERIVE_SW_REQ, ERROR_MSG_DERIVE_SW_REQ_ID_OVERFLOW);
    }

    // 7. Display the error window.
    context.App.Window.IsInformationPaneVisible = true;
    context.App.Window.ActiveInfoWindow = "Error";

    // 8. If an error occurs, a dialog box will be displayed.
    if (context.App.Errors.Errors.Any())
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DERIVE_SW_REQ_HAS_ERROR);
    }
}

// =======================================
// Sub processing function
// =======================================

// ---------------------------------------
// Derivation function for descendant Software Requirement
// Create a structure under the target Software Requirement Group that is similar to the System Requirement Group from which the derivation originates.
// Arguments: Source System Requirement Group, target Software Requirement Group, list to store the created Software Requirement
// ---------------------------------------
private void DeriveChildSoftwareRequirements(IModel srcGroup, IModel dstGroup, List<IModel> createdSoftwareRequirements)
{
    // Scan the child models of the derived group.
    var children = srcGroup.GetChildren();
    foreach (var model in children)
    {
        if (model.As(CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP))
        {
            // A Software Requirement Group is created based on the System Requirement Group.
            var newModel = dstGroup.AddNewModel(FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS, CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP);
            newModel.SetField(FIELD_NAME_NAME, model.Name);

            // Derive descendant models starting from the added model.
            DeriveChildSoftwareRequirements(model, newModel, createdSoftwareRequirements);
        }
        else if (model.As(CLASS_NAME_SYSTEM_REQUIREMENT))
        {
            // A Software Requirement is created based on System Requirement.
            var newModel = dstGroup.AddNewModel(FIELD_NAME_SOFTWARE_REQUIREMENTS, CLASS_NAME_SOFTWARE_REQUIREMENT);
            newModel.SetField(FIELD_NAME_NAME, model.Name);
            newModel.SetField(FIELD_NAME_INPUT_SYSTEM_REQUIREMENT, model);

            // Add the created Software Requirement to the list.
            createdSoftwareRequirements.Add(newModel);
        }
        else
        {
            // Ignore everything except the System Requirement Group and System Requirement.
        }
    }
}

