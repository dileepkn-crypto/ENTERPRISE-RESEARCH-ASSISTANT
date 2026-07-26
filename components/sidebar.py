import streamlit as st


def render_sidebar():
    """
    Global ResearchIQ navigation sidebar.
    Used across all Streamlit pages.
    """

    with st.sidebar:

        # =====================================================
        # BRAND
        # =====================================================

        st.markdown(
            (
                '<div class="brand">'
                '<div class="brand-icon">R</div>'
                '<div>'
                '<div class="brand-name">ResearchIQ</div>'
                '<div class="brand-subtitle">'
                'Knowledge Intelligence'
                '</div>'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sidebar-divider"></div>',
            unsafe_allow_html=True
        )

        # =====================================================
        # WORKSPACE
        # =====================================================

        st.markdown(
            '<div class="sidebar-section-title">'
            'WORKSPACE'
            '</div>',
            unsafe_allow_html=True
        )

        st.page_link(
            "app.py",
            label="Dashboard",
            icon=":material/dashboard:"
        )

        st.page_link(
            "pages/1_research_copilot.py",
            label="Research Copilot",
            icon=":material/auto_awesome:"
        )

        st.page_link(
            "pages/2_knowledge_library.py",
            label="Knowledge Library",
            icon=":material/library_books:"
        )

        st.page_link(
            "pages/3_semantic_search.py",
            label="Semantic Search",
            icon=":material/search:"
        )

        # =====================================================
        # RESEARCH INTELLIGENCE
        # =====================================================

        st.markdown(
            '<div class="sidebar-section-title">'
            'RESEARCH INTELLIGENCE'
            '</div>',
            unsafe_allow_html=True
        )

        st.page_link(
            "pages/4_paper_analyzer.py",
            label="Paper Analyzer",
            icon=":material/description:"
        )

        st.page_link(
            "pages/5_compare_papers.py",
            label="Compare Papers",
            icon=":material/compare_arrows:"
        )

        st.page_link(
            "pages/6_research_gap_finder.py",
            label="Research Gap Finder",
            icon=":material/lightbulb:"
        )

        st.page_link(
            "pages/7_analytics.py",
            label="Analytics",
            icon=":material/analytics:"
        )

        # =====================================================
        # SYSTEM STATUS
        # =====================================================

        st.markdown(
            '<div class="sidebar-divider"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sidebar-section-title">'
            'AI ENGINE'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            (
                '<div class="engine-status">'
                '<div class="status-row">'
                '<span class="status-dot"></span>'
                '<span class="status-title">'
                'RAG Engine Online'
                '</span>'
                '</div>'
                '<div class="status-description">'
                'Semantic retrieval + grounded generation '
                '+ page-level citations'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            (
                '<div class="sidebar-footer">'
                '<span>Built by Dileep K N</span>'
                '<span>v1.0</span>'
                '</div>'
            ),
            unsafe_allow_html=True
        )
