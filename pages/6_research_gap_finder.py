import streamlit as st

from components.sidebar import render_sidebar
from components.page_header import page_header

from core.vector_store import VectorStore
from services.gap_finder_service import GapFinderService
from services.llm_service import LLMService

from utils.helpers import load_css


st.set_page_config(
    page_title="Research Gap Finder | ResearchIQ",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_css()

render_sidebar()


page_header(
    eyebrow="RESEARCH DISCOVERY",

    title="Research Gap",

    highlight="Finder",

    description=(
        "Analyze evidence across academic literature to "
        "discover recurring limitations, underexplored "
        "directions and candidate research opportunities."
    )
)


# =========================================================
# YOUR EXISTING RESEARCH GAP FINDER CODE CONTINUES HERE
# =========================================================


# =========================================================
# SERVICES
# =========================================================

@st.cache_resource
def initialize_gap_finder():

    vector_store = VectorStore()

    llm_service = LLMService()

    gap_finder = GapFinderService(
        vector_store,
        llm_service
    )

    return (
        gap_finder,
        vector_store
    )


try:

    gap_finder, vector_store = (
        initialize_gap_finder()
    )

except Exception as exc:

    st.error(
        f"Unable to initialize Research Gap Finder: {exc}"
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

header_html = (
    '<div class="ri-eyebrow">'
    'RESEARCH DISCOVERY'
    '</div>'

    '<div class="ri-title" '
    'style="font-size:3.2rem;">'

    'Research Gap '

    '<span class="ri-gradient">'
    'Finder'
    '</span>'

    '</div>'

    '<div class="ri-description">'

    'Analyze evidence across multiple academic papers '
    'to discover stated limitations, cross-paper patterns '
    'and candidate directions for future research.'

    '</div>'
)

st.markdown(
    header_html,
    unsafe_allow_html=True
)


st.write("")


# =========================================================
# KNOWLEDGE BASE STATUS
# =========================================================

documents = (
    gap_finder.get_documents()
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
            "Gap intelligence ready"
        )

    else:

        st.warning(
            "At least 2 papers required"
        )


st.divider()


# =========================================================
# VALIDATION
# =========================================================

if len(documents) < 2:

    st.warning(
        "Research Gap Finder requires at least "
        "two indexed research papers."
    )

    st.info(
        "Upload additional research papers from "
        "Knowledge Library and return here."
    )

    st.stop()


# =========================================================
# PAPER SELECTION
# =========================================================

st.markdown(
    "## Select research corpus"
)

st.caption(
    "Choose the papers ResearchIQ should analyze "
    "together. More relevant papers generally provide "
    "a stronger basis for cross-paper analysis."
)


selected_documents = st.multiselect(
    "Research papers",
    options=documents,
    default=documents[:min(
        len(documents),
        3
    )]
)


# =========================================================
# SELECTION INFORMATION
# =========================================================

if selected_documents:

    st.caption(
        f"{len(selected_documents)} "
        "papers selected"
    )


if len(selected_documents) < 2:

    st.warning(
        "Select at least two different papers."
    )


st.write("")


analyze_button = st.button(
    "Discover Research Opportunities",
    type="primary",
    disabled=(
        len(selected_documents) < 2
    )
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    with st.status(
        "Analyzing research landscape...",
        expanded=True
    ) as status:

        try:

            st.write(
                "Collecting indexed evidence..."
            )

            st.write(
                "Analyzing stated limitations..."
            )

            st.write(
                "Identifying cross-paper patterns..."
            )

            st.write(
                "Evaluating methodological and "
                "technical opportunities..."
            )

            st.write(
                "Synthesizing candidate research "
                "directions..."
            )

            result = (
                gap_finder.analyze(
                    selected_documents
                )
            )

            status.update(
                label=(
                    "Research gap intelligence complete"
                ),
                state="complete",
                expanded=False
            )

        except Exception as exc:

            status.update(
                label="Analysis failed",
                state="error"
            )

            st.error(
                f"Research gap analysis failed: {exc}"
            )

            st.stop()


    # =====================================================
    # REPORT
    # =====================================================

    st.write("")

    st.markdown(
        "## Research Gap Intelligence Report"
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Papers analyzed",
            result["document_count"]
        )


    with c2:

        total_chunks = sum(
            item["chunks"]
            for item
            in result["document_stats"]
        )

        st.metric(
            "Evidence chunks",
            total_chunks
        )


    with c3:

        st.metric(
            "Evidence context",
            f'{result["context_characters"]:,}'
        )


    # =====================================================
    # DOCUMENT EVIDENCE
    # =====================================================

    with st.expander(
        "Research corpus details"
    ):

        for item in result[
            "document_stats"
        ]:

            st.markdown(
                f"**{item['filename']}**"
            )

            st.caption(
                f"{item['chunks']} chunks · "
                f"{item['context_characters']:,} "
                "context characters"
            )


    st.divider()


    # =====================================================
    # AI REPORT
    # =====================================================

    st.markdown(
        result["analysis"]
    )


    # =====================================================
    # ACADEMIC WARNING
    # =====================================================

    st.divider()

    st.warning(
        "Candidate opportunities generated by ResearchIQ "
        "are hypotheses derived from the selected indexed "
        "papers. They should not be presented as confirmed "
        "research gaps without validation through a broader "
        "systematic literature review."
    )


    # =====================================================
    # EXPORT
    # =====================================================

    st.markdown(
        "### Export research intelligence"
    )


    document_list = "\n".join(
        f"- {document}"
        for document
        in result["documents"]
    )


    report = (
        "# ResearchIQ Research Gap Intelligence\n\n"

        "## Research Corpus\n\n"

        f"{document_list}\n\n"

        "---\n\n"

        f"{result['analysis']}\n\n"

        "---\n\n"

        "## Validation Notice\n\n"

        "Candidate research opportunities in this report "
        "are AI-synthesized hypotheses derived from the "
        "selected documents. A broader literature review "
        "is required before claiming a confirmed research "
        "gap."
    )


    st.download_button(
        label="Download Gap Intelligence Report",
        data=report,
        file_name=(
            "researchiq_gap_intelligence.md"
        ),
        mime="text/markdown"
    )
