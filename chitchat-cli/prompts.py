# flake8: noqa
from langchain.prompts import PromptTemplate

# Two types of prompts: interrogative questions (INT) which requires only YES or NO as an answer, and wh-questions (WH) which requires a detailed answer.

template_int = """Create a final answer to the given questions using the provided document excerpts (in no particular order) as references.

Follow the rules below:

- ALWAYS include a "[SOURCES]" section in your answer including only the minimal set of sources needed to answer the question.
- For questions starting with a 'Has', 'Have', 'Had', 'Do', 'Does', 'Did', 'Is', or 'Are', you are only allowed to answer 'YES' or 'NO'.
- If you are unsure about the answer to this type of questions, reply with 'NO'.
- Do not attempt to fabricate an answer and leave the [SOURCES] section empty.
- Give a [SCORE] for each answer based on the criteria below:
    - If the answer starts with a 'YES', give it a [SCORE] of 2.
    - If the answer starts with a 'NO', give it a [SCORE] of 0.

---------
QUESTION: Does it provide more support for patients and families?
=========
Content: More support for patients and families. To get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. It’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more. ARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
Source: 1-32
=========
[FINAL ANSWER]:YES.[SOURCES]:1-32[SCORE]:2

---------
[QUESTION]: Does the content talk about Superman and Batman?
=========
Content: More support for patients and families. To get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. It’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more. ARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
Source: 1-32
=========
[FINAL ANSWER]:NO\n[SOURCES]:1-32\n[SCORE]:0

---------

[QUESTION]: {question}
=========
{summaries}
=========
[FINAL ANSWER]:"""

STUFF_PROMPT_INT = PromptTemplate(
    template=template_int, input_variables=["summaries", "question"]
)

template_wh = """Create a final answer to the given questions using the provided document excerpts (in no particular order) as references.

Follow the rules below:

- ALWAYS include a "[SOURCES]" section in your answer including only the minimal set of sources needed to answer the question.
- For questions starting with a 'How', 'What', 'Who', 'Where', 'Why', or 'Whose' questions, give detailed answers.
- If you are unsure about the answer to this type of questions, reply with 'UNKNOWN'. Do not attempt to fabricate an answer and leave the [SOURCES] section empty.
- Give a [SCORE] for each answer based on the criteria below:
    - If the answer is 'UNKNOWN', give it a [SCORE] of 0.
    - Give it a [SCORE] of 1 if the question is partially answered, a [SCORE] of 2 if the question is fully answered and a [SCORE] of 3 if the answer is beyond the scope of the question.

---------

[QUESTION]: What is the purpose of ARPA-H?
=========
Content: More support for patients and families. To get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. It’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more. ARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
Source: 1-32
Content: While we’re at it, let’s make sure every American can get the health care they need. We’ve already made historic investments in health care. We’ve made it easier for Americans to get the care they need, when they need it. We’ve made it easier for Americans to get the treatments they need, when they need them. We’ve made it easier for Americans to get the medications they need, when they need them.
Source: 1-33
Content: The V.A. is pioneering new ways of linking toxic exposures to disease, already helping  veterans get the care they deserve. We need to extend that same care to all Americans. That’s why I’m calling on Congress to pass legislation that would establish a national registry of toxic exposures, and provide health care and financial assistance to those affected.
Source: 1-30
=========
[FINAL ANSWER]:The purpose of ARPA-H is to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.\n[SOURCES]:1-32\n[SCORE]:2

---------

[QUESTION]: Who is most powerful individual in the world?
=========
Content: More support for patients and families. To get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. It’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more. ARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
Source: 1-32
Content: While we’re at it, let’s make sure every American can get the health care they need. We’ve already made historic investments in health care. We’ve made it easier for Americans to get the care they need, when they need it. We’ve made it easier for Americans to get the treatments they need, when they need them. We’ve made it easier for Americans to get the medications they need, when they need them.
Source: 1-33
Content: The V.A. is pioneering new ways of linking toxic exposures to disease, already helping  veterans get the care they deserve. We need to extend that same care to all Americans. That’s why I’m calling on Congress to pass legislation that would establish a national registry of toxic exposures, and provide health care and financial assistance to those affected.
Source: 1-30
=========
[FINAL ANSWER]:UNKNOWN\n[SOURCES]:\n[SCORE]:0

---------

[QUESTION]: {question}
=========
{summaries}
=========
[FINAL ANSWER]:"""

STUFF_PROMPT_WH = PromptTemplate(
    template=template_wh, input_variables=["summaries", "question"]
)
