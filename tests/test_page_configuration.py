from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_each_streamlit_page_configures_itself_once():
    """Streamlit permits only one page configuration call per script."""
    scripts = [
        PROJECT_ROOT / "app.py",
        *sorted((PROJECT_ROOT / "pages").glob("*.py")),
    ]

    duplicate_configs = [
        script.name
        for script in scripts
        if script.read_text(encoding="utf-8").count(
            "st.set_page_config("
        )
        != 1
    ]

    assert not duplicate_configs, (
        "Every Streamlit script must call st.set_page_config() exactly "
        f"once; invalid scripts: {', '.join(duplicate_configs)}"
    )
