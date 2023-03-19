import streamlit as st


def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key


def sidebar():
    with st.sidebar:
        st.markdown(
            "## Instructions\n"
            "1. Enter a valid [OpenAI API token](https://platform.openai.com/account/api-keys)\n"  # noqa: E501
            "2. Upload a supported file\n"
            "3. Ask any questions\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown(
            "Inspired by [knowledge_gpt](https://github.com/mmz-001/knowledge_gpt)"
        )
