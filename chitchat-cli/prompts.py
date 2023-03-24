# flake8: noqa
from langchain.prompts import PromptTemplate

## Use a shorter template to reduce the number of tokens in the prompt
template = """Create a final answer to the given questions using the provided document excerpts(in no particular order) as references. ALWAYS include a "SOURCES" section in your answer including only the minimal set of sources needed to answer the question. If you are unable to answer the question, simply state that you do not know by answering 'UNKNOWN'. You must use 'YES' or 'NO' to answer any questions starting with a 'Has', 'Have', 'Had', 'Do', 'Does', 'Did', 'Is', or 'Are'. Do not attempt to fabricate an answer and leave the SOURCES section empty.

---------

QUESTION: What is the purpose of ARPA-H?
=========
Content: More support for patients and families. To get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. It’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more. ARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
Source: 1-32
Content: While we’re at it, let’s make sure every American can get the health care they need. We’ve already made historic investments in health care. We’ve made it easier for Americans to get the care they need, when they need it. We’ve made it easier for Americans to get the treatments they need, when they need them. We’ve made it easier for Americans to get the medications they need, when they need them.
Source: 1-33
Content: The V.A. is pioneering new ways of linking toxic exposures to disease, already helping  veterans get the care they deserve. We need to extend that same care to all Americans. That’s why I’m calling on Congress to pass legislation that would establish a national registry of toxic exposures, and provide health care and financial assistance to those affected.
Source: 1-30
=========
FINAL ANSWER: The purpose of ARPA-H is to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
SOURCES: 1-32
---------

QUESTION: What is most powerful individual in the world?
=========
Content: More support for patients and families. To get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. It’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more. ARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
Source: 1-32
Content: While we’re at it, let’s make sure every American can get the health care they need. We’ve already made historic investments in health care. We’ve made it easier for Americans to get the care they need, when they need it. We’ve made it easier for Americans to get the treatments they need, when they need them. We’ve made it easier for Americans to get the medications they need, when they need them.
Source: 1-33
Content: The V.A. is pioneering new ways of linking toxic exposures to disease, already helping  veterans get the care they deserve. We need to extend that same care to all Americans. That’s why I’m calling on Congress to pass legislation that would establish a national registry of toxic exposures, and provide health care and financial assistance to those affected.
Source: 1-30
=========
FINAL ANSWER: UNKNOWN
SOURCES:

---------

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""

STUFF_PROMPT = PromptTemplate(
    template=template, input_variables=["summaries", "question"]
)
