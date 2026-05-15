"""main.py : Entry point for this extension"""

from nd import * # Load NextDesign API intellisense information.

# This will load all files that were implemented in separate parts.
from update_id import update_id # Function: Update ID
from derive_test_results import derive_test_results # Function: Derives Test Result models.
from count_test_results import count_test_results # Function: Aggregates Test Results
from search_impacted_components_and_interfaces import search_impacted_components_and_interfaces # Function: Extracts the affected areas of the Interface.
from derive_software_requirements import derive_software_requirements # Function: Derives Software Requirement models.
