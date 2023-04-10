# chitchat 🤖💬📢🤖

<p align="center">
<img src="logo.jpg" width="40%">
</p>

![badge](https://img.shields.io/badge/version-0.1.1-blue)

**chitchat is a context-based question answering tool powered by GPT3.5. Ideal for working with document collections, chitchat delivers accurate and efficient answers to your questions.**

## Setup

- Make sure `poetry` is [installed](https://python-poetry.org/docs/) for package and dependency management.
- Use `poetry install` to initialize the virtual environment for the first time.
- Use `poetry shell` to activate the virtual environment.
- Rename `config-template.ini` to `config.ini`, and fill in the values. For example:

```ini
[API]
openai_api_key = sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
model_engine = gpt-3.5-turbo

[files]
candidate_files = [
    "data/ke-kcb-2021-ar-00.pdf",
    "data/supporting-pdf.pdf",
    "data/supporting-txt.txt",
    "data/supporting-docx.docx",
    ]
question_file = "chitchat-cli/data/questions.csv"
answer_file = "example/answer.json"
score_file = "example/score.csv"
```

> We are using the [integrated report](https://drive.google.com/file/d/1_HDUkfimhW8XdqLtLQTl9la2hV10KMhP/view) of Kenya Commercial Bank (2021) as the input document.

- Another headsup: in `utils.py` we have control over two parameters: `chunk_size` and `chunk_overlap`. The former controls the length of the text chunks, by default, it is using `length_function=len`, which refers to the character number. The latter controls the overlap between two adjacent chunks.

> Sometimes when `chunk_overlap` is set to be small, the answer could be generated without any specific "sources" as no similar such chunks are detected. But bear in mind that, the reason why we don't see any relevant chunks could be complicated as the file parsing is not perfect sometimes. Table of contents, footnotes, tables, captions, or even paragraphs split into two columns, two pages, will mess up the parsed text.

## Demo

A callable script from cli.

```bash
# In root directory of this repo:
python chitchat-cli/main.py
```

- Specify the document path (`candidate_files`, `question_file`, `answer_file` and `score_file`) in `config.ini`.
- Modify `chitchat-cli/data/questions.csv` if needed for additional questions.

### Answer evaluation

#### Definition

- *Interrogative questions* with `YES` or `NO` answers, e.g.,
  - "Does the company have a sustainability strategy?"
  - "Is there any evidence of the company's commitment to sustainability?"
  - "Has the company set any sustainability targets?"
- *WH-questions* with open-ended answers, e.g.,
  - "How does the company ensure that its sustainability strategy is aligned with its business strategy?"
  - "What are the company's sustainability targets?"

#### Scoring

- For interrogative questions, the answer should start with either `YES` or `NO`.
  - The *base score* is 2 for `YES` and 0 for `NO`.
- For WH-questions, we ask the model to provide a evaluation (base) score as a reference. **[blackbox]**
  - 0 for `UNKNOWN`.
  - 1 for partially answered question.
  - 2 for fully answered question.
  - 3 for answers beyond the scope of the question.
- Since some extra variations of the questions are added in to the predefined question file, we need to tweak a little bit to give bonus point to the *base score*.
  - If a variation of the question is provided, the *theoretical maximum score* is 3.
  - If a variation of the question is missing, the *theoretical maximum score* is 3 for WH-questions, and 2 for interrogative questions.
  - If the answer to a variation question (`v2`) gains a score greater than or equal to 2, we add 1 bonus point to the *base score*.
  - Under any circumstances, the sum of *base score* + bonus point cannot exceed its *theoretical maximum score*.
- We calculate the ratio of the sum of *base score* and bonus point to the *theoretical maximum score* for each question, and take the arithmetic mean of the ratios as the final score of the company.

Let's look at one example:

```
  code                                             answer  score_v1  score_v2  score  ideal  score_ideal_ratio
0  A.1                                                 NO         0       NaN      0      2           0.000000
1  A.2                                               YES.         2       NaN      2      2           1.000000
2  A.3                                               YES.         2       2.0      3      3           1.000000
3  A.4  The Board ensures all directors, CEOs, and man...         2       NaN      2      2           1.000000
4  A.5                                               YES.         2       0.0      2      3           0.666667
5  A.6  YES, the company strategy promotes sustainabil...         2       2.0      3      3           1.000000
6  A.7                                               YES.         2       2.0      3      3           1.000000
```

The arithmetic mean of `score_ideal_ratio` is the final score of the company, which is 0.81 in this case.

- The final score of each company is the ratio of the [total points] to the [total number of questions times 3] normalized to [0, 1]
  - Leadership `[.75, 1]`
  - Good `[.65, .75)`
  - Fair `[.50, .65)`
  - Needs improvement `[0, .50)`

## Roadmap

- [x] Add variation to the `questions.csv`
- [x] Use rule-based approach to score each answer
- [ ] Other LLM candidates
  - ~~dolly-v1-6b. [*Hello Dolly: Democratizing the magic of ChatGPT with open models*](https://www.databricks.com/blog/2023/03/24/hello-dolly-democratizing-magic-chatgpt-open-models.html)~~
    - "dolly-v1-6b is not a state-of-the-art generative language model and, though quantitative benchmarking is ongoing, is not designed to perform competitively with more modern model architectures or models subject to larger pretraining corpuses. It is designed for academic or research purposes, and to encourage model and engineering experimentation."
    - *Review: slow, not following instructions.*
- [ ] Better pdf parsing
- [ ] Similarity between the output and provided human answers (?)
- [ ] Confidence of the output. Probably a deadend though (?)
- [ ] Fact-check the output with human assessment (?)

## Resources

- [LangChain](https://github.com/hwchase17/langchain)
  - [Document Loaders](https://python.langchain.com/en/latest/modules/indexes/document_loaders.html)
  - [Question Answering over Docs](https://python.langchain.com/en/latest/use_cases/question_answering.html)
  - [Question Answering with Sources](https://python.langchain.com/en/latest/modules/chains/index_examples/qa_with_sources.html)
  - [Prompt Templates](https://python.langchain.com/en/latest/modules/prompts/prompt_templates.html)
- [mmz-001/knowledge_gpt](https://github.com/mmz-001/knowledge_gpt)
