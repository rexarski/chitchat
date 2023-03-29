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
    load_query,
    write_list,
)
from tqdm import tqdm
import json
from score import calculate_score

config = configparser.ConfigParser()


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

    questions = load_query(question_file)
    for line in tqdm(questions):
        query = line["question"]
        sources = search_docs(index, query)

        qa = {}
        qa["section"] = line["section"]
        qa["code"] = line["code"]
        qa["variation"] = line["variation"]
        qa["question"] = query

        try:
            answer = get_answer(sources, query, line["question_type"])
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
            qa["score"] = int(answer["output_text"].split("[SCORE]:")[-1].rstrip())
        except ValueError:
            # Sometimes the response from gpt adds a random period after the score
            temp = answer["output_text"].split("[SCORE]:")[-1]
            try:
                qa["score"] = int(temp.strip("."))
            except ValueError:
                print(f"Strange scores. [SCORE]: {temp}")
                qa["score"] = 0
        # qa["score"] = answer["output_text"].split("[SCORE]:")[-1]

        output.append(qa)

    write_list(output, answer_file)
    print("[DONE] Data written into JSON")

    # TODO: need to figure out how we are going to use this output_df
    score_df, company_level_score = calculate_score(answer_file)
    print(f"The company level score is {company_level_score}")

    # write score_df into a csv file
    score_df.to_csv(score_file, index=False)


if __name__ == "__main__":
    config.read("config.ini")
    os.environ["OPENAI_API_KEY"] = config.get("API", "openai_api_key")
    candidate_files = json.loads(config.get("files", "candidate_files"))
    question_file = json.loads(config.get("files", "question_file"))
    answer_file = json.loads(config.get("files", "answer_file"))
    score_file = json.loads(config.get("files", "score_file"))
    main()
