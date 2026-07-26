from pathlib import Path

import streamlit as st


def load_css():
    """
    Load the global ResearchIQ stylesheet.
    """

    project_root = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    css_path = (
        project_root
        / "assets"
        / "styles.css"
    )

    if not css_path.exists():

        st.warning(
            f"ResearchIQ stylesheet not found: "
            f"{css_path}"
        )

        return

    css_content = css_path.read_text(
        encoding="utf-8"
    )

    st.markdown(
        f"""
        <style>
        {css_content}
        </style>
        """,
        unsafe_allow_html=True
    )