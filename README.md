# ASM Annotator v2

A CLI tool for manually labeling geographic points of interest using Google Earth Pro's historical imagery. For each point in a CSV, the tool generates a bounding-box KML, opens it in Google Earth Pro to fly to that location on a target date, and prompts for a label and confidence score.

## Requirements

- macOS (uses `open -a` to launch apps)
- Python 3.10+ (uses `X | None` syntax)
- [Google Earth Pro](https://www.google.com/earth/about/versions/) installed as `Google Earth Pro.app`

> **Cross-platform note:** [src/gep_launcher.py](src/gep_launcher.py) shells out to the macOS `open` command to launch Google Earth Pro and hand it each target KML. To run on Linux or Windows, swap those calls for the platform equivalent (`xdg-open` or a direct path to the `google-earth-pro` binary on Linux; `os.startfile()` or `start` on Windows).

## GEP Settings

In Google Earth Pro, open **Preferences > Navigation** and set:

- **Fly-To Speed** → top speed (max)
- **Mouse Wheel Speed** → medium
- Check **Do not automatically tilt while zooming**

These keep each fly-to snappy and the view flat, so the bounding box lines up cleanly with the historical imagery.

## Usage

```bash
python src/main.py            # uses data/sites.csv
python src/main.py path/to/my.csv
```

The CSV must have columns `lat,lon,label,confidence`. Rows with a blank `label` are queued for annotation; already-labeled rows are skipped, so you can resume at any time.

For each point, enter a two-character response at the prompt:

- First char: `P` (positive) or `N` (negative)
- Second char: `1`–`5` (confidence)

Example: `P3`, `N5`. Progress is saved to the CSV after every annotation. `Ctrl-C` exits safely.

## Layout

- [src/main.py](src/main.py) — interactive loop
- [src/kml_generator.py](src/kml_generator.py) — KML construction (target bbox + watcher network link)
- [src/gep_launcher.py](src/gep_launcher.py) — launches Google Earth Pro and reopens the target KML
- [src/csv_handler.py](src/csv_handler.py) — CSV load/save with atomic writes
- [src/config.py](src/config.py) — paths, bbox buffer, LookAt range, target date
