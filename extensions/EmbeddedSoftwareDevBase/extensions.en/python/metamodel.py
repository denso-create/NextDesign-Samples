"""Definition of Metamodel Information for Embedded Software Development Profiles

This defines the class names and field names defined in the profile so that they can be used in the extension.
"""

# ---------------------------------------
# Definition of field names common to each process
# ---------------------------------------
FIELD_NAME_NAME = "Name"
FIELD_NAME_ID = "ID"

# ---------------------------------------
# Definition related to requirements analysis
# ---------------------------------------
# Requirements Analysis class name
CLASS_NAME_SYSTEM_REQUIREMENTS_ANALYSIS = "SystemRequirementAnalysis"
CLASS_NAME_SOFTWARE_REQUIREMENTS_ANALYSIS = "SoftwareRequirementAnalysis"

# Requirement group class name
CLASS_NAME_SYSTEM_REQUIREMENTS_GROUP = "SystemRequirementGroup"
CLASS_NAME_SOFTWARE_REQUIREMENTS_GROUP = "SoftwareRequirementGroup"

# Requirement class name
CLASS_NAME_SYSTEM_REQUIREMENT = "SystemRequirement"
CLASS_NAME_SOFTWARE_REQUIREMENT = "SoftwareRequirement"

# Field names related to Software Requirement
FIELD_NAME_REQUIREMENTS_GROUP = "SoftwareRequirementGroup"
FIELD_NAME_SOFTWARE_REQUIREMENTS_SUB_GROUPS = "SoftwareRequirementSubgroup"
FIELD_NAME_SOFTWARE_REQUIREMENTS = "SoftwareRequirement"
FIELD_NAME_INPUT_SYSTEM_REQUIREMENT = "Input_SystemRequirement"

# ---------------------------------------
# Definition related to test
# ---------------------------------------
# Test process class name
CLASS_NAME_SOFTWARE_TEST = "SoftwareTest"
CLASS_NAME_SOFTWARE_COMPONENT_TEST = "SoftwareComponentTest"
CLASS_NAME_SOFTWARE_INTEGRATION_TEST = "SoftwareIntegrationTest"

# Test case group class name
CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_TEST = "TestCaseGroup_SoftwareTest"
CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_COMPONENT_TEST = "TestCaseGroup_SoftwareComponentTest"
CLASS_NAME_TEST_CASES_GROUP_SOFTWARE_INTEGRATION_TEST = "TestCaseGroup_SoftwareIntegrationTest"

# Test case class name
CLASS_NAME_TEST_CASE_SOFTWARE_TEST = "TestCase_SoftwareTest"
CLASS_NAME_TEST_CASE_SOFTWARE_COMPONENT_TEST = "TestCase_SoftwareComponentTest"
CLASS_NAME_TEST_CASE_SOFTWARE_INTEGRATION_TEST = "TestCase_SoftwareIntegrationTest"

# Test result group class name
CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_TEST = "TestResultGroup_SoftwareTest"
CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_COMPONENT_TEST = "TestResultGroup_SoftwareComponentTest"
CLASS_NAME_TEST_RESULTS_GROUP_SOFTWARE_INTEGRATION_TEST = "TestResultGroup_SoftwareIntegrationTest"

# Test result class name
CLASS_NAME_TEST_RESULT_SOFTWARE_TEST = "TestResult_SoftwareTest"
CLASS_NAME_TEST_RESULT_SOFTWARE_COMPONENT_TEST = "TestResult_SoftwareComponentTest"
CLASS_NAME_TEST_RESULT_SOFTWARE_INTEGRATION_TEST = "TestResult_SoftwareIntegrationTest"

# General information class name
CLASS_NAME_TEST_RESULTS_SUMMARY = "GeneralInformation"

# Field names related to test
FIELD_NAME_TEST_CASE_GROUPS = "TestCaseGroup"
FIELD_NAME_TEST_CASE_SUB_GROUPS = "TestCaseSubgroup"
FIELD_NAME_TEST_RESULTS_GROUPS = "TestResultGroup"
FIELD_NAME_TEST_RESULTS_SUB_GROUPS = "TestResultSubgroup"
FIELD_NAME_TEST_CASES = "TestCase"
FIELD_NAME_TEST_RESULTS = "TestResult"
FIELD_NAME_TEST_RESULTS_SUMMARY = "GeneralInformation"
FIELD_NAME_TEST_RESULTS_STATUS = "Pass_FailStatus"

# Field names in the general information
FIELD_NAME_PLANNED_TEST_CASES = "NumberofPlannedTestCases"
FIELD_NAME_ACTUAL_TEST_CASES = "NumberofActualTestCases"
FIELD_NAME_OK_TEST_CASES = "NumberofPassedTestCases"
FIELD_NAME_NG_TEST_CASES = "NumberofFailedTestCases"
FIELD_NAME_NOT_RUN_TEST_CASES = "NumberofUnexecutedTestCases"
FIELD_NAME_EXCLUDED_TEST_CASES = "NumberofUntargetedTestCases"

# Pass/Fail status value
FIELD_VALUE_STATUS_OK = "OK"
FIELD_VALUE_STATUS_NG = "NG"
FIELD_VALUE_STATUS_NOT_RUN = "Undecided"
FIELD_VALUE_STATUS_EXCLUDED = "NotApplicable"

# ---------------------------------------
# Definitions of software architecture
# ---------------------------------------
# Software architecture class name
CLASS_NAME_PROVIDED_INTERFACE_SOFTWARE_COMPONENT = "Abst_ProvidedInterface_SoftwareComponent"
CLASS_NAME_SOFTWARE_COMPONENT_ARCHITECTURE_DESIGN = "SoftwareComponent_SoftwareArchitectureDesign"

# Interface field names
FIELD_NAME_USED_BY_COMPONENTS = "ConsumingSoftwareComponent"
FIELD_NAME_DELEGATED_INTERFACES = "DelegatedInterface"

# Component field names
FIELD_NAME_INTERFACE_FUNCTIONS = "InterfaceFunction"
FIELD_NAME_INTERFACE_DATA = "InterfaceData"

# =======================================
# Profile-dependent structure definitions
# =======================================

# A structure for managing class names for each test stage.
class TestProcessClassNames:
    def __init__(
        self,
        process_class: str,  # Test process class name
        test_cases_group_class: str,  # Test case group class name
        test_case_class: str,  # Test case class name
        test_results_group_class: str,  # Test result group class name
        test_result_class: str  # Test result class name
    ) -> None:
        self.process_class = process_class
        self.test_cases_group_class = test_cases_group_class
        self.test_case_class = test_case_class
        self.test_results_group_class = test_results_group_class
        self.test_result_class = test_result_class
