# README

<p align="center">
<img src="https://s3.amazonaws.com/moonup/production/uploads/noauth/b3AVwKK334lyREpZwqPxs.jpeg" width="40%">
</p>

## How to use chitchat?

- Make sure `poetry` is [installed](https://python-poetry.org/docs/) for package and dependency management.
- Use `poetry install` to initialize the virtual environment for the first time.
- Use `poetry shell` to activate the virtual environment.
- Rename `config.ini.template` to `config.init`, and fill in the values.

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
  - Add some value for each 'YES'
  - Minus some value for each 'NO'
  - Such values will depend on the section that a question belongs to
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
