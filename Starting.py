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
"""
SECURITY NOTE:
- Never commit API keys to version control
- For production, use environment variables or Azure Key Vault
- Rotate keys regularly
- Consider implementing key management system
"""

# Azure Document Intelligence endpoint and key
# Replace these with your actual values from Azure Portal
endpoint = "YOUR_ENDPOINT_HERE"  # e.g., "https://your-resource.cognitiveservices.azure.com/"
key = "YOUR_KEY_HERE"  # Your Azure Document Intelligence API key

# =============================================
# SAMPLE DOCUMENT
# =============================================
# You can use either a URL or local file path
# Option 1: URL to document
formUrl = "YOUR_DOCUMENT_URL_HERE"  # e.g., "https://example.com/your-document.pdf"

# Option 2: Local file path
local_file_path = "YOUR_LOCAL_FILE_PATH_HERE"  # e.g., "documents/sample.pdf"

# =============================================
# CLIENT INITIALIZATION
# =============================================
# Create the Document Intelligence client
document_intelligence_client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# =============================================
# DOCUMENT ANALYSIS
# =============================================
# Start the document analysis process
# For URL-based analysis:
poller = document_intelligence_client.begin_analyze_document(
    "prebuilt-layout", AnalyzeDocumentRequest(url_source=formUrl)
)

# For local file analysis:
# with open(local_file_path, "rb") as f:
#     poller = document_intelligence_client.begin_analyze_document(
#         "prebuilt-layout", AnalyzeDocumentRequest(file=f)
#     )

result = poller.result()

# =============================================
# STYLE ANALYSIS
# =============================================
for idx, style in enumerate(result.styles):
    print(
        "Document contains {} content".format(
         "handwritten" if style.is_handwritten else "no handwritten"
        )
    )

# =============================================
# PAGE CONTENT ANALYSIS
# =============================================
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

print("----------------------------------------") ### This is for presentation purposes only
