// =======================================
// Definition of Metamodel Information for Embedded Software Development Profiles
// This defines the class names and field names defined in the profile so that they can be used in the extension.
// =======================================

// ---------------------------------------
// Definition of field names common to each process
// ---------------------------------------
const string FIELD_NAME_NAME = "Name";
const string FIELD_NAME_ID = "ID";

// ---------------------------------------
// Definition related to requirements analysis
// ---------------------------------------
// Requirements Analysis class name
const string CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS = "SystemRequirementAnalysis";
const string CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS = "SoftwareRequirementAnalysis";

// Requirement group class name
const string CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP = "SystemRequirementGroup";
const string CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP = "SoftwareRequirementGroup";

// Requirement class name
const string CLASS_NAME_SYSTEM_REQUIREMENT = "SystemRequirement";
const string CLASS_NAME_SOFTWARE_REQUIREMENT = "SoftwareRequirement";

// Field names related to Software Requirement
const string FIELD_NAME_REQUIREMENTS_GROUP = "SoftwareRequirementGroup";
const string FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS = "SoftwareRequirementSubgroup";
const string FIELD_NAME_SOFTWARE_REQUIREMENTS = "SoftwareRequirement";
const string FIELD_NAME_INPUT_SYSTEM_REQUIREMENT = "Input_SystemRequirement";

// ---------------------------------------
// Definition related to test
// ---------------------------------------
// Test process class name
const string CLASS_NAME_SOFTWARE_TEST = "SoftwareTest";
const string CLASS_NAME_SOFTWARE_COMPONENT_TEST = "SoftwareComponentTest";
const string CLASS_NAME_SOFTWARE_INTEGRATION_TEST = "SoftwareIntegrationTest";

// Test case group class name
const string CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST = "TestCaseGroup_SoftwareTest";
const string CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST = "TestCaseGroup_SoftwareComponentTest";
const string CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST = "TestCaseGroup_SoftwareIntegrationTest";

// Test case class name
const string CLASS_NAME_TEST_CASE_SOFTWARE_TEST = "TestCase_SoftwareTest";
const string CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST = "TestCase_SoftwareComponentTest";
const string CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST = "TestCase_SoftwareIntegrationTest";

// Test result group class name
const string CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_TEST = "TestResultGroup_SoftwareTest";
const string CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_COMPONENT_TEST = "TestResultGroup_SoftwareComponentTest";
const string CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_INTEGRATION_TEST = "TestResultGroup_SoftwareIntegrationTest";

// Test result class name
const string CLASS_NAME_TEST_RESULT_SOFTWARE_TEST = "TestResult_SoftwareTest";
const string CLASS_NAME_TEST_RESULT_SOFTWARE_COMPONENT_TEST = "TestResult_SoftwareComponentTest";
const string CLASS_NAME_TEST_RESULT_SOFTWARE_INTEGRATION_TEST = "TestResult_SoftwareIntegrationTest";

// General information class name
const string CLASS_NAME_TEST_RESULTS_SUMMARY = "GeneralInformation";

// Field names related to test
const string FIELD_NAME_TEST_CASE_GROUPS = "TestCaseGroup";
const string FIELD_NAME_TEST_CASE_SUB_GROUPS = "TestCaseSubgroup";
const string FIELD_NAME_TEST_RESULTS_GROUPS = "TestResultGroup";
const string FIELD_NAME_TEST_RESULTS_SUB_GROUPS = "TestResultSubgroup";
const string FIELD_NAME_TEST_CASES = "TestCase";
const string FIELD_NAME_TEST_RESULTS = "TestResult";
const string FIELD_NAME_TEST_RESULTS_SUMMARY = "GeneralInformation";
const string FIELD_NAME_TEST_RESULTS_STATUS = "Pass_FailStatus";

// Field names in the general information
const string FIELD_NAME_PLANNED_TEST_CASES = "NumberofPlannedTestCases";
const string FIELD_NAME_ACTUAL_TEST_CASES = "NumberofActualTestCases";
const string FIELD_NAME_OK_TEST_CASES = "NumberofPassedTestCases";
const string FIELD_NAME_NG_TEST_CASES = "NumberofFailedTestCases";
const string FIELD_NAME_NOT_RUN_TEST_CASES = "NumberofUnexecutedTestCases";
const string FIELD_NAME_EXCLUDED_TEST_CASES = "NumberofUntargetedTestCases";

// Pass/Fail status value
const string FIELD_VALUE_STATUS_OK = "OK";
const string FIELD_VALUE_STATUS_NG = "NG";
const string FIELD_VALUE_STATUS_NOT_RUN = "Undecided";
const string FIELD_VALUE_STATUS_EXCLUDED = "NotApplicable";

// ---------------------------------------
// Definitions of software architecture
// ---------------------------------------
// Software architecture class name
const string CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT = "Abst_ProvidedInterface_SoftwareComponent";
const string CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN = "SoftwareComponent_SoftwareArchitectureDesign";

// Interface field names
const string FIELD_NAME_USED_BY_COMPONENTS = "ConsumingSoftwareComponent";
const string FIELD_NAME_DELEGATED_INTERFACES = "DelegatedInterface";

// Component field names
const string FIELD_NAME_INTERFACE_FUNCTIONS = "InterfaceFunction";
const string FIELD_NAME_INTERFACE_DATA = "InterfaceData";

// =======================================
// Profile-dependent structure definitions
// =======================================

// A structure for managing class names for each test stage.
private struct TestProcessClassNames
{
    public string ProcessClass;          // Test process class name
    public string TestCasesGroupClass;   // Test case group class name
    public string TestCaseClass;         // Test case class name
    public string TestResultsGroupClass; // Test result group class name
    public string TestResultClass;       // Test result class name
};
