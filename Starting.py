"""
This code sample shows Prebuilt Layout operations with the Azure AI Document Intelligence client library.
The async versions of the samples require Python 3.8 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""

# =============================================
# IMPORTS AND DEPENDENCIES
# =============================================
# Required packages:
# - azure-ai-documentintelligence
# - azure-core
# These can be installed using pip:
# pip install azure-ai-documentintelligence

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

# =============================================
# AZURE CONFIGURATION
# =============================================

# Azure Document Intelligence endpoint and key
# Replace these with your actual values from Azure Portal
endpoint = "YOUR_ENDPOINT_HERE"
key = "YOUR_KEY_HERE"

# =============================================
# SAMPLE DOCUMENT
# =============================================
# Using a sample PDF from Azure's GitHub repository
# You can replace this with your own document URL
formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"
# Replace this path with your local file path
#local_file_path = "path/to/your/document.pdf"
# =============================================
# CLIENT INITIALIZATION
# =============================================
# Create the Document Intelligence client
# This client will be used for all API calls
document_intelligence_client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# =============================================
# DOCUMENT ANALYSIS
# =============================================
# Start the document analysis process
# - Uses "prebuilt-layout" model for general document analysis
# - Returns a poller object for async operation
# - The analysis is performed on the document at the specified URL
poller = document_intelligence_client.begin_analyze_document(
    "prebuilt-layout", AnalyzeDocumentRequest(url_source=formUrl)
)
result = poller.result()

# =============================================
# STYLE ANALYSIS
# =============================================
# Check if the document contains any handwritten content
# This is useful for documents that might contain both printed and handwritten text
for idx, style in enumerate(result.styles):
    print(
        "Document contains {} content".format(
         "handwritten" if style.is_handwritten else "no handwritten"
        )
    )

# =============================================
# PAGE CONTENT ANALYSIS
# =============================================
# Process each page in the document
for page in result.pages:
    # Extract and print all text lines
    for line_idx, line in enumerate(page.lines):
        print(
         "...Line # {} has text content '{}'".format(
        line_idx,
        line.content.encode("utf-8")
        )
    )

    # Process selection marks (checkboxes, radio buttons)
    for selection_mark in page.selection_marks:
        print(
         "...Selection mark is '{}' and has a confidence of {}".format(
         selection_mark.state,
         selection_mark.confidence
         )
    )

# =============================================
# TABLE ANALYSIS
# =============================================
# Process all tables in the document
for table_idx, table in enumerate(result.tables):
    # Print table dimensions
    print(
        "Table # {} has {} rows and {} columns".format(
        table_idx, table.row_count, table.column_count
        )
    )
    
    # Process each cell in the table
    for cell in table.cells:
        print(
            "...Cell[{}][{}] has content '{}'".format(
            cell.row_index,
            cell.column_index,
            cell.content.encode("utf-8"),
            )
        )

print("----------------------------------------")
### This is for presentation purposes
