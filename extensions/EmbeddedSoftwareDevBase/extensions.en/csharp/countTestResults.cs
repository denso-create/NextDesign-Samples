// =======================================
// Function: Aggregates Test Results
// =======================================
// 
// The test results are aggregated and the fields are updated for the General Information of the selected model and all models under it.
// When the General Information is updated, an error (Type: Information) is added to the corresponding General Information model.
// 
// Processing Overview
//   - Check if the target model is selected.
//   - Retrieves the target test result group.
//   - The data for the target test result group is aggregated from the lowest level downwards, and the General Information is updated.
//
// Notes
//   The processing is implemented using LINQ (Add, AddRange, Append, Contains, FirstOrDefault, Select, ToList, Where).
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
TestProcessClassNames[] COUNT_TARGET_PROCESS_CLASS_NAMES = new TestProcessClassNames[]
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
string DIALOG_MSG_NO_GROUP_OR_SUMMARY_SELECTED = "Please select the Test Result Group or General Information in the editor.";
string DIALOG_MSG_NO_UPDATED_SUMMARY = "There were no models that were eligible for update.";
string ERROR_TITLE_UPDATE_TEST_RESULTS_SUMMARY = "Aggregates Test Results";
string ERROR_MSG_UPDATED_TEST_CASE_COUNTS = "The number of test cases has been updated.";

// =======================================
// Main processing function
// The function defined here is linked to the Command in manifest.json.
// =======================================
public void CountTestResults(ICommandContext context, ICommandParams parameters)
{
    // 1. Retrieve the model that corresponds to the target class from the models currently selected in the editor.
    var targetClasses = COUNT_TARGET_PROCESS_CLASS_NAMES
        .Select(p => p.TestResultsGroupClass)
        .Append(CLASS_NAME_TEST_RESULTS_SUMMARY);
    var selectedModels = GetSelectedModels(context).Where(model => model.AsIn(targetClasses)).ToList();

    // 2. Verify that the model corresponding to the target class is selected.
    if (!selectedModels.Any())
    {
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_GROUP_OR_SUMMARY_SELECTED);
        return;
    }

    // 3. Retrieve the process to which the selected model belongs.
    var representative = selectedModels.First();
    var targetProcess = COUNT_TARGET_PROCESS_CLASS_NAMES.First(process => representative.FindOwnerByClass(process.ProcessClass) != null);
    var processRoot = representative.FindOwnerByClass(targetProcess.ProcessClass);

    // 4. Retrieve the target Test Result Group.
    var targetGroups = GetTargetTestResultsGroups(processRoot, selectedModels, targetProcess.TestResultsGroupClass);

    // 5. Update the General Information of child models.
    context.App.Errors.ClearErrors();
    foreach (var targetGroup in targetGroups)
    {
        CountAndUpdateSummary(targetGroup, targetProcess);
    }

    // 6. Output the results.
    var errors = context.App.Workspace.CurrentProject.GetAllErrorsWithChildren();
    if (errors.Any())
    {
        // If any changes occur, an error window will be displayed.
        context.App.Window.IsInformationPaneVisible = true;
        context.App.Window.ActiveInfoWindow = "Error";
    }
    else
    {
        // If there are no changes, a dialog box will notify you.
        context.App.Window.UI.ShowInformationDialog(DIALOG_MSG_NO_UPDATED_SUMMARY);
    }
}

// ---------------------------------------
// Function to retrieve target Test Result Group
// This retrieves the selected group/general information that does not have an ancestor in the selected group.
// Search recursively from the root model.
// Arguments: Search root model, selection model group, class name of the target group
// Return value: List of results
// ---------------------------------------
private List<IModel> GetTargetTestResultsGroups(IModel root, IEnumerable<IModel> selectedModels, string targetClass)
{
    var results = new List<IModel>();

    var selectedModelsList = selectedModels.ToList();
    if (selectedModelsList.Contains(root))
    {
        // If selected, it will be added to the results.
        results.Add(root);
        return results;
    }

    var testResultsSummary = root.GetChildren().FirstOrDefault(model => model.As(CLASS_NAME_TEST_RESULTS_SUMMARY));
    if (testResultsSummary != null && selectedModelsList.Contains(testResultsSummary))
    {
        // If "General Information" is selected, the test results group will be added to the results.
        results.Add(root);
        return results;
    }

    // If no model is selected, child models are recursively explored.
    var childrenGroup = root.GetChildren().Where(model => model.As(targetClass));
    foreach (var group in childrenGroup)
    {
        var childResults = GetTargetTestResultsGroups(group, selectedModelsList, targetClass);
        results.AddRange(childResults);
    }
    return results;
}

// ---------------------------------------
// Test result aggregation and general information update function
// For all General Information under the target Test Result Group, the test results will be aggregated and updated.
// Arguments: Target test result group, target process class name
// Return value: List of results
// ---------------------------------------
private TestResultsCounts CountAndUpdateSummary(IModel testResultGroup, TestProcessClassNames targetProcess)
{
    var counter = new TestResultsCounts();

    // The subgroups are aggregated and updated first, and then the results are added together.
    var childrenGroups = testResultGroup.GetChildren().Where(model => model.As(targetProcess.TestResultsGroupClass));
    foreach (var group in childrenGroups)
    {
        var childCounts = CountAndUpdateSummary(group, targetProcess);
        counter.Planned += childCounts.Planned;
        counter.Actual += childCounts.Actual;
        counter.Ok += childCounts.Ok;
        counter.Ng += childCounts.Ng;
        counter.NotRun += childCounts.NotRun;
        counter.Excluded += childCounts.Excluded;
    }

    // Aggregate the direct test results.
    var childrenTestCases = testResultGroup.GetChildren().Where(model => model.As(targetProcess.TestResultClass));
    foreach (var testCase in childrenTestCases)
    {
        var status = testCase.GetFieldString(FIELD_NAME_TEST_RESULTS_STATUS);

        if (status != FIELD_VALUE_STATUS_EXCLUDED) counter.Planned++;
        if (status == FIELD_VALUE_STATUS_OK || status == FIELD_VALUE_STATUS_NG) counter.Actual++;
        if (status == FIELD_VALUE_STATUS_OK) counter.Ok++;
        if (status == FIELD_VALUE_STATUS_NG) counter.Ng++;
        if (status == FIELD_VALUE_STATUS_NOT_RUN) counter.NotRun++;
        if (status == FIELD_VALUE_STATUS_EXCLUDED) counter.Excluded++;
    }

    // Update the General Information.
    var summary = testResultGroup.GetChildren().FirstOrDefault(model => model.As(CLASS_NAME_TEST_RESULTS_SUMMARY));
    if (summary != null)
    {
        // The field will be updated.
        summary.SetField(FIELD_NAME_PLANNED_TEST_CASES, counter.Planned);
        summary.SetField(FIELD_NAME_ACTUAL_TEST_CASES, counter.Actual);
        summary.SetField(FIELD_NAME_OK_TEST_CASES, counter.Ok);
        summary.SetField(FIELD_NAME_NG_TEST_CASES, counter.Ng);
        summary.SetField(FIELD_NAME_NOT_RUN_TEST_CASES, counter.NotRun);
        summary.SetField(FIELD_NAME_EXCLUDED_TEST_CASES, counter.Excluded);

        // Add an error (Type: Information).
        summary.AddError
        (
            fields: FIELD_NAME_NAME,
            type: "Information",
            title: ERROR_TITLE_UPDATE_TEST_RESULTS_SUMMARY,
            message: ERROR_MSG_UPDATED_TEST_CASE_COUNTS
        );
    }

    return counter;
}

// =======================================
// Data structure definition
// =======================================

// A structure for aggregating test results.
private struct TestResultsCounts
{
    public int Planned;  // Number of planned test cases
    public int Actual;   // Actual number of test cases
    public int Ok;       // Number of OK test cases
    public int Ng;       // Number of Failed test cases
    public int NotRun;   // Number of unexecuted test cases
    public int Excluded; // Number of excluded test cases
};