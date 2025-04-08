import streamlit as st

from utils import get_localised_text, icons

# ATTENTION: Singleton, can only be called once
st.set_page_config(layout="wide")

st.session_state.setdefault("language", "English")
st.session_state.setdefault("version", "4Bio")
st.session_state.setdefault("show_video_transcripts", False)

version: str = st.session_state["version"]
language: str = st.session_state["language"]
text = get_localised_text(version, language)


pg = st.navigation(
    [
        st.Page(
            "routes/home.py",
            title=text("SDE_PAGENAMES_START"),
            icon=icons["house"],
        ),
        st.Page(
            "routes/photosynthesis.py",
            title=text("SDE_PAGENAMES_PHOTOSYNTHESIS"),
            icon=icons["leaves"],
        ),
        st.Page(
            "routes/method.py",
            title=text("SDE_PAGENAMES_MEASURINGMETHOD"),
            icon=icons["books"],
        ),
        st.Page(
            "routes/model_explain.py",
            title=text("SDE_PAGENAMES_COMPUTATIONALMODELS"),
            icon=icons["computer"],
        ),
        st.Page(
            "routes/exp_in_silico.py",
            title=text("SDE_PAGENAMES_EXPERIMENTSINSILICO"),
            icon=icons["bar_chart"],
        ),
        st.Page(
            "routes/plant_memory.py",
            title=text("SDE_PAGENAMES_PLANTLIGHTMEMORY"),
            icon=icons["chart_with_upwards_trend"],
        ),
        st.Page(
            "routes/conclusion.py",
            title=text("SDE_PAGENAMES_CONCLUSION"),
            icon=icons["heavy_check_mark"],
        ),
        st.Page(
            "routes/contact.py",
            title=text("SDE_PAGENAMES_CONTACT"),
            icon=icons["phone"],
        ),
    ]
)

with st.sidebar:
    st.sidebar.write(f"## {text('SDE_SIDEBAR_SETTINGS')} :gear:")

    # Version selector
    versions = {"4Bio": text("SDE_4BIO"), "4Math": text("SDE_4MATH")}
    version_idx = dict(zip(versions, range(len(versions))))
    st.selectbox(
        label=f"⚙ {text('SDE_SIDEBAR_VERSION')} 👩‍🎓👩🏼‍🔬",
        index=version_idx[version],
        options=versions,
        format_func=versions.get,
        key="_version",
        on_change=lambda: st.session_state.update({"version": st.session_state["_version"]}),
    )

    # Language selector
    languages = {
        "English": "🇬🇧  " + text("SDE_LANGUAGE_EN"),
        "German": "🇩🇪  " + text("SDE_LANGUAGE_DE"),
        # "Polish": "🇵🇱  " + text("SDE_LANGUAGE_PL"),
        "French": "🇫🇷  " + text("SDE_LANGUAGE_FR"),
    }
    language_idx = dict(zip(languages, range(len(languages))))
    st.selectbox(
        label=f"⚙ {text('SDE_SIDEBAR_LANGUAGE')} 🌍💬",
        index=language_idx[language],
        options=languages,
        key="_language",
        on_change=lambda: st.session_state.update({"language": st.session_state["_language"]}),
    )

    # Video selector
    st.sidebar.checkbox(
        label=text("VIDEO_TRANSCRIPT_SWITCH"),
        value=False,
        args=("show_video_transcripts",),
        key="_show_video_transcripts",
        on_change=lambda: st.session_state.update(
            {"show_video_transcripts": st.session_state["_show_video_transcripts"]}
        ),
    )


pg.run()
