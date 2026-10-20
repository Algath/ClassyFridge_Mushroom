```bash
git clone <url-de-ton-fork> && cd FungiTastic
uv venv && uv pip install -r baselines/closed_set/requirements.txt
mkdir -p data && cd dataset && uv run python download.py --metadata --images --subset "m" --size "300" --save_path "../data" && cd ..
cd baselines/closed_set && uv run python prepare_metadata.py
```
