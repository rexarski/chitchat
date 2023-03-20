from openai.error import OpenAIError
import configparser
import os
from utils import (
    embed_docs,
    get_answer,
    get_sources,
    parse_docx,
    parse_pdf,
    parse_txt,
    search_docs,
    text_to_docs,
)
from tqdm import tqdm


def main(uploaded_file=None):
    index = None
    doc = None
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            doc = parse_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            doc = parse_docx(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            doc = parse_txt(uploaded_file)
        else:
            raise ValueError("File type not supported!")
        text = text_to_docs(doc)
        try:
            print("Indexing document...")
            index = embed_docs(text)
        except OpenAIError as e:
            print(e._message)

    output = []
    queries = load_query("chitchat-cli/query.txt")
    for query in tqdm(queries):
        sources = search_docs(index, query)

        qa = {}
        qa["question"] = query

        try:
            answer = get_answer(sources, query)
            sources = get_sources(answer, sources)
            qa["answer"] = answer["output_text"].split("SOURCES: ")[0]
            top_k_contents = []
            top_k_pages = []
            for source in sources:
                top_k_contents.append(source.page_content)
                top_k_pages.append(source.metadata["source"])
            qa["source_contents"] = top_k_contents
            qa["source_pages"] = top_k_pages
        except OpenAIError as e:
            print(e._message)

        output.append(qa)
    print(output)


def load_query(query_file):
    with open(query_file, "r") as file:
        # Read all lines into a list
        lines = file.readlines()
        # Remove newline characters from each line
        lines = [line.strip() for line in lines]
        # Convert the list into a tuple
        lines_tuple = tuple(lines)
    return lines_tuple


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    os.environ["OPENAI_API_KEY"] = config.get("API", "openai_api_key")
    candidate_file = "data/Equity-Sustainability-Report-2021.pdf"

    with open(candidate_file, "rb") as uploaded_file:
        main(uploaded_file)
