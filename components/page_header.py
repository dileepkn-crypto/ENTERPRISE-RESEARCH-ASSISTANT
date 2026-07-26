import streamlit as st
from html import escape


def page_header(
    eyebrow: str,
    title: str,
    highlight: str = "",
    description: str = ""
):
    """
    Standard ResearchIQ page header.

    Provides:
    - Consistent top positioning
    - Left alignment
    - Gradient title highlight
    - Consistent description width
    - Responsive layout
    """

    safe_eyebrow = escape(eyebrow)
    safe_title = escape(title)
    safe_highlight = escape(highlight)
    safe_description = escape(description)

    if safe_highlight:
        title_content = f"""
            {safe_title}
            <span class="ri-page-highlight">
                {safe_highlight}
            </span>
        """
    else:
        title_content = safe_title

    st.html(
        f"""
        <div class="ri-page-header">

            <div class="ri-page-eyebrow">
                {safe_eyebrow}
            </div>

            <h1 class="ri-page-title">
                {title_content}
            </h1>

            <p class="ri-page-description">
                {safe_description}
            </p>

        </div>
        """
    )
