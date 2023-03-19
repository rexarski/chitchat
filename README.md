# README

> GPT Index is focused on loading and querying over documents/datasets
> Langchain is more general purpose and has a whole bunch of different things it helps with

## Todos
- [x] structure the app
  - [x] `app.py`
  - [x] `requirements.txt`
  - [x] `setup.py`
  - [x] `README.md`
  - [x] `data` directory
  - [x] `tests` directory
- [x] LlamaIndex
  - [x] https://gpt-index.readthedocs.io/en/latest/
  - [x] https://github.com/jerryjliu/gpt_index
- [ ] streamlit
- [x] ~~Update `requirements.txt` with `pipreqs . --force`~~
- [x] Add `gpt-3.5-turbo-0301` support


## How to use?

```bash
poetry install
poetry shell
```

- Rename `config.ini.template` to `config.init`, and fill in the values.

### Streamlit app

```bash
cd chitchat
streamlit run main.py
```

### CLI

- Specify the directory of "context files".
- Input the question following the prompt, or use `:q` or enter to exit.

```bash
python cli-app.py
```

## Resources

- [a lot of different document loaders that LangChain supports](https://langchain.readthedocs.io/en/latest/modules/document_loaders/how_to_guides.html)
- [Question Answering - LangChain](https://langchain.readthedocs.io/en/latest/modules/indexes/chain_examples/question_answering.html)
- https://github.com/mmz-001/knowledge_gpt