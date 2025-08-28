import pandas as pd
import ast

MAX_UNITS = 14

def encode_traits(traits, all_traits):
    """Return dict of trait columns -> tier"""
    return {f"trait_{t}": next((x["tier_current"] for x in traits if x["name"] == t), 0)
            for t in all_traits}


def encode_units(units, all_champs, all_items, max_units=MAX_UNITS):
    """Return dict with unit presence, tier, and items"""
    row = {}

    for champ in all_champs:
        row[f"unit_{champ}"] = 0
        row[f"unit_{champ}_tier"] = 0
    for item in all_items:
        row[f"item_{item}"] = 0

    for u in units[:max_units]:
        champ = u["character_id"]
        row[f"unit_{champ}"] = 1
        row[f"unit_{champ}_tier"] = u["tier"]

        for it in u.get("itemNames", []):
            row[f"item_{it}"] += 1

    return row


df = pd.read_csv("data.csv", header=0)

df['traits'] = df['traits'].apply(ast.literal_eval)
df['units'] = df['units'].apply(ast.literal_eval)
all_traits = sorted({t["name"] for traits in df["traits"] for t in traits})
all_champs = sorted({u["character_id"] for units in df["units"] for u in units})
all_items = sorted({i for units in df["units"] for u in units for i in u.get("itemNames", [])})

rows = []
for _, row in df.iterrows():
    trait_features = encode_traits(row["traits"], all_traits)
    unit_item_features = encode_units(row["units"], all_champs, all_items)
    rows.append({
        "placement": row["placement"],
        "level": row["level"],
        **trait_features,
        **unit_item_features
    })

processed_df = pd.DataFrame(rows)

processed_df.to_csv("processed.csv", index=False)
