// =======================================
// 組込みソフト開発プロファイルのメタモデル情報の定義
// プロファイルで定義されているクラス名やフィールド名をエクステンションで使うために定義します。
// =======================================

// ---------------------------------------
// 各工程で共通するフィールド名の定義
// ---------------------------------------
const string FIELD_NAME_NAME = "Name";
const string FIELD_NAME_ID = "ID";

// ---------------------------------------
// 要求分析に関する定義
// ---------------------------------------
// 要求分析のクラス名
const string CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS = "SystemRequirementAnalysis";
const string CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS = "SoftwareRequirementAnalysis";

// 要求グループのクラス名
const string CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP = "SystemRequirementGroup";
const string CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP = "SoftwareRequirementGroup";

// 要求のクラス名
const string CLASS_NAME_SYSTEM_REQUIREMENT = "SystemRequirement";
const string CLASS_NAME_SOFTWARE_REQUIREMENT = "SoftwareRequirement";

// ソフトウェア要求に関するフィールド名
const string FIELD_NAME_REQUIREMENTS_GROUP = "SoftwareRequirementGroup";
const string FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS = "SoftwareRequirementSubgroup";
const string FIELD_NAME_SOFTWARE_REQUIREMENTS = "SoftwareRequirement";
const string FIELD_NAME_INPUT_SYSTEM_REQUIREMENT = "Input_SystemRequirement";

// ---------------------------------------
// テストに関する定義
// ---------------------------------------
// テスト工程のクラス名
const string CLASS_NAME_SOFTWARE_TEST = "SoftwareTest";
const string CLASS_NAME_SOFTWARE_COMPONENT_TEST = "SoftwareComponentTest";
const string CLASS_NAME_SOFTWARE_INTEGRATION_TEST = "SoftwareIntegrationTest";

// テストケースグループのクラス名
const string CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST = "TestCaseGroup_SoftwareTest";
const string CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST = "TestCaseGroup_SoftwareComponentTest";
const string CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST = "TestCaseGroup_SoftwareIntegrationTest";

// テストケースのクラス名
const string CLASS_NAME_TEST_CASE_SOFTWARE_TEST = "TestCase_SoftwareTest";
const string CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST = "TestCase_SoftwareComponentTest";
const string CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST = "TestCase_SoftwareIntegrationTest";

// テスト結果グループのクラス名
const string CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_TEST = "TestResultGroup_SoftwareTest";
const string CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_COMPONENT_TEST = "TestResultGroup_SoftwareComponentTest";
const string CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_INTEGRATION_TEST = "TestResultGroup_SoftwareIntegrationTest";

// テスト結果のクラス名
const string CLASS_NAME_TEST_RESULT_SOFTWARE_TEST = "TestResult_SoftwareTest";
const string CLASS_NAME_TEST_RESULT_SOFTWARE_COMPONENT_TEST = "TestResult_SoftwareComponentTest";
const string CLASS_NAME_TEST_RESULT_SOFTWARE_INTEGRATION_TEST = "TestResult_SoftwareIntegrationTest";

// 総合情報のクラス名
const string CLASS_NAME_TEST_RESULTS_SUMMARY = "GeneralInformation";

// テストに関するフィールド名
const string FIELD_NAME_TEST_CASE_GROUPS = "TestCaseGroup";
const string FIELD_NAME_TEST_CASE_SUB_GROUPS = "TestCaseSubgroup";
const string FIELD_NAME_TEST_RESULTS_GROUPS = "TestResultGroup";
const string FIELD_NAME_TEST_RESULTS_SUB_GROUPS = "TestResultSubgroup";
const string FIELD_NAME_TEST_CASES = "TestCase";
const string FIELD_NAME_TEST_RESULTS = "TestResult";
const string FIELD_NAME_TEST_RESULTS_SUMMARY = "GeneralInformation";
const string FIELD_NAME_TEST_RESULTS_STATUS = "Pass_FailStatus";

// 総合情報のフィールド名
const string FIELD_NAME_PLANNED_TEST_CASES = "NumberofPlannedTestCases";
const string FIELD_NAME_ACTUAL_TEST_CASES = "NumberofActualTestCases";
const string FIELD_NAME_OK_TEST_CASES = "NumberofPassedTestCases";
const string FIELD_NAME_NG_TEST_CASES = "NumberofFailedTestCases";
const string FIELD_NAME_NOT_RUN_TEST_CASES = "NumberofUnexecutedTestCases";
const string FIELD_NAME_EXCLUDED_TEST_CASES = "NumberofUntargetedTestCases";

// 合否ステータスの値
const string FIELD_VALUE_STATUS_OK = "OK";
const string FIELD_VALUE_STATUS_NG = "NG";
const string FIELD_VALUE_STATUS_NOT_RUN = "Undecided";
const string FIELD_VALUE_STATUS_EXCLUDED = "NotApplicable";

// ---------------------------------------
// ソフトウェアアーキテクチャに関する定義
// ---------------------------------------
// ソフトウェアアーキテクチャのクラス名
const string CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT = "Abst_ProvidedInterface_SoftwareComponent";
const string CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN = "SoftwareComponent_SoftwareArchitectureDesign";

// インタフェースのフィールド名
const string FIELD_NAME_USED_BY_COMPONENTS = "ConsumingSoftwareComponent";
const string FIELD_NAME_DELEGATED_INTERFACES = "DelegatedInterface";

// コンポーネントのフィールド名
const string FIELD_NAME_INTERFACE_FUNCTIONS = "InterfaceFunction";
const string FIELD_NAME_INTERFACE_DATA = "InterfaceData";

// =======================================
// プロファイルに依存する構造体定義
// =======================================

// テスト工程毎のクラス名をまとめて管理する構造体
private struct TestProcessClassNames
{
    public string ProcessClass;          // テスト工程のクラス名
    public string TestCasesGroupClass;   // テストケースグループクラス名
    public string TestCaseClass;         // テストケースクラス名
    public string TestResultsGroupClass; // テスト結果グループクラス名
    public string TestResultClass;       // テスト結果クラス名
};
