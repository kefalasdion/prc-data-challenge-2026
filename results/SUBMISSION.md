# Final submission record

| Item | Value |
| --- | --- |
| Team | enthusiastic-yawn |
| Stage | Final (Jan, Feb, Jun, Jul 2026) |
| File | `enthusiastic-yawn_final.parquet` |
| Bucket | `prc-2026-enthusiastic-yawn` |
| Uploaded | 2026-10-14T11:05:53Z (MinIO client `mc cp`) |
| Rows | 670,790 (matches `final_submitting.parquet`, same ID order) |
| Columns | `MVT_ID_mvt` (double), `TAXITIME_SEC_mvt` (float) |
| Size | 6,250,414 bytes |
| SHA-256 | `7a6efff26a4701e54d18532fb7411d0575f8bb4be710a09846aeedccd58f574b` |
| MD5 / S3 ETag | `465ce81ffd6a8b1b098f5b332cce2078` |

Produced by one top-to-bottom run of
[`PRC_Data_Challenge_2026_V17_2_FINAL_ONE_RUN.ipynb`](../PRC_Data_Challenge_2026_V17_2_FINAL_ONE_RUN.ipynb)
with `run_local.py`. The full log is in [`final_run.log`](final_run.log).

## October 2025 development validation

The model was trained on Jan–Sep 2025 and validated on October 2025, with 185,674 departures.

| Subset | Rows | RMSE (s) | MAE (s) |
| --- | --- | --- | --- |
| Known NM anchor | 183,761 | 223.9 | 144.8 |
| Missing NM anchor, frozen V9 benchmark | 1,913 | 888.6 | 381.3 |
| Missing NM anchor, V17 peer branch | 1,913 | 1,081.7 | 416.6 |
| Overall (known + V9 benchmark) | 185,674 | 240.3 | — |

Production settings were frozen from this run: main LightGBM 1,195 trees, missing-anchor
LightGBM 81 trees, and missing blend 0.9 peer-corrected + 0.1 historical.

The notebook's production path uses the V17 peer branch for the 9,077 final departures
(1.35%) without an NM anchor. On October 2025 that branch validated worse than the
frozen V9 benchmark.

## Final prediction summary

Median predicted taxi-out by month: Jan 976 s, Feb 929 s, Jun 934 s, Jul 954 s.
The July 2025 training median was 948 s. Predictions are clipped at 0 s.
