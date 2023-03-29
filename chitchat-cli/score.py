import pandas as pd
import json

# df = pd.DataFrame(
#     {
#         "code": ["A", "A", "B", "B", "C", "C", "D", "D", "E"],
#         "score": [3, 2, 2, 1, 1, 2, 2, 2, 0],
#         "variation": ["v1", "v2", "v1", "v2", "v1", "v2", "v1", "v2", "v1"],
#         "answer": [True, False, True, False, True, True, False, True, True],
#     }
# )

# For the following input:
#   code  score variation  answer
# 0    A      3        v1    True
# 1    A      2        v2   False
# 2    B      2        v1    True
# 3    B      1        v2   False
# 4    C      1        v1    True
# 5    C      2        v2    True
# 6    D      2        v1   False
# 7    D      2        v2    True
# 8    E      0        v1    True

# We expect the following output:
#       answer  score_v1  score_v2  score  ideal  score_ideal_ratio
# code
# A       True         3       2.0      3      3           1.000000
# B       True         2       1.0      2      3           0.666667
# C       True         1       2.0      2      3           0.666667
# D      False         2       2.0      3      3           1.000000
# E       True         0       NaN      0      2           0.000000


def calculate_score(filepath):
    with open(filepath) as f:
        data = json.load(f)

    df = pd.DataFrame(data, columns=["code", "score", "variation", "answer"])

    # Group the dataframe by code and keep answers from variation v1
    df_v1 = df.loc[df["variation"] == "v1"].groupby("code")[["answer", "score"]].first()

    # Calculate bonus points for score of variation v1 and v2
    df_v2 = df.loc[df["variation"] == "v2"].groupby("code")["score"].first()

    df_merged = df_v1.merge(df_v2, on="code", how="left", suffixes=("_v1", "_v2"))

    # Calculate final score based on score_x and score_y
    df_merged["score"] = (
        df_merged["score_v1"]
        + df_merged["score_v2"].apply(lambda x: 1 if x >= 2 else 0)
    ).apply(lambda y: min(y, 3))
    df_merged["ideal"] = df_merged["score_v2"].apply(
        lambda x: 3 if pd.notnull(x) else 2
    )
    df_merged["score_ideal_ratio"] = df_merged["score"] / df_merged["ideal"]
    df_merged = df_merged.reset_index()
    company_level_score = round(df_merged["score_ideal_ratio"].mean(), 2)

    return (df_merged, company_level_score)
