# PRC Data Challenge 2026 — team enthusiastic-yawn

Taxi-out time prediction for the [PRC Data Challenge 2026](https://prc-data-challenge-2026.netlify.app/)
(EUROCONTROL Performance Review Commission / OpenSky Network).

The model predicts `TAXITIME_SEC_mvt` (take-off time minus off-block time, in seconds)
for every departure in the challenge ranking set. The whole pipeline is a single notebook:
[`PRC_Data_Challenge_2026_V17_2_FINAL_ONE_RUN.ipynb`](PRC_Data_Challenge_2026_V17_2_FINAL_ONE_RUN.ipynb).

## Method (V17.2)

Departures are split by whether they have a usable Network Manager (NM) off-block anchor.

```text
KNOWN NM ANCHOR                          MISSING NM ANCHOR (~1%)
        |                                        |
operational / queue / recurrence         real + synthetic missing-anchor
features                                 training rows
        |                                        |
one LightGBM (≤ 1200 trees)              peer-imputed pseudo anchor
        |                                        |
NM anchor + predicted residual           one LightGBM correction (≤ 1200 trees)
```

Feature groups:

- calendar and NM timestamp features; the anchor is take-off time minus the first available
  NM off-block time, in the order AOBT, EOBT, IOBT, LOBT
- airport × stand × runway and operator / recurring-flight features
- NM match-quality features
- runway arrival/departure sequence, gap and queue features
- off-block → take-off movement counts (dynamic temporal graph built from movement times only, no labels)
- static graph embeddings (truncated SVD, 8 dimensions) over challenge columns
- leakage-safe historical priors (airport, runway, hour, stand)

No CatBoost, neural networks or multi-model ensembles are used.

Run order in the notebook:

1. Development validation: train on Jan–Sep 2025, validate on October 2025.
2. Freeze the selected LightGBM iteration count and missing-anchor configuration.
3. Retrain on all 2025 training departures.
4. Predict every departure in the ranking file.
5. Build, save and re-validate the submission parquet.

### Note on feature timing

The dynamic graph features use movements on both sides of each departure (centred and
future neighbours). That fits the retrospective, post-operations purpose of the challenge,
but these features would not be available in a pre-pushback forecasting setting.

## Data

The challenge data is not redistributed here. Download it from the OpenSky MinIO bucket
`prc-2026-datasets` (challenge registration required) and place it in `data/raw/`:

- `training_2025-01-01_2025-02-01.parquet` … `training_2025-12-01_2026-01-01.parquet` (12 files)
- `final_ranking.parquet` and `final_submitting.parquet` (final phase: Jan, Feb, Jun, Jul 2026)

If the two `final_*` files are absent, the notebook falls back to `ranking.parquet` and
`submitting.parquet` (ranking phase) and names the output `enthusiastic-yawn_v<N>.parquet`.

## Running

### Google Colab

Open the notebook and run all cells. Cell 2 prompts for the parquet files (or a zip) and
copies them to `/content/data/raw/`.

### Locally

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt   # macOS: brew install libomp first

mkdir -p work/data/raw && cp /path/to/challenge/*.parquet work/data/raw/
PRC_ROOT=$PWD/work .venv/bin/python run_local.py > run.log 2>&1
```

`run_local.py` executes the notebook's code cells in order and streams progress to the log.
You can also run the notebook in Jupyter with `PRC_ROOT` set.

The full run uses about 4.2M 2025 movements as context and is memory-intensive. The notebook
prints RAM usage at each major step.

### Output

`$PRC_ROOT/outputs/enthusiastic-yawn_final.parquet` with exactly two columns,
`MVT_ID_mvt` and `TAXITIME_SEC_mvt`. Before saving, the notebook checks that the file has
the template's row count and ID order, unique IDs and finite predictions. It then reads the
saved file back and checks it again.

## Results

October 2025 validation RMSE is 240.3 s overall and 223.9 s on departures with an NM anchor.
[`results/SUBMISSION.md`](results/SUBMISSION.md) records the final submission (checksum, upload
time, validation table). [`results/final_run.log`](results/final_run.log) is the full log of
the run that produced it.

## Reproducibility

- Base seed `SEED = 42`. Every model seed is a fixed offset from it.
- LightGBM runs on CPU (`device_type="cpu"`).
- Package versions used for the final run are pinned in `requirements.txt` (Python 3.12.10).

## License

Copyright (C) 2026 team enthusiastic-yawn.

This program is free software: you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software Foundation, version 3.
See [`LICENSE`](LICENSE).
