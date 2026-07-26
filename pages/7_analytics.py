import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.page_header import page_header

from core.vector_store import VectorStore
from services.analytics_service import AnalyticsService

from utils.helpers import load_css


st.set_page_config(
    page_title="Research Analytics | ResearchIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_css()

render_sidebar()


page_header(
    eyebrow="KNOWLEDGE OBSERVABILITY",

    title="Research",

    highlight="Analytics",

    description=(
        "Explore the structure, distribution and coverage "
        "of your indexed academic knowledge base using "
        "deterministic research analytics."
    )
)


# =========================================================
# YOUR EXISTING ANALYTICS CODE CONTINUES HERE
# =========================================================

# =========================================================
# SERVICES
# =========================================================

@st.cache_resource
def initialize_analytics():

    vector_store = VectorStore()

    analytics = AnalyticsService(
        vector_store
    )

    return analytics, vector_store


try:

    analytics, vector_store = (
        initialize_analytics()
    )

except Exception as exc:

    st.error(
        f"Unable to initialize analytics: {exc}"
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

header_html = (
    '<div class="ri-eyebrow">'
    'KNOWLEDGE OBSERVABILITY'
    '</div>'

    '<div class="ri-title" '
    'style="font-size:3.2rem;">'

    'Research '

    '<span class="ri-gradient">'
    'Analytics'
    '</span>'

    '</div>'

    '<div class="ri-description">'

    'Explore the structure, distribution and coverage '
    'of your indexed academic knowledge base using '
    'deterministic analytics derived directly from '
    'ResearchIQ metadata.'

    '</div>'
)

st.markdown(
    header_html,
    unsafe_allow_html=True
)

st.write("")


# =========================================================
# OVERVIEW
# =========================================================

try:

    overview = (
        analytics.get_overview()
    )

except Exception as exc:

    st.error(
        f"Unable to calculate analytics: {exc}"
    )

    st.stop()


if overview["total_chunks"] == 0:

    st.warning(
        "Your ResearchIQ knowledge base is empty."
    )

    st.info(
        "Upload and index research documents from "
        "Knowledge Library to generate analytics."
    )

    st.stop()


# =========================================================
# KPI CARDS
# =========================================================

st.markdown(
    "## Knowledge Base Overview"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Indexed Papers",
        overview[
            "total_documents"
        ]
    )


with c2:

    st.metric(
        "Knowledge Vectors",
        overview[
            "total_chunks"
        ]
    )


with c3:

    st.metric(
        "Pages Represented",
        overview[
            "unique_pages"
        ]
    )


with c4:

    st.metric(
        "Avg. Chunks / Paper",
        f'{overview["average_chunks"]:.1f}'
    )


st.divider()


# =========================================================
# DOCUMENT STATISTICS
# =========================================================

document_stats = (
    analytics.get_document_statistics()
)

document_df = pd.DataFrame(
    document_stats
)


# =========================================================
# CHUNK DISTRIBUTION
# =========================================================

st.markdown(
    "## Knowledge Distribution"
)

st.caption(
    "Number of semantic chunks stored for each "
    "indexed research document."
)


if not document_df.empty:

    chart_data = (
        document_df[
            [
                "Document",
                "Chunks"
            ]
        ]
        .set_index(
            "Document"
        )
    )

    st.bar_chart(
        chart_data,
        use_container_width=True
    )


st.write("")


# =========================================================
# TWO-COLUMN ANALYTICS
# =========================================================

left, right = st.columns(2)


# ---------------------------------------------------------
# PAGE COVERAGE
# ---------------------------------------------------------

with left:

    st.markdown(
        "### Page Coverage"
    )

    st.caption(
        "Number of unique indexed pages represented "
        "for each research paper."
    )

    if not document_df.empty:

        page_chart = (
            document_df[
                [
                    "Document",
                    "Pages"
                ]
            ]
            .set_index(
                "Document"
            )
        )

        st.bar_chart(
            page_chart,
            use_container_width=True
        )


# ---------------------------------------------------------
# CHARACTER DISTRIBUTION
# ---------------------------------------------------------

with right:

    st.markdown(
        "### Indexed Text Volume"
    )

    st.caption(
        "Total number of text characters represented "
        "in indexed chunks for each document."
    )

    if not document_df.empty:

        character_chart = (
            document_df[
                [
                    "Document",
                    "Characters"
                ]
            ]
            .set_index(
                "Document"
            )
        )

        st.bar_chart(
            character_chart,
            use_container_width=True
        )


st.divider()


# =========================================================
# KNOWLEDGE SHARE
# =========================================================

st.markdown(
    "## Knowledge Base Share"
)

st.caption(
    "Percentage of the vector knowledge base contributed "
    "by each indexed research document."
)


distribution = (
    analytics.get_knowledge_distribution()
)

distribution_df = pd.DataFrame(
    distribution
)


if not distribution_df.empty:

    share_chart = (
        distribution_df[
            [
                "Document",
                "Knowledge Share (%)"
            ]
        ]
        .set_index(
            "Document"
        )
    )

    st.bar_chart(
        share_chart,
        use_container_width=True
    )


st.divider()


# =========================================================
# DOCUMENT TABLE
# =========================================================

st.markdown(
    "## Document Intelligence"
)

st.caption(
    "Deterministic statistics calculated directly "
    "from indexed document chunks."
)


st.dataframe(
    document_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DOCUMENT INSPECTOR
# =========================================================

st.divider()

st.markdown(
    "## Document Inspector"
)


document_names = (
    document_df["Document"]
    .tolist()
)


selected_document = st.selectbox(
    "Select document",
    document_names
)


selected_data = (
    document_df[
        document_df[
            "Document"
        ]
        == selected_document
    ]
)


if not selected_data.empty:

    row = selected_data.iloc[0]


    i1, i2, i3, i4 = (
        st.columns(4)
    )


    i1.metric(
        "Chunks",
        int(
            row["Chunks"]
        )
    )


    i2.metric(
        "Pages",
        int(
            row["Pages"]
        )
    )


    i3.metric(
        "Characters",
        f'{int(row["Characters"]):,}'
    )


    i4.metric(
        "Avg Chunk Length",
        f'{row["Avg Chunk Length"]:.0f}'
    )


# =========================================================
# PAGE-LEVEL DISTRIBUTION
# =========================================================

page_distribution = (
    analytics.get_page_distribution()
)

page_df = pd.DataFrame(
    page_distribution
)


if not page_df.empty:

    selected_pages = (
        page_df[
            page_df[
                "Document"
            ]
            == selected_document
        ]
    )


    if not selected_pages.empty:

        st.markdown(
            "### Chunks by Page"
        )

        page_chart = (
            selected_pages[
                [
                    "Page",
                    "Chunks"
                ]
            ]
            .set_index(
                "Page"
            )
        )

        st.bar_chart(
            page_chart,
            use_container_width=True
        )


st.divider()


# =========================================================
# VECTOR DATABASE HEALTH
# =========================================================

st.markdown(
    "## Knowledge Base Health"
)


health_col1, health_col2 = (
    st.columns(2)
)


with health_col1:

    if (
        overview["total_documents"] > 0
        and overview["total_chunks"] > 0
    ):

        st.success(
            "Vector database contains indexed "
            "research knowledge."
        )

    else:

        st.warning(
            "Knowledge base requires documents."
        )


with health_col2:

    if overview["unique_pages"] > 0:

        st.success(
            "Page-level metadata is available "
            "for citation and evidence tracing."
        )

    else:

        st.warning(
            "No page-level metadata detected."
        )


# =========================================================
# EXPORT
# =========================================================

st.divider()

st.markdown(
    "## Export Analytics"
)


csv_data = (
    document_df.to_csv(
        index=False
    )
)


st.download_button(
    label="Download Knowledge Analytics CSV",
    data=csv_data,
    file_name=(
        "researchiq_knowledge_analytics.csv"
    ),
    mime="text/csv"
)


# =========================================================
# FOOTER NOTE
# =========================================================

st.caption(
    "Analytics shown on this page are calculated "
    "directly from indexed ChromaDB metadata and "
    "document chunks. Gemini is not used to generate "
    "the core statistics."
)
