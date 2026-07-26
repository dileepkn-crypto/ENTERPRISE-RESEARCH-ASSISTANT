from pathlib import Path

import streamlit as st

from components.sidebar import render_sidebar
from components.page_header import page_header
from components.upload_component import document_uploader

from core.embeddings import EmbeddingService
from core.vector_store import VectorStore
from services.ingestion_service import IngestionService

from utils.config import DOCUMENTS_PATH
from utils.helpers import load_css


st.set_page_config(
    page_title="Knowledge Library | ResearchIQ",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_css()

render_sidebar()


page_header(
    eyebrow="KNOWLEDGE MANAGEMENT",

    title="Knowledge",

    highlight="Library",

    description=(
        "Upload, index and manage the academic documents "
        "that power your ResearchIQ knowledge base."
    )
)


# =========================================================
# YOUR EXISTING KNOWLEDGE LIBRARY CODE CONTINUES HERE
# =========================================================


@st.cache_resource
def initialize_ingestion():

    embedding_service = (
        EmbeddingService()
    )

    vector_store = (
        VectorStore()
    )

    ingestion = (
        IngestionService(
            embedding_service,
            vector_store
        )
    )

    return ingestion, vector_store


ingestion_service, vector_store = (
    initialize_ingestion()
)


st.metric(
    "Indexed knowledge vectors",
    vector_store.count()
)


st.divider()


uploaded_file = document_uploader()


if uploaded_file:

    st.markdown(
        "### Document"
    )

    c1, c2 = st.columns(
        [3, 1]
    )

    with c1:

        st.write(
            f"**{uploaded_file.name}**"
        )

        st.caption(
            f"{uploaded_file.size / 1024:.1f} KB"
        )

    with c2:

        index_button = st.button(
            "Index document",
            type="primary",
            use_container_width=True
        )


    if index_button:

        # Basic filename sanitization
        safe_name = Path(
            uploaded_file.name
        ).name

        destination = (
            DOCUMENTS_PATH
            / safe_name
        )

        file_bytes = (
            uploaded_file.getvalue()
        )

        destination.write_bytes(
            file_bytes
        )

        with st.status(
            "Building research knowledge...",
            expanded=True
        ) as status:

            try:

                st.write(
                    "Extracting document text..."
                )

                st.write(
                    "Creating semantic chunks..."
                )

                st.write(
                    "Generating embeddings..."
                )

                result = (
                    ingestion_service.ingest(
                        destination
                    )
                )

                st.write(
                    "Persisting vectors to ChromaDB..."
                )

                status.update(
                    label="Document indexed successfully",
                    state="complete",
                    expanded=True
                )

            except Exception as exc:

                status.update(
                    label="Indexing failed",
                    state="error"
                )

                st.error(str(exc))

                st.stop()


        st.success(
            f"{result['filename']} added to ResearchIQ."
        )


        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Pages",
            result["pages"]
        )

        c2.metric(
            "Chunks",
            result["chunks"]
        )

        c3.metric(
            "Stored vectors",
            result["stored"]
        )


st.divider()


# ---------------------------------------------------------
# Local library
# ---------------------------------------------------------

st.subheader(
    "Indexed files"
)

documents = [
    file
    for file in DOCUMENTS_PATH.iterdir()
    if file.is_file()
    and not file.name.startswith(".")
]


if not documents:

    st.info(
        "No research documents uploaded yet."
    )

else:

    for document in documents:

        with st.container(
            border=True
        ):

            c1, c2 = st.columns(
                [4, 1]
            )

            with c1:

                st.write(
                    f"**{document.name}**"
                )

                st.caption(
                    document.suffix.upper().replace(
                        ".",
                        ""
                    )
                )

            with c2:

                size = (
                    document.stat().st_size
                    / 1024
                )

                st.caption(
                    f"{size:.1f} KB"
                )
