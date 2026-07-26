import streamlit as st

from components.sidebar import render_sidebar
from components.page_header import page_header

from core.vector_store import VectorStore
from services.llm_service import LLMService
from services.paper_analyzer import PaperAnalyzer

from utils.helpers import load_css


st.set_page_config(
    page_title="Paper Analyzer | ResearchIQ",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_css()

render_sidebar()


page_header(
    eyebrow="DOCUMENT INTELLIGENCE",

    title="Paper",

    highlight="Analyzer",

    description=(
        "Transform academic papers into structured research "
        "intelligence covering objectives, methodology, "
        "findings, contributions, limitations and "
        "future directions."
    )
)


# =========================================================
# YOUR EXISTING PAPER ANALYZER CODE CONTINUES HERE
# =========================================================

# =========================================================
# SERVICES
# =========================================================

@st.cache_resource
def initialize_analyzer():

    vector_store = VectorStore()

    llm_service = LLMService()

    analyzer = PaperAnalyzer(
        vector_store,
        llm_service
    )

    return analyzer, vector_store


try:

    analyzer, vector_store = (
        initialize_analyzer()
    )

except Exception as exc:

    st.error(
        f"Unable to initialize Paper Analyzer: {exc}"
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

header_html = (
    '<div class="ri-eyebrow">'
    'RESEARCH INTELLIGENCE'
    '</div>'
    '<div class="ri-title" '
    'style="font-size:3.2rem;">'
    'Paper '
    '<span class="ri-gradient">'
    'Analyzer'
    '</span>'
    '</div>'
    '<div class="ri-description">'
    'Transform academic papers into structured '
    'research intelligence including methodology, '
    'findings, contributions, limitations and '
    'future research directions.'
    '</div>'
)

st.markdown(
    header_html,
    unsafe_allow_html=True
)


st.write("")


# =========================================================
# DATABASE STATUS
# =========================================================

vector_count = vector_store.count()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Knowledge Vectors",
    vector_count
)


documents = analyzer.get_documents()

c2.metric(
    "Indexed Documents",
    len(documents)
)


c3.metric(
    "Analysis Engine",
    "Gemini"
)


st.divider()


# =========================================================
# DOCUMENT SELECTION
# =========================================================

st.markdown(
    "## Select research paper"
)


if not documents:

    st.warning(
        "No indexed research documents were found. "
        "Upload and index a paper from Knowledge Library."
    )

    st.stop()


selected_document = st.selectbox(
    "Research document",
    documents
)


st.caption(
    "The analysis is generated from the indexed "
    "evidence belonging to the selected document."
)


analyze_button = st.button(
    "Analyze Research Paper",
    type="primary",
    use_container_width=False
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    with st.status(
        "Analyzing research paper...",
        expanded=True
    ) as status:

        try:

            st.write(
                "Retrieving document evidence..."
            )

            chunks = (
                analyzer.get_document_chunks(
                    selected_document
                )
            )

            st.write(
                f"Found {len(chunks)} "
                "indexed research chunks."
            )

            st.write(
                "Building academic evidence context..."
            )

            st.write(
                "Generating structured analysis..."
            )

            result = analyzer.analyze(
                selected_document
            )

            status.update(
                label="Research analysis complete",
                state="complete",
                expanded=False
            )

        except Exception as exc:

            status.update(
                label="Analysis failed",
                state="error"
            )

            st.error(
                f"Paper analysis failed: {exc}"
            )

            st.stop()


    # =====================================================
    # RESULTS
    # =====================================================

    st.write("")
    st.markdown(
        "## Research Intelligence Report"
    )


    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Chunks analyzed",
        result["chunks_analyzed"]
    )

    c2.metric(
        "Context characters",
        f'{result["context_characters"]:,}'
    )

    c3.metric(
        "Source",
        result["filename"]
    )


    st.divider()


    st.markdown(
        result["analysis"]
    )


    # =====================================================
    # EXPORT
    # =====================================================

    st.divider()

    st.markdown(
        "### Export analysis"
    )

    report = (
        "# ResearchIQ Paper Analysis\n\n"
        f"Document: {result['filename']}\n\n"
        f"{result['analysis']}\n"
    )

    st.download_button(
        label="Download Analysis Report",
        data=report,
        file_name=(
            f"{result['filename']}"
            "_research_analysis.md"
        ),
        mime="text/markdown"
    )
