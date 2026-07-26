import streamlit as st


def source_card(
    source: dict,
    expanded: bool = False
):

    source_id = source.get(
        "source_id",
        "Source"
    )

    filename = source.get(
        "filename",
        "Unknown Document"
    )

    page = source.get(
        "page"
    )

    text = source.get(
        "text",
        ""
    )

    rrf_score = source.get(
        "rrf_score"
    )

    rerank_score = source.get(
        "rerank_score"
    )

    retrieval_sources = source.get(
        "retrieval_sources",
        []
    )


    # =====================================================
    # PAGE
    # =====================================================

    page_text = (
        f"Page {page}"
        if page is not None
        else "Page N/A"
    )


    # =====================================================
    # LABEL
    # =====================================================

    label = (
        f"[{source_id}] "
        f"{filename} · "
        f"{page_text}"
    )


    # =====================================================
    # CARD
    # =====================================================

    with st.expander(
        label,
        expanded=expanded
    ):

        st.caption(
            "Retrieved Research Evidence"
        )

        st.write(
            text
        )


        # =================================================
        # RETRIEVAL INFORMATION
        # =================================================

        if retrieval_sources:

            retrieval_label = ", ".join(
                source_name.upper()
                for source_name
                in retrieval_sources
            )

            st.caption(
                f"Retrieved by: {retrieval_label}"
            )


        # =================================================
        # SCORES
        # =================================================

        score_col1, score_col2 = (
            st.columns(2)
        )


        with score_col1:

            if rrf_score is not None:

                st.metric(
                    "RRF Score",
                    f"{rrf_score:.5f}"
                )


        with score_col2:

            if rerank_score is not None:

                st.metric(
                    "Rerank Score",
                    f"{rerank_score:.4f}"
                )


        if (
            rrf_score is not None
            or rerank_score is not None
        ):

            st.caption(
                "Retrieval and reranking scores are "
                "ranking signals, not confidence "
                "probabilities."
            )