"""組込みソフト開発プロファイルのメタモデル情報の定義

プロファイルで定義されているクラス名やフィールド名をエクステンションで使うために定義します。
"""

# ---------------------------------------
# 各工程で共通するフィールド名の定義
# ---------------------------------------
FIELD_NAME_NAME = "Name"
FIELD_NAME_ID = "ID"

# ---------------------------------------
# 要求分析に関する定義
# ---------------------------------------
# 要求分析のクラス名
CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS = "SystemRequirementAnalysis"
CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS = "SoftwareRequirementAnalysis"

# 要求グループのクラス名
CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP = "SystemRequirementGroup"
CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP = "SoftwareRequirementGroup"

# 要求のクラス名
CLASS_NAME_SYSTEM_REQUIREMENT = "SystemRequirement"
CLASS_NAME_SOFTWARE_REQUIREMENT = "SoftwareRequirement"

# ソフトウェア要求に関するフィールド名
FIELD_NAME_REQUIREMENTS_GROUP = "SoftwareRequirementGroup"
FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS = "SoftwareRequirementSubgroup"
FIELD_NAME_SOFTWARE_REQUIREMENTS = "SoftwareRequirement"
FIELD_NAME_INPUT_SYSTEM_REQUIREMENT = "Input_SystemRequirement"

# ---------------------------------------
# テストに関する定義
# ---------------------------------------
# テスト工程のクラス名
CLASS_NAME_SOFTWARE_TEST = "SoftwareTest"
CLASS_NAME_SOFTWARE_COMPONENT_TEST = "SoftwareComponentTest"
CLASS_NAME_SOFTWARE_INTEGRATION_TEST = "SoftwareIntegrationTest"

# テストケースグループのクラス名
CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST = "TestCaseGroup_SoftwareTest"
CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST = "TestCaseGroup_SoftwareComponentTest"
CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST = "TestCaseGroup_SoftwareIntegrationTest"

# テストケースのクラス名
CLASS_NAME_TEST_CASE_SOFTWARE_TEST = "TestCase_SoftwareTest"
CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST = "TestCase_SoftwareComponentTest"
CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST = "TestCase_SoftwareIntegrationTest"

# テスト結果グループのクラス名
CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_TEST = "TestResultGroup_SoftwareTest"
CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_COMPONENT_TEST = "TestResultGroup_SoftwareComponentTest"
CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_INTEGRATION_TEST = "TestResultGroup_SoftwareIntegrationTest"

# テスト結果のクラス名
CLASS_NAME_TEST_RESULT_SOFTWARE_TEST = "TestResult_SoftwareTest"
CLASS_NAME_TEST_RESULT_SOFTWARE_COMPONENT_TEST = "TestResult_SoftwareComponentTest"
CLASS_NAME_TEST_RESULT_SOFTWARE_INTEGRATION_TEST = "TestResult_SoftwareIntegrationTest"

# 総合情報のクラス名
CLASS_NAME_TEST_RESULTS_SUMMARY = "GeneralInformation"

# テストに関するフィールド名
FIELD_NAME_TEST_CASE_GROUPS = "TestCaseGroup"
FIELD_NAME_TEST_CASE_SUB_GROUPS = "TestCaseSubgroup"
FIELD_NAME_TEST_RESULTS_GROUPS = "TestResultGroup"
FIELD_NAME_TEST_RESULTS_SUB_GROUPS = "TestResultSubgroup"
FIELD_NAME_TEST_CASES = "TestCase"
FIELD_NAME_TEST_RESULTS = "TestResult"
FIELD_NAME_TEST_RESULTS_SUMMARY = "GeneralInformation"
FIELD_NAME_TEST_RESULTS_STATUS = "Pass_FailStatus"

# 総合情報のフィールド名
FIELD_NAME_PLANNED_TEST_CASES = "NumberofPlannedTestCases"
FIELD_NAME_ACTUAL_TEST_CASES = "NumberofActualTestCases"
FIELD_NAME_OK_TEST_CASES = "NumberofPassedTestCases"
FIELD_NAME_NG_TEST_CASES = "NumberofFailedTestCases"
FIELD_NAME_NOT_RUN_TEST_CASES = "NumberofUnexecutedTestCases"
FIELD_NAME_EXCLUDED_TEST_CASES = "NumberofUntargetedTestCases"

# 合否ステータスの値
FIELD_VALUE_STATUS_OK = "OK"
FIELD_VALUE_STATUS_NG = "NG"
FIELD_VALUE_STATUS_NOT_RUN = "Undecided"
FIELD_VALUE_STATUS_EXCLUDED = "NotApplicable"

# ---------------------------------------
# ソフトウェアアーキテクチャに関する定義
# ---------------------------------------
# ソフトウェアアーキテクチャのクラス名
CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT = "Abst_ProvidedInterface_SoftwareComponent"
CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN = "SoftwareComponent_SoftwareArchitectureDesign"

# インタフェースのフィールド名
FIELD_NAME_USED_BY_COMPONENTS = "ConsumingSoftwareComponent"
FIELD_NAME_DELEGATED_INTERFACES = "DelegatedInterface"

# コンポーネントのフィールド名
FIELD_NAME_INTERFACE_FUNCTIONS = "InterfaceFunction"
FIELD_NAME_INTERFACE_DATA = "InterfaceData"

# =======================================
# プロファイルに依存する構造体定義
# =======================================

# テスト工程毎のクラス名をまとめて管理する構造体
class TestProcessClassNames:
    def __init__(
        self,
        process_class: str,  # テスト工程のクラス名
        test_cases_group_class: str,  # テストケースグループクラス名
        test_case_class: str,  # テストケースクラス名
        test_results_group_class: str,  # テスト結果グループクラス名
        test_result_class: str  # テスト結果クラス名
    ) -> None:
        self.process_class = process_class
        self.test_cases_group_class = test_cases_group_class
        self.test_case_class = test_case_class
        self.test_results_group_class = test_results_group_class
        self.test_result_class = test_result_class