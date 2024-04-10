# !!! WARNING: Make sure you read my comments! --> {Diwas}
# Adobe License: http://www.apache.org/licenses/LICENSE-2.0
# PDF Extractor File Using Adobe SDK

import logging
import os.path
import zipfile
import json
import re

# Authentication Key (Adobe SDK)
PDF_SERVICES_CLIENT_ID = "dedee6b461214e23ba46091e2e621e9b"
PDF_SERVICES_CLIENT_SECRET = "p8e-i4Blx0SBppPl6oVzFEdem2vl9Y8xDL6B"
# Configure your absoulute path from root here ! ---> {Diwas}
abs_path = "/home/diwas/Downloads/Abstractive Summarizer (My Work)"
base_path = abs_path + "/Streamlit Summarizer App"


def run_sdk(pdf_file_name, output_file_name):
    from adobe.pdfservices.operation.auth.credentials import Credentials
    from adobe.pdfservices.operation.exception.exceptions import (
        ServiceApiException,
        ServiceUsageException,
        SdkException,
    )
    from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import (
        ExtractPDFOptions,
    )
    from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import (
        ExtractElementType,
    )
    from adobe.pdfservices.operation.execution_context import ExecutionContext
    from adobe.pdfservices.operation.io.file_ref import FileRef
    from adobe.pdfservices.operation.pdfops.extract_pdf_operation import (
        ExtractPDFOperation,
    )

    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    try:
        # Initial setup, create credentials instance.
        credentials = (
            Credentials.service_principal_credentials_builder()
            .with_client_id(PDF_SERVICES_CLIENT_ID)
            .with_client_secret(PDF_SERVICES_CLIENT_SECRET)
            .build()
        )

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/uploads/" + pdf_file_name)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = (
            ExtractPDFOptions.builder()
            .with_element_to_extract(ExtractElementType.TEXT)
            .build()
        )
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + "/output/" + output_file_name)
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")


def extract_relevant_text(output_file_name):
    zip_file_path = base_path + "/output/" + output_file_name
    # It is default so, yeah we gotta use it !
    json_file_name = "structuredData.json"

    # Checks if the text belongs to a paragraph (only way available to detect clean text)
    def check_paragraph(test_text):
        paragraph_pattern = r"//Document/Sect(?:\[\d+\])?/P(?:\[\d+\])?"
        list_pattern = r"//Document/Sect(?:\[\d+\])?/L/LI/LBody"
        return re.match(paragraph_pattern, test_text) or re.match(
            list_pattern, test_text
        )

    cleaned_text = ""
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        if json_file_name in zip_ref.namelist():
            with zip_ref.open(json_file_name) as json_file:
                data_dict = json.load(json_file)

            elements = data_dict["elements"]
            for element in elements:
                path = element["Path"]
                if check_paragraph(path):
                    cleaned_text += element["Text"]

        else:
            print(f"{json_file_name} not found in the zip file.")
    return cleaned_text
