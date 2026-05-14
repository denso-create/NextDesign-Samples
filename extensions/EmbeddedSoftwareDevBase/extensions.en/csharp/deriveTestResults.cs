// =======================================
// Function: Derives Test Result models.
// =======================================
//
// This function creates Test Result Group/Test Result with the same hierarchical structure 
// as the Test Case Group selected in the main editor, all under the Test Result Group selected in the sub-editor.
// Sets up the derivation relationship from Test Case to Test Result.
// General Information model will be added to the created Test Result Group.
// 
// Processing Overview
//   - This checks if the selected model is invalid.
//   - Retrieves the Test Case Group from which the derivation originated.
//   - The source Test Case Group is recursively scanned and added to the Test Result Group.
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

// =======================================
// User-defined settings (parameters)
// You can edit this area to change the target of the operation or the message.
// =======================================

// ---------------------------------------
// Array of process information
// Define the information for each process.
// You can add new steps by adding elements to this array.
// ---------------------------------------
TestProcessClassNames[] DERIVE_TARGET_PROCESS_CLASS_NAMES = new TestProcessClassNames[]
{
    // Software Test Process
    new TestProcessClassNames
    {
        ProcessClass            = CLASS_NAME_SOFTWARE_TEST,
        TestCasesGroupClass     = CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST,
        TestCaseClass           = CLASS_NAME_TEST_CASE_SOFTWARE_TEST,
        TestResultsGroupClass   = CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_TEST,
        TestResultClass         = CLASS_NAME_TEST_RESULT_SOFTWARE_TEST,
    },
    // Software Component Test Process
    new TestProcessClassNames
    {
        ProcessClass            = CLASS_NAME_SOFTWARE_COMPONENT_TEST,
        TestCasesGroupClass     = CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST,
        TestCaseClass           = CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST,
        TestResultsGroupClass   = CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_COMPONENT_TEST,
        TestResultClass         = CLASS_NAME_TEST_RESULT_SOFTWARE_COMPONENT_TEST,
    },
    // Software Integration Test Process
    new TestProcessClassNames
    {
        ProcessClass            = CLASS_NAME_SOFTWARE_INTEGRATION_TEST,
        TestCasesGroupClass     = CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST,
        TestCaseClass           = CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST,
        TestResultsGroupClass   = CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_INTEGRATION_TEST,
        TestResultClass         = CLASS_NAME_TEST_RESULT_SOFTWARE_INTEGRATION_TEST,
    }
};

// ---------------------------------------
// Messages (user notifications)
// This is the text displayed when adding a dialog box or error message.
// ---------------------------------------
// Message to display in the dialog box
string DIALOG_MSG_NO_SELECTED_TEST_CASE_GROUP = "Please select the source Test Case group in the main editor.";
string DIALOG_MSG_HAS_MULTIPLE_CLASSES = "Please select the same type for all Test Case Group used for derivation.";
string DIALOG_MSG_SUB_EDITOR_INVALID = "In the sub-editor, select one Test Result Group to which the derived model will be added.";
string DIALOG_MSG_DIFFERENT_PROCESSES_SELECTED = "The process for the selected Test Case Group and the Test Result Group is different.";

// Derivation process notification
string ERROR_TITLE_DERIVE_TEST_RESULTS = "Derives Test Result models";
string ERROR_MSG_TEST_RESULTS_CREATED = "A model has been created.";

// =======================================
// Main processing function
// The function defined here is linked to the Command in manifest.json.
// =======================================
public void DeriveTestResults(ICommandContext context, ICommandParams parameters)
{
    // 1. Retrieve the model currently selected in the main editor and sub-editor.
    // Retrieves the model and Test Case Group currently selected in the main editor.
    var testCasesGroupClasses = DERIVE_TARGET_PROCESS_CLASS_NAMES.Select(p => p.TestCasesGroupClass);
    var selectedModelsMain = GetSelectedModelsInMainEditor(context).ToList();
    var selectedTestCasesGroups = selectedModelsMain.Where(model => model.AsIn(testCasesGroupClasses)).ToList();

    // Gets the currently selected model in the sub-editor.
    var selectedModelsSub = GetSelectedModelsInSubEditor(context).ToList();

    // 2. Verify that the correct model is selected. If incorrect, display a dialog box and exit.
    // 2.1. Ensure that at least one Test Case Group is selected in the main editor.
    if (!selectedTestCasesGroups.Any())
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_SELECTED_TEST_CASE_GROUP);
        return;
    }

    // 2.2. All Test Case Group selected in the main editor must be of the same type.
    var first = selectedTestCasesGroups.FirstOrDefault();
    if (!selectedTestCasesGroups.All(model => string.Equals(model.ClassName, first?.ClassName)))
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_HAS_MULTIPLE_CLASSES);
        return;
    }

    // 2.3. The sub-editor is displayed, and there is one model selected in the sub-editor.
    if (!context.App.Window.EditorPage.IsSubEditorVisible || selectedModelsSub.Count != 1)
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_SUB_EDITOR_INVALID);
        return;
    }

    // This retrieves the process to which the currently selected Test Case Group in the main editor belongs.
    var representative = selectedTestCasesGroups.FirstOrDefault();
    var targetProcess = DERIVE_TARGET_PROCESS_CLASS_NAMES.FirstOrDefault(process => process.TestCasesGroupClass == representative?.ClassName);
    var processRoot = representative?.FindOwnerByClass(targetProcess.ProcessClass);

    // 2.4. The class selected in the sub-editor must correspond to the class selected in the main editor.
    if (selectedModelsSub.First().ClassName != targetProcess.TestResultsGroupClass)
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_DIFFERENT_PROCESSES_SELECTED);
        return;
    }

    // 3. Obtain the source and destination of the derivation.
    // Retrieves the Test Case Group from which the derivation originated.
    var srcGroups = new List<IModel>();
    CollectSelectedRootModels(processRoot, selectedTestCasesGroups, new[] { targetProcess.TestCasesGroupClass }, srcGroups);

    // Retrieves the derived Test Result Group.
    var dstGroup = selectedModelsSub.First();

    // 4. Perform the derivation.
    // The contents of the error window will be cleared before execution.
    context.App.Errors.ClearErrors();

    // The source Test Case Group is recursively traversed, and a similar structure is created under the Test Result Group.
    foreach (var srcGroup in srcGroups)
    {
        var newModel = dstGroup.AddNewModel(FIELD_NAME_TEST_RESULTS_SUB_GROUPS, targetProcess.TestResultsGroupClass);
        newModel.SetField(FIELD_NAME_NAME, srcGroup.Name);

        // Information notifications are registered in the child model added directly under the derived model.
        newModel.AddError(FIELD_NAME_NAME, "Information", ERROR_TITLE_DERIVE_TEST_RESULTS, ERROR_MSG_TEST_RESULTS_CREATED);

        DeriveChildTestResults(srcGroup, newModel, targetProcess);
    }
}

// =======================================
// Sub processing function
// =======================================

// ---------------------------------------
// Function for deriving Test result for descendants.
// Create a structure similar to the source Test Case Group under the destination Test Result Group.
// However, we will add a General Information model to the Test Result Group.
// Arguments: Source Test Case Group, destination Test Result Group, class name of the target process
// ---------------------------------------
private void DeriveChildTestResults(IModel testCasesGroup, IModel testResultsGroup, TestProcessClassNames targetProcess)
{
    // Add the General Information model to the Test Result Group.
    testResultsGroup.AddNewModel(FIELD_NAME_TEST_RESULTS_SUMMARY, CLASS_NAME_TEST_RESULTS_SUMMARY);

    // Scan the child models of the derived Test Case Group.
    var children = testCasesGroup.GetChildren();
    foreach (var model in children)
    {
        if (model.As(targetProcess.TestCasesGroupClass))
        {
            // Add a Test Result Group to the Test Result Group.
            var newModel = testResultsGroup.AddNewModel(FIELD_NAME_TEST_RESULTS_SUB_GROUPS, targetProcess.TestResultsGroupClass);
            newModel.SetField(FIELD_NAME_NAME, model.Name);

            // Derive descendant models starting from the added model.
            DeriveChildTestResults(model, newModel, targetProcess);
        }
        else if (model.As(targetProcess.TestCaseClass))
        {
            // Add the Test Result to the Test Result Group.
            var newModel = testResultsGroup.AddNewModel(FIELD_NAME_TEST_RESULTS, targetProcess.TestResultClass);
            newModel.SetField(FIELD_NAME_NAME, model.Name);
            newModel.SetField(FIELD_NAME_TEST_CASES, model);
        }
        else
        {
            // Ignore everything except Test Case Group and Test Case.
        }
    }
}