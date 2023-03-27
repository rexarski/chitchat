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
import json

config = configparser.ConfigParser()
config.read("config.ini")
os.environ["OPENAI_API_KEY"] = config.get("API", "openai_api_key")
# candidate_files = ["data/ifc.txt", "data/walled-garden-part.pdf"]
candidate_files = ["data/Equity-Sustainability-Report-2021.pdf"]


def main():
    """Process a list of submitted files."""

    index = None
    docs = []

    for cand in candidate_files:
        with open(cand, "rb") as file:
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
        print("Indexing document...")
        index = embed_docs(text)
    except OpenAIError as e:
        print(e._message)

    output = []

    # TODO: parallelize this

    questions = load_query("chitchat-cli/questions.csv")
    for line in tqdm(questions):
        query = line["question"]
        sources = search_docs(index, query)

        qa = {}
        qa["section"] = line["section"]
        qa["code"] = line["code"]
        qa["variation"] = line["variation"]
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

        # TODO: placeholder for scoring mechanism

        output.append(qa)

    write_list(output)
    print("Done writing JSON data into .json file")


def load_query(query_file):
    dict_list = []
    with open(query_file, "r") as file:
        for line in file:
            values = line.strip().split(",")
            my_dict = {
                "section": values[0],
                "code": values[1],
                "variation": values[2],
                "question": values[3].strip().strip('"'),
            }
            dict_list.append(my_dict)
    return dict_list


def write_list(a_list):
    with open("output.json", "w") as file:
        json.dump(a_list, file)


if __name__ == "__main__":
    main()
