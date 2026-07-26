import streamlit as st


def document_uploader(
    key: str = "research_document"
):

    return st.file_uploader(
        "Upload research document",
        type=[
            "pdf",
            "docx",
            "txt"
        ],
        accept_multiple_files=False,
        key=key,
        help=(
            "Supported formats: "
            "PDF, DOCX and TXT"
        )
    )