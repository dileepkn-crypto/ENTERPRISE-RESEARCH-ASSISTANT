import streamlit as st

from components.sidebar import render_sidebar
from components.page_header import page_header
from components.source_card import source_card

from core.embeddings import EmbeddingService
from core.vector_store import VectorStore
from core.retriever import ResearchRetriever
from services.search_service import SearchService

from utils.helpers import load_css


st.set_page_config(
    page_title="Semantic Search | ResearchIQ",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_css()

render_sidebar()


page_header(
    eyebrow="INTELLIGENT RETRIEVAL",

    title="Semantic",

    highlight="Search",

    description=(
        "Discover relevant academic evidence using "
        "meaning-aware semantic retrieval across your "
        "indexed research knowledge."
    )
)


# =========================================================
# YOUR EXISTING SEMANTIC SEARCH CODE CONTINUES HERE
# =========================================================

@st.cache_resource
def initialize_search():

    embedding_service = (
        EmbeddingService()
    )

    vector_store = (
        VectorStore()
    )

    retriever = (
        ResearchRetriever(
            embedding_service,
            vector_store
        )
    )

    search_service = (
        SearchService(
            retriever
        )
    )

    return search_service, vector_store


search_service, vector_store = (
    initialize_search()
)


st.caption(
    f"{vector_store.count()} vectors available"
)


st.divider()


query = st.text_input(
    "Search research knowledge",
    placeholder=(
        "e.g. How is deep learning used "
        "in mobile applications?"
    )
)


top_k = st.slider(
    "Number of results",
    min_value=1,
    max_value=10,
    value=5
)


search = st.button(
    "Search knowledge",
    type="primary"
)


if search:

    if not query.strip():

        st.warning(
            "Enter a search query."
        )

    elif vector_store.count() == 0:

        st.warning(
            "The knowledge base is empty."
        )

    else:

        with st.spinner(
            "Searching semantic knowledge..."
        ):

            results = (
                search_service.search(
                    query=query,
                    top_k=top_k
                )
            )


        st.markdown(
            f"### {len(results)} relevant passages"
        )


        for index, result in enumerate(
            results,
            start=1
        ):

            result["source_id"] = (
                f"S{index}"
            )

            source_card(
                result,
                expanded=(
                    index == 1
                )
            )
