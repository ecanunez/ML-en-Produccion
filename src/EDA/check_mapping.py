import pandas as pd

mapping = pd.read_parquet(
    "data/interim/player_mapping.parquet"
)

print("\nAMBIGUOUS")
print(
    mapping[
        mapping["method"] == "ambiguous"
    ]
    .head(50)
)

print("\nNOT FOUND")
print(
    mapping[
        mapping["method"] == "not_found"
    ]
    .head(50)
)

mapping_df = pd.read_parquet(
    "data/interim/player_mapping.parquet"
)

not_found = mapping_df[
    mapping_df["method"] == "not_found"
]

print(
    not_found["lineup_name"]
    .sort_values()
    .head(100)
)

not_found = mapping_df[
    mapping_df["method"] == "not_found"
]

print(len(not_found))