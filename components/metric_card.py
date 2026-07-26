import html

import streamlit as st


def metric_card(
    title: str,
    value,
    subtitle: str = ""
):

    safe_title = html.escape(
        str(title)
    )

    safe_value = html.escape(
        str(value)
    )

    safe_subtitle = html.escape(
        str(subtitle)
    )

    card_html = (
        '<div class="metric-card">'
        f'<div class="metric-label">'
        f'{safe_title}'
        '</div>'
        f'<div class="metric-value">'
        f'{safe_value}'
        '</div>'
        f'<div class="metric-subtitle">'
        f'{safe_subtitle}'
        '</div>'
        '</div>'
    )

    st.markdown(
        card_html,
        unsafe_allow_html=True
    )