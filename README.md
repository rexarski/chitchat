# chitchat

<p align="center">
<img src="logo.jpg" width="40%">
</p>

**chitchat is a context-based question answering tool powered by GPT3.5. Ideal for working with document collections, chitchat delivers accurate and efficient answers to your questions.**

## Setup

- Make sure `poetry` is [installed](https://python-poetry.org/docs/) for package and dependency management.
- Use `poetry install` to initialize the virtual environment for the first time.
- Use `poetry shell` to activate the virtual environment.
- Rename `config-template.ini` to `config.ini`, and fill in the values.

For example:

```ini
[API]
openai_api_key = sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
model_engine = gpt-3.5-turbo

[files]
candidate_files = [
    "data/Equity-Sustainability-Report-2021.pdf",
    "data/Equity-Sustainability-Report-2020.pdf",
    ]
question_file = "chitchat-cli/data/questions.csv"
answer_file = "answer.json"
score_file = "score.csv"
```

## CLI (WIP)

A command line interface for a set of predefined questions.

```bash
# In root directory of this repo:
python chitchat-cli/main.py
```

- Specify the document path (`candidate_files`, `question_file`, `answer_file` and `score_file`) in `config.ini`.
- Modify `chitchat-cli/data/questions.csv` if needed for additional questions.

## Streamlit app

An interactive web app.

```bash
cd chitchat
streamlit run main.py
```

## Roadmap

- [x] Add variation to the `questions.csv`
  - ~~For each question (code), select the answer-variation pair that has higher confidence (?)~~
- [x] Use rule-based approach to score each answer:
  - Add 2 points for straight `YES`
    - If variations (alternatives) of the questions lead to `YES`, then add 1 point as a bonus
    - [ ] The criterion for bonus point is not clear yet
    - If a question has no variations, then give this bonus point for free
  - [ ] What is the criterion for "partially observed" answer? (the case where we add 1 point)
  - Zero point for each `NO`
  - Zero point for `UNKNOWN`
  - The final score of each company is the ratio of the [total points] to the [total number of questions times 3] normalized to [0, 1]
    - Leadership `[.75, 1]`
    - Good `[.65, .75)`
    - Fair `[.50, .65)`
    - Needs improvement `[0, .50)`
  - [x] Generate company-level score based on answers to multiple documents
- [ ] Better filepath handling
- [ ] Better pdf parsing
- [ ] Prompt output parsing with [langchain](https://python.langchain.com/en/latest/modules/prompts/output_parsers/getting_started.html)

- Optional
  - [ ] Confidence of the output. Probably a deadend though (?)
  - [ ] Factcheck the output with human assessment (?)

## Resources

- [LangChain](https://github.com/hwchase17/langchain)
  - [Document Loaders](https://python.langchain.com/en/latest/modules/indexes/document_loaders.html)
  - [Question Answering over Docs](https://python.langchain.com/en/latest/use_cases/question_answering.html)
  - [Question Answering with Sources](https://python.langchain.com/en/latest/modules/chains/index_examples/qa_with_sources.html)
  - [Prompt Templates](https://python.langchain.com/en/latest/modules/prompts/prompt_templates.html)
- [mmz-001/knowledge_gpt](https://github.com/mmz-001/knowledge_gpt)
