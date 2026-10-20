import os, sys
import pandas as pd

DATA = sys.argv[1] if len(sys.argv) > 1 else "../../data/FungiTastic"
DATA = os.path.abspath(DATA)
META = f"{DATA}/metadata/FungiTastic-Mini"
IMG = f"{DATA}/FungiTastic-Mini"
SIZE = "300p"

os.makedirs("metadata", exist_ok=True)
for split, name in [("train", "Train"), ("val", "Val"), ("test", "Test")]:
    df = pd.read_csv(f"{META}/FungiTastic-Mini-{name}.csv")
    df = df.rename(columns={"category_id": "class_id"})
    df["image_path"] = df["filename"].apply(lambda f: f"{IMG}/{split}/{SIZE}/{f}")
    missing = (~df["image_path"].head(20).apply(os.path.exists)).sum()
    print(f"{split}: {len(df)} lignes, {missing}/20 images introuvables (échantillon)")
    df.to_csv(f"metadata/FungiTastic-Mini-{name}.csv", index=False)
