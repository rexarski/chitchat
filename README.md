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

## Resources

- [Different document loaders that LangChain supports](https://langchain.readthedocs.io/en/latest/modules/document_loaders/how_to_guides.html)
- [Question Answering - LangChain](https://langchain.readthedocs.io/en/latest/modules/indexes/chain_examples/question_answering.html)
- [mmz-001/knowledge_gpt](https://github.com/mmz-001/knowledge_gpt)
