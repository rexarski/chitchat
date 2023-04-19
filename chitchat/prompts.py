# flake8: noqa
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate

examples = [
    {
        "question": "Does it provide more support for patients and families?",
        "summaries": """
        Content: More support for patients and families. To get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. It’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more. ARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
        Source: 1-32
        [FINAL ANSWER]:YES.[SOURCES]:1-32[SCORE]:2
        """,
    },
    {
        "question": "Does the content talk about Superman and Batman?",
        "summaries": """
        Content: More support for patients and families. To get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. It’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more. ARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
        Source: 1-32
        [FINAL ANSWER]:NO\n[SOURCES]:1-32\n[SCORE]:0
        """,
    },
    {
        "question": "What is the purpose of ARPA-H?",
        "summaries": """
        Content: More support for patients and families. To get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. It’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more. ARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
        Source: 1-32
        Content: While we’re at it, let’s make sure every American can get the health care they need. We’ve already made historic investments in health care. We’ve made it easier for Americans to get the care they need, when they need it. We’ve made it easier for Americans to get the treatments they need, when they need them. We’ve made it easier for Americans to get the medications they need, when they need them.
        Source: 1-33
        Content: The V.A. is pioneering new ways of linking toxic exposures to disease, already helping  veterans get the care they deserve. We need to extend that same care to all Americans. That’s why I’m calling on Congress to pass legislation that would establish a national registry of toxic exposures, and provide health care and financial assistance to those affected.
        Source: 1-30
        [FINAL ANSWER]:The purpose of ARPA-H is to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.\n[SOURCES]:1-32\n[SCORE]:2
        """,
    },
    {
        "question": "Who is most powerful individual in the world?",
        "summaries": """
        Content: More support for patients and families. To get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. It’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more. ARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
        Source: 1-32
        Content: While we’re at it, let’s make sure every American can get the health care they need. We’ve already made historic investments in health care. We’ve made it easier for Americans to get the care they need, when they need it. We’ve made it easier for Americans to get the treatments they need, when they need them. We’ve made it easier for Americans to get the medications they need, when they need them.
        Source: 1-33
        Content: The V.A. is pioneering new ways of linking toxic exposures to disease, already helping  veterans get the care they deserve. We need to extend that same care to all Americans. That’s why I’m calling on Congress to pass legislation that would establish a national registry of toxic exposures, and provide health care and financial assistance to those affected.
        Source: 1-30
        [FINAL ANSWER]:UNKNOWN\n[SOURCES]:\n[SCORE]:0
        """,
    },
]

example_template = """
[QUESTION]: {question}
=========
{summaries}
=========
[FINAL ANSWER]:
"""

example_prompt = PromptTemplate(
    input_variables=["summaries", "question"], template=example_template
)

prefix = """
Create a final answer to the given questions using the provided document excerpts (in no particular order) as references.

- Always give a detailed answer.
- Always include a "[SOURCES]" section in your answer including only the minimal set of sources needed to answer the question.
- Use 'YES' or 'NO' to answer questions starting with a 'Has', 'Have', 'Had', 'Do', 'Does', 'Did', 'Is', or 'Are', you are required to answer 'YES' or 'NO' at first, then followed a detailed answer. Answer 'NO' if you are unsure, and leave the [SOURCES] section empty.
- Do not use 'YES' or 'NO' to answer questions starting with a 'How', 'What', 'Who', 'Where', 'Why', or 'Whose' questions, give detailed answers instead. Answer 'UNKNOWN' if you are unsure, and leave the [SOURCES] section empty.
- Give a [SCORE] for each answer based on the criteria below:
    - If the answer starts with a 'YES', give it a [SCORE] of 2.
    - If the answer starts with a 'NO', give it a [SCORE] of 0.
    - If the answer is 'UNKNOWN', give it a [SCORE] of 0.
    - Give it a [SCORE] of 1 if the question is partially answered, a [SCORE] of 2 if the question is fully answered and a [SCORE] of 3 if the answer is beyond the scope of the question.
"""

suffix = """
[QUESTION]: {question}
=========
{summaries}
=========
[FINAL ANSWER]:
"""

STUFF_PROMPT = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["question", "summaries"],
)
