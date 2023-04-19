import streamlit as st

from components.faq import faq


# def set_openai_api_key(api_key: str):
#     st.session_state["OPENAI_API_KEY"] = api_key
#     st.session_state["api_key_configured"] = True


def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Make sure your [OpenAI API key](https://platform.openai.com/account/api-keys) has been correctly stored in your `config.ini`\n"
            "2. Upload pdf, docx, or txt file(s)\n"
            "3. Submit the files and wait for generated answers to predefined questions\n"
        )
        # api_key_input = st.text_input(
        #     "OpenAI API Key",
        #     type="password",
        #     placeholder="Paste your OpenAI API key here (sk-...)",
        #     help="You can get your API key from https://platform.openai.com/account/api-keys.",
        #     value=st.session_state.get("OPENAI_API_KEY", ""),
        # )

        # if api_key_input:
        #     set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "**chitchat** is a context-based question answering tool powered by GPT3.5."
            "Ideal for working with document collections, chitchat delivers answers to"
            "your predefined questions."
        )
        st.markdown(
            "This tool is a work in progress. "
            "Source: [GitHub](https://github.com/rexarski/chitchat)"
        )
