import streamlit as st

st.set_page_config(page_title="chitchat", page_icon="🤖💬📢🤖", layout="centered")
st.header("chitchat")

from openai.error import OpenAIError
import configparser

# import os
from utils import (
    embed_docs,
    get_answer,
    get_sources,
    parse_docx,
    parse_pdf,
    parse_txt,
    search_docs,
    text_to_docs,
    load_query,
    write_list,
)
from tqdm import tqdm
import json
from score import calculate_score
import pandas as pd  # in case we need to output as a table

from components.sidebar import sidebar

sidebar()


config = configparser.ConfigParser()
config.read("config.ini")
# os.environ["OPENAI_API_KEY"] = config.get("API", "openai_api_key")
# candidate_files = json.loads(config.get("files", "candidate_files"))
question_file = json.loads(config.get("files", "question_file"))
answer_file = json.loads(config.get("files", "answer_file"))
score_file = json.loads(config.get("files", "score_file"))
st.session_state["OPENAI_API_KEY"] = config.get("API", "openai_api_key")
st.session_state["api_key_configured"] = True


index = None
docs = []


def clear_submit():
    st.session_state["submit"] = False
    st.cache_data.clear()


candidate_files = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "docx", "txt"],
    help="Scanned documents are not supported yet!",
    on_change=clear_submit,
    accept_multiple_files=True,
)


st.write("Candidate files: ", len(candidate_files))

if len(candidate_files) > 0:
    for file in candidate_files:
        # with open(cand.name, "rb") as file:
        doc = None
        if file is not None:
            if file.name.endswith(".pdf"):
                doc = parse_pdf(file)
            elif file.name.endswith(".docx"):
                doc = parse_docx(file)
            elif file.name.endswith(".txt"):
                doc = parse_txt(file)
            else:
                raise ValueError("File type not supported!")
        docs.append(doc)

    text = text_to_docs(docs)
    try:
        with st.spinner("Indexing document... This may take a while⏳"):
            index = embed_docs(text)
            st.session_state["api_key_configured"] = True
    except OpenAIError as e:
        st.error(e._message)

button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    elif not index:
        st.error("Please upload documents!")
    else:
        st.session_state["submit"] = True

        output = []

        questions = load_query(question_file)
        count = 0

        my_bar = st.progress(0, text="Generating answers...")
        for line in tqdm(questions):
            count += 1
            my_bar.progress(
                count / len(questions),
                text=f"Generating answer for question {count}...",
            )

            query = line["question"]
            sources = search_docs(index, query)

            qa = {}
            qa["section"] = line["section"]
            qa["code"] = line["code"]
            qa["variation"] = line["variation"]
            qa["question"] = query

            try:
                answer = get_answer(sources, query)
            except OpenAIError as e:
                print(e._message)
            sources = get_sources(answer, sources)
            qa["answer"] = answer["output_text"].split("[SOURCES]:")[0].rstrip()
            # here k=7
            top_k_contents = []
            top_k_pages = []
            for source in sources:
                top_k_contents.append(source.page_content)
                top_k_pages.append(source.metadata["source"])
            qa["source_contents"] = top_k_contents
            qa["source_pages"] = top_k_pages
            try:
                qa["score"] = int(
                    answer["output_text"].split("[SCORE]:")[-1].rstrip()
                )
            except ValueError:
                # Sometimes the response from gpt adds a random period after the score
                temp = answer["output_text"].split("[SCORE]:")[-1]
                try:
                    qa["score"] = int(temp.strip("."))
                except ValueError:
                    print(f"Strange scores. [SCORE]: {temp}")
                    qa["score"] = 0

            output.append(qa)

        if st.session_state["submit"]:
            # TODO: need to figure out how we are going to use this output_df
            score_df, company_level_score = calculate_score(answer_file)
            print(company_level_score)
            st.markdown(
                f"Company-level score: **:blue[{company_level_score}]**"
            )

            # display the output as markdown
            current_section = None
            for answer in output:
                if current_section != answer["section"]:
                    current_section = answer["section"]
                    st.markdown(f"## {current_section}")
                if answer["variation"] == "v1":
                    st.markdown(
                        f"**Question: {answer['code']}** {answer['question']}"
                    )
                    st.markdown(f"**Answer:** {answer['answer']}")
                    st.markdown(
                        f"**Source:** {[source for source in answer['source_pages']]}"
                    )

            # display the output as a (messy) table
            # st.table(pd.DataFrame(output))
            # display the output as a list of nested dictionaries (json-like)
            # st.write(output)

        write_list(output, answer_file)
        # print("[DONE] Data written into JSON")

        # write score_df into a csv file
        score_df.to_csv(score_file, index=False)
