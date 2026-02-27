# Setup

This project targets **Python 3.11+**.

## Create and activate a virtual environment

macOS / Linux:

```bash
 python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
```

Windows (PowerShell):

```powershell
 py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
```

If you get an execution policy error, run this once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Install the library (editable) + workshop tools

```bash
pip install -e ".[dev,notebooks]"
```

## Optional: geospatial transforms (CRS)

If you plan to work with real-world coordinates, install the optional geospatial
extra to enable EPSG transforms.

Geo helpers live in `simulated_city.geo` and include convenience functions like
`wgs2utm(...)` / `utm2wgs(...)` plus the general `transform_xy(...)`.

```bash
pip install -e ".[geo]"
```

Tip: for notebooks that include both mapping + CRS transforms, you can install both extras:

```bash
pip install -e ".[notebooks,geo]"
```

## Open in VS Code

The repository ships a `.vscode/` folder with ready-to-use workspace settings.

1. Open the project folder in VS Code:

   ```bash
   code .
   ```

2. When prompted, install the **recommended extensions** (Python, Pylance, Jupyter).  
   You can also open them manually: **Extensions** → filter by `@recommended`.

3. Select the `.venv` interpreter:  
   Open the Command Palette → **Python: Select Interpreter** → choose `./.venv/bin/python`  
   (VS Code may detect it automatically from `settings.json`).

4. Run and debug using the pre-configured launch targets in the **Run and Debug** panel:

   | Launch target | What it does |
   |---|---|
   | **Run tests** | Runs `pytest -v` |
   | **simulated_city (CLI smoke)** | Runs `python -m simulated_city` |
   | **Demo: config + MQTT** | Runs `scripts/demo/01_config_and_mqtt.py` |
   | **Demo: beer drinker** | Runs `scripts/demo/03_beer_drinker.py` |

## Run notebooks

- VS Code: open a notebook in `notebooks/` and select the `.venv` kernel.
- Or start Jupyter:

```bash
jupyter lab
```

You can also run:

```bash
python -m jupyterlab
```

## Run tests

```bash
python -m pytest
```
