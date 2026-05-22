// =======================================
// main.cs: Entry point for this extension
// =======================================

// This will load all files that were implemented in separate parts.
#load "updateId.cs"                              // Function: Update ID
#load "deriveTestResults.cs"                     // Function: Derives Test Result models.
#load "countTestResults.cs"                      // Function: Aggregates Test Results
#load "searchImpactedComponentsAndInterfaces.cs" // Function: Extracts the affected areas of the Interface.
#load "deriveSoftwareRequirements.cs"            // Function: Derives Software Requirement models.