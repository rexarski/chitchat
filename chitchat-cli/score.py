# group answers to questions by `code`
# add bonus score to base score
# calcualte the mean of all scores (78 questions)

import pandas as pd
import json

with open('output.json') as f:
    data = json.load(f)
df = pd.DataFrame(data, columns=['code', 'score', 'var', 'answer'])

def calculate_score(row):
    if row['variation'] == 'v2' and 'YES' in row['answer']:
        return row['score'] + 1
    else:
        return row['score']

df['score'] = df.apply(calculate_score, axis=1)
df = df.groupby('code')['score'].sum().reset_index()

print(df)
