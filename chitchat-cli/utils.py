import re
import os
from io import BytesIO
from typing import Any, Dict, List

import docx2txt

from embeddings import OpenAIEmbeddings
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import VectorStore
from langchain.vectorstores.faiss import FAISS
from openai.error import AuthenticationError
from prompts import STUFF_PROMPT_INT, STUFF_PROMPT_WH
from pypdf import PdfReader
import pandas as pd
import json


def parse_docx(file: BytesIO) -> str:
    text = docx2txt.process(file)
    # Remove multiple newlines
    text = re.sub(r"\n\s*\n", "\n\n", text)
    return {"text": text, "file": file.name}


def parse_pdf(file: BytesIO) -> List[str]:
    pdf = PdfReader(file)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        # Merge hyphenated words
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        # Fix newlines in the middle of sentences
        text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
        # Remove multiple newlines
        text = re.sub(r"\n\s*\n", "\n\n", text)

        output.append({"text": text, "file": file.name})

    return output


def parse_txt(file: BytesIO) -> str:
    text = file.read().decode("utf-8")
    # Remove multiple newlines
    text = re.sub(r"\n\s*\n", "\n\n", text)

    return {"text": text, "file": file.name}


def text_to_docs(cands: List[dict]) -> List[Document]:
    """Converts a list of dictionaries to a list of Documents
    with metadata."""
    page_docs = []
    for cand in cands:
        if isinstance(cand, dict):
            # Take a single string as one page
            cand = [cand]
        for page in cand:
            page_docs.append(
                Document(page_content=page["text"], metadata={"file": page["file"]})
            )

        # Add page numbers as metadata
        for i, doc in enumerate(page_docs):
            doc.metadata["page"] = i + 1
    # page_docs = [Document(page_content=page) for page in text]

    # Split pages into chunks
    doc_chunks = []

    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=0,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "file": os.path.basename(doc.metadata["file"]),
                    "page": doc.metadata["page"],
                    "chunk": i,
                },
            )
            # Add sources as metadata
            doc.metadata[
                "source"
            ] = f"{doc.metadata['file']}-{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc_chunks.append(doc)

    return doc_chunks


def embed_docs(_docs: List[Document]) -> VectorStore:
    """Embeds a list of Documents and returns a FAISS index"""

    # Embed the chunks
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    index = FAISS.from_documents(_docs, embeddings)

    return index


def search_docs(_index: VectorStore, query: str) -> List[Document]:
    """Searches a FAISS index for similar chunks to the query
    and returns a list of Documents."""

    # Search for similar chunks
    docs = _index.similarity_search(query, k=7)
    return docs


def get_answer(docs: List[Document], query: str, question_type: str) -> Dict[str, Any]:
    """Gets an answer to a question from a list of Documents."""

    # Get the answer

    if question_type == "interrogative":
        prompt_used = STUFF_PROMPT_INT
    elif question_type == "wh":
        prompt_used = STUFF_PROMPT_WH

    chain = load_qa_with_sources_chain(
        OpenAI(
            temperature=0,  # for fixed, predictable results
            openai_api_key=os.environ["OPENAI_API_KEY"],
            model_name="gpt-3.5-turbo",
        ),  # type: ignore
        chain_type="stuff",
        prompt=prompt_used,
    )

    # Cohere doesn't work very well as of now.
    # chain = load_qa_with_sources_chain(
    #     Cohere(temperature=0), chain_type="stuff", prompt=STUFF_PROMPT  # type: ignore
    # )
    answer = chain(
        {"input_documents": docs, "question": query}, return_only_outputs=True
    )
    return answer


def get_sources(answer: Dict[str, Any], _docs: List[Document]) -> List[Document]:
    """Gets the source documents for an answer."""

    # Get sources for the answer
    source_keys = [s for s in answer["output_text"].split("[SOURCES]:")[-1].split(", ")]

    source_docs = []
    for doc in _docs:
        if doc.metadata["source"] in source_keys:
            source_docs.append(doc)

    return source_docs


# The following function is giving us a typo:

# def load_query(query_file):
#     dict_list = []
#     with open(query_file, "r") as file:
#         for line in file:
#             values = line.strip().split(",")
#             my_dict = {
#                 "section": values[0],
#                 "code": values[1],
#                 "variation": values[2],
#                 "question": values[3].strip().strip('"'),
#             }
#             dict_list.append(my_dict)
#     return dict_list


def load_query(query_file):
    df = pd.read_csv(query_file, header=None)
    df.columns = ["section", "code", "variation", "question_type", "question"]
    return df.to_dict("records")


def write_list(a_list, filepath):
    with open(filepath, "w") as file:
        json.dump(a_list, file)
