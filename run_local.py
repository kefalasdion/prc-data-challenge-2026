"""Run the V17.2 notebook top to bottom as a plain Python script.

Executes every code cell in order and streams progress to stdout, so a long
local run can be followed in a log file. This is how the final submission was
produced on macOS.

Usage:
    PRC_ROOT=/path/to/workdir python run_local.py > run.log 2>&1

PRC_ROOT must contain data/raw/ with the challenge parquet files; the
submission is written to PRC_ROOT/outputs/.
"""

import json
import os
import sys
from pathlib import Path

NOTEBOOK = Path(__file__).with_name("PRC_Data_Challenge_2026_V17_2_FINAL_ONE_RUN.ipynb")

if not os.environ.get("PRC_ROOT"):
    sys.exit("Set PRC_ROOT to a directory containing data/raw/*.parquet")

os.environ.setdefault("MPLBACKEND", "Agg")

from IPython.display import display  # noqa: E402  (used by the notebook cells)

cells = json.loads(NOTEBOOK.read_text())["cells"]
namespace = {"display": display, "__name__": "__main__"}

for i, cell in enumerate(cells):
    if cell["cell_type"] != "code":
        continue
    print(f"\n#### CELL {i} START", flush=True)
    exec(compile("".join(cell["source"]), f"<cell {i}>", "exec"), namespace)

print("\n#### DONE", flush=True)
