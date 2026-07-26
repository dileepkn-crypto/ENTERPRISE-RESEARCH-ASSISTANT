import streamlit as st

from components.sidebar import render_sidebar
from components.page_header import page_header

from core.vector_store import VectorStore

from utils.helpers import load_css


st.set_page_config(
    page_title=(
        "ResearchIQ | "
        "Academic Knowledge Intelligence"
    ),
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_css()



render_sidebar()


# =========================================================
# VECTOR STORE
# =========================================================

@st.cache_resource
def initialize_vector_store():

    return VectorStore()


try:

    vector_store = (
        initialize_vector_store()
    )

    vector_count = (
        vector_store.count()
    )

    engine_online = True

    engine_error = None

except Exception as exc:

    vector_store = None

    vector_count = 0

    engine_online = False

    engine_error = str(exc)


# =========================================================
# PAGE HEADER
# =========================================================

page_header(

    eyebrow=(
        "RESEARCH KNOWLEDGE INTELLIGENCE"
    ),

    title=(
        "Turn research into"
    ),

    highlight=(
        "actionable knowledge."
    ),

    description=(
        "ResearchIQ combines semantic retrieval, "
        "hybrid search, cross-encoder reranking and "
        "evidence-grounded generative AI to help "
        "researchers explore, understand and synthesize "
        "large collections of academic knowledge."
    )
)


# =========================================================
# ENGINE STATUS
# =========================================================

if engine_online:

    if vector_count > 0:

        st.success(
            f"Knowledge engine online · "
            f"{vector_count} semantic vectors indexed"
        )

    else:

        st.warning(
            "Knowledge engine online · "
            "No research documents indexed yet."
        )

else:

    st.error(
        "ResearchIQ could not connect to "
        "the knowledge engine."
    )

    if engine_error:

        with st.expander(
            "Technical details"
        ):

            st.code(
                engine_error
            )


# =========================================================
# INTELLIGENCE OVERVIEW
# =========================================================

st.markdown(
    """
    <div class="ri-section-title">
        Intelligence Overview
    </div>

    <div class="ri-section-description">
        Current status of the ResearchIQ
        knowledge intelligence stack.
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2, col3, col4 = (
    st.columns(4)
)


with col1:

    st.metric(
        "Knowledge Vectors",
        vector_count
    )


with col2:

    st.metric(
        "Retrieval Engine",
        "Hybrid"
    )


with col3:

    st.metric(
        "Generation",
        "Gemini"
    )


with col4:

    st.metric(
        "Evidence",
        "Page-level"
    )


# =========================================================
# RESEARCH WORKSPACE
# =========================================================

st.markdown(
    """
    <div class="ri-section-title">
        Research Intelligence Workspace
    </div>

    <div class="ri-section-description">
        Explore the major capabilities available
        across the ResearchIQ platform.
    </div>
    """,
    unsafe_allow_html=True
)


row1_col1, row1_col2, row1_col3 = (
    st.columns(3)
)


with row1_col1:

    st.html(
        """
        <div class="ri-card">

            <div class="ri-card-label">
                AI RESEARCH ASSISTANT
            </div>

            <div class="ri-card-value">
                Research Copilot
            </div>

            <div class="ri-card-subtitle">
                Ask questions across indexed academic
                literature and receive evidence-grounded
                answers with traceable sources.
            </div>

        </div>
        """
    )


with row1_col2:

    st.html(
        """
        <div class="ri-card">

            <div class="ri-card-label">
                KNOWLEDGE MANAGEMENT
            </div>

            <div class="ri-card-value">
                Knowledge Library
            </div>

            <div class="ri-card-subtitle">
                Upload, process and index academic
                papers into the ResearchIQ
                knowledge base.
            </div>

        </div>
        """
    )


with row1_col3:

    st.html(
        """
        <div class="ri-card">

            <div class="ri-card-label">
                INTELLIGENT RETRIEVAL
            </div>

            <div class="ri-card-value">
                Semantic Search
            </div>

            <div class="ri-card-subtitle">
                Discover relevant academic evidence
                using meaning-aware retrieval.
            </div>

        </div>
        """
    )


st.write("")


row2_col1, row2_col2, row2_col3 = (
    st.columns(3)
)


with row2_col1:

    st.html(
        """
        <div class="ri-card">

            <div class="ri-card-label">
                DOCUMENT INTELLIGENCE
            </div>

            <div class="ri-card-value">
                Paper Analyzer
            </div>

            <div class="ri-card-subtitle">
                Extract objectives, methodologies,
                findings, limitations and future
                research directions.
            </div>

        </div>
        """
    )


with row2_col2:

    st.html(
        """
        <div class="ri-card">

            <div class="ri-card-label">
                CROSS-PAPER ANALYSIS
            </div>

            <div class="ri-card-value">
                Compare Papers
            </div>

            <div class="ri-card-subtitle">
                Compare methodologies, datasets,
                findings and limitations across
                academic papers.
            </div>

        </div>
        """
    )


with row2_col3:

    st.html(
        """
        <div class="ri-card">

            <div class="ri-card-label">
                RESEARCH DISCOVERY
            </div>

            <div class="ri-card-value">
                Research Gap Finder
            </div>

            <div class="ri-card-subtitle">
                Identify recurring limitations and
                candidate future research directions.
            </div>

        </div>
        """
    )


# =========================================================
# ARCHITECTURE
# =========================================================

st.markdown(
    """
    <div class="ri-section-title">
        Enterprise RAG Architecture
    </div>

    <div class="ri-section-description">
        Multi-stage retrieval and reasoning architecture
        for evidence-grounded academic intelligence.
    </div>
    """,
    unsafe_allow_html=True
)


with st.expander(
    "View ResearchIQ intelligence pipeline"
):

    st.markdown(
        """
**Research Documents**

↓

**PDF Processing & Text Extraction**

↓

**Intelligent Chunking**

↓

**Embedding Generation**

↓

**Vector Knowledge Base**

↓

**Research Query**

↓

**Dense Retrieval + BM25 Retrieval**

↓

**Reciprocal Rank Fusion**

↓

**Cross-Encoder Reranking**

↓

**Relevance Guard**

↓

**Evidence Context**

↓

**Gemini**

↓

**Grounded Answer + Sources**
"""
    )


# =========================================================
# FOOTER
# =========================================================

st.write("")
st.write("")

st.divider()


footer_left, footer_right = (
    st.columns([3, 1])
)


with footer_left:

    st.caption(
        "Built by Dileep K N"
    )

    st.caption(
        "ResearchIQ · AI Research & Academic "
        "Knowledge Intelligence Platform"
    )


with footer_right:

    st.caption(
        "Enterprise RAG"
    )
