# README

<p align="center">
<img src="https://s3.amazonaws.com/moonup/production/uploads/noauth/b3AVwKK334lyREpZwqPxs.jpeg" width="40%">
</p>

## How to use chitchat?

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
```

### CLI (WIP)

A command line interface for a set of predefined questions.

```bash
# In root directory of this repo:
python chitchat-cli/cli-app.py
```

- Specify the document path (`candidate_files`, `question_file`)in `main.py`.
- Modify `chitchat-cli/questions.csv` if needed for additional questions.

### Streamlit app

An interactive web app.

```bash
cd chitchat
streamlit run main.py
```

## Roadmap

- [x] Add variation to the `questions.csv`
  - ~~For each question (code), select the answer-variation pair that has higher confidence (?)~~
- [ ] Use rule-based approach to score each answer:
  - Add 2 points for straight `YES`
    - If variations (alternatives) of the questions lead to `YES`, then add 1 point as a bonus
    - [ ] The criterion for bonus point is not clear yet
    - If a question has no variations, then give this bonus point for free
  - [ ] What is the criterion for "partially observed" answer? (the case where we add 1 point)
  - Zero point for each `NO`
  - Zero point for `UNKNOWN`
  - The final score of each company is the ratio of the [total points] to the [total number of questions times 3] normalized to [0, 1]
    - Leadership rating (75% and above)
    - Good rating (65% to 74%)
    - Fair rating (50% to 64%)
    - Needs improvement rating (below 50%)
  - Generate company-level score based on answers to multiple documents
  - Portfolio-level view will display the scores of all those companies
- [ ] Better filepath handling
- [ ] Better pdf parsing

- Optional
  - [ ] Confidence of the output. Probably a deadend though (?)
  - [ ] Factcheck the output with human assessment (?)

## Resources

- [Different document loaders that LangChain supports](https://langchain.readthedocs.io/en/latest/modules/document_loaders/how_to_guides.html)
- [Question Answering - LangChain](https://langchain.readthedocs.io/en/latest/modules/indexes/chain_examples/question_answering.html)
- [mmz-001/knowledge_gpt](https://github.com/mmz-001/knowledge_gpt)
