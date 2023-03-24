# README

## How to use chitchat?

- `poetry install` to initialize the virtual environment for the first time.
- `poetry shell` to activate the virtual environment.
- Rename `config.ini.template` to `config.init`, and fill in the values.

### Streamlit app

An interactive web app.

```bash
cd chitchat
streamlit run main.py
```

### CLI

A command line interface for a set of predefined questions.

```bash
python chitchat-cli/cli-app.py
```

- Specify the document path in `main.py`.
- Modify `query.txt` if needed for additional questions.

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
