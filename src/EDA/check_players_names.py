import pandas as pd

mapping = pd.read_parquet(
    "data/interim/player_mapping.parquet"
)

nf = mapping[
    mapping["method"] == "not_found"
]

print(
    nf["lineup_name"]
    .sort_values()
    .to_string(index=False)
)

players_df[
    players_df["name"]
    .str.contains("kja", case=False, na=False)
][["player_id", "name"]]