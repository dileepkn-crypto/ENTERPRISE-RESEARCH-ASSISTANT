import streamlit as st

from components.sidebar import render_sidebar
from components.page_header import page_header

from core.vector_store import VectorStore
from services.comparison_service import ComparisonService
from services.llm_service import LLMService

from utils.helpers import load_css


st.set_page_config(
    page_title="Compare Papers | ResearchIQ",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_css()

render_sidebar()


page_header(
    eyebrow="CROSS-DOCUMENT INTELLIGENCE",

    title="Compare",

    highlight="Research Papers",

    description=(
        "Compare research problems, methodologies, datasets, "
        "models, findings, contributions and limitations "
        "across academic papers."
    )
)


# =========================================================
# YOUR EXISTING COMPARE PAPERS CODE CONTINUES HERE
# =========================================================


# =========================================================
# INITIALIZE SERVICES
# =========================================================

@st.cache_resource
def initialize_comparison():

    vector_store = VectorStore()

    llm_service = LLMService()

    comparison_service = (
        ComparisonService(
            vector_store,
            llm_service
        )
    )

    return (
        comparison_service,
        vector_store
    )


try:

    comparison_service, vector_store = (
        initialize_comparison()
    )

except Exception as exc:

    st.error(
        f"Unable to initialize comparison engine: {exc}"
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

header_html = (
    '<div class="ri-eyebrow">'
    'CROSS-DOCUMENT INTELLIGENCE'
    '</div>'

    '<div class="ri-title" '
    'style="font-size:3.2rem;">'

    'Compare '

    '<span class="ri-gradient">'
    'Research Papers'
    '</span>'

    '</div>'

    '<div class="ri-description">'

    'Compare research problems, methodologies, datasets, '
    'models, findings, contributions and limitations '
    'across multiple academic papers using grounded '
    'research evidence.'

    '</div>'
)

st.markdown(
    header_html,
    unsafe_allow_html=True
)


st.write("")


# =========================================================
# KNOWLEDGE BASE
# =========================================================

documents = (
    comparison_service.get_documents()
)

vector_count = (
    vector_store.count()
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Knowledge Vectors",
        vector_count
    )


with c2:

    st.metric(
        "Indexed Papers",
        len(documents)
    )


with c3:

    if len(documents) >= 2:

        st.success(
            "Comparison engine ready"
        )

    else:

        st.warning(
            "At least 2 papers required"
        )


st.divider()


# =========================================================
# REQUIRE TWO PAPERS
# =========================================================

if len(documents) < 2:

    st.warning(
        "Multi-paper comparison requires at least "
        "two different indexed research papers."
    )

    st.info(
        "Open Knowledge Library, upload another "
        "research paper, index it, and return here."
    )

    st.stop()


# =========================================================
# PAPER SELECTION
# =========================================================

st.markdown(
    "## Select papers"
)

st.caption(
    "Choose two different indexed papers to perform "
    "an evidence-grounded academic comparison."
)


paper_col1, paper_col2 = (
    st.columns(2)
)


with paper_col1:

    st.markdown(
        "### Paper A"
    )

    paper_a = st.selectbox(
        "Select first research paper",
        documents,
        index=0,
        key="comparison_paper_a"
    )


with paper_col2:

    st.markdown(
        "### Paper B"
    )

    default_b = (
        1
        if len(documents) > 1
        else 0
    )

    paper_b = st.selectbox(
        "Select second research paper",
        documents,
        index=default_b,
        key="comparison_paper_b"
    )


# =========================================================
# VALIDATION
# =========================================================

if paper_a == paper_b:

    st.warning(
        "Select two different research papers."
    )


st.write("")


compare_button = st.button(
    "Compare Research Papers",
    type="primary",
    disabled=(
        paper_a == paper_b
    )
)


# =========================================================
# COMPARISON
# =========================================================

if compare_button:

    with st.status(
        "Comparing research papers...",
        expanded=True
    ) as status:

        try:

            st.write(
                f"Retrieving evidence from "
                f"{paper_a}..."
            )

            st.write(
                f"Retrieving evidence from "
                f"{paper_b}..."
            )

            st.write(
                "Aligning research dimensions..."
            )

            st.write(
                "Comparing methodologies and findings..."
            )

            st.write(
                "Generating cross-document "
                "research synthesis..."
            )

            result = (
                comparison_service.compare(
                    paper_a,
                    paper_b
                )
            )

            status.update(
                label=(
                    "Research comparison complete"
                ),
                state="complete",
                expanded=False
            )

        except Exception as exc:

            status.update(
                label="Comparison failed",
                state="error"
            )

            st.error(
                f"Comparison failed: {exc}"
            )

            st.stop()


    # =====================================================
    # RESULT HEADER
    # =====================================================

    st.write("")
    st.markdown(
        "## Comparative Intelligence Report"
    )


    # =====================================================
    # PAPER METRICS
    # =====================================================

    c1, c2 = st.columns(2)


    with c1:

        st.markdown(
            f"### Paper A"
        )

        st.write(
            f"**{result['paper_a']}**"
        )

        st.metric(
            "Evidence chunks",
            result["paper_a_chunks"]
        )

        st.caption(
            f"{result['paper_a_context']:,} "
            "context characters analyzed"
        )


    with c2:

        st.markdown(
            f"### Paper B"
        )

        st.write(
            f"**{result['paper_b']}**"
        )

        st.metric(
            "Evidence chunks",
            result["paper_b_chunks"]
        )

        st.caption(
            f"{result['paper_b_context']:,} "
            "context characters analyzed"
        )


    st.divider()


    # =====================================================
    # COMPARISON REPORT
    # =====================================================

    st.markdown(
        result["comparison"]
    )


    # =====================================================
    # EXPORT
    # =====================================================

    st.divider()

    st.markdown(
        "### Export comparison"
    )


    report = (
        "# ResearchIQ Comparative Research Report\n\n"

        f"## Paper A\n"
        f"{result['paper_a']}\n\n"

        f"## Paper B\n"
        f"{result['paper_b']}\n\n"

        "---\n\n"

        f"{result['comparison']}"
    )


    safe_a = (
        result["paper_a"]
        .replace(".pdf", "")
        .replace(" ", "_")
    )

    safe_b = (
        result["paper_b"]
        .replace(".pdf", "")
        .replace(" ", "_")
    )


    st.download_button(
        label="Download Comparison Report",
        data=report,
        file_name=(
            f"{safe_a}_vs_"
            f"{safe_b}_comparison.md"
        ),
        mime="text/markdown"
    )
