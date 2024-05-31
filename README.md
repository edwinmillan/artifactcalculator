# ArtifactCalculator

Currently supports a specific format within artifact sheets. `.md` and `.txt`.

The line needs to start with `(<somenumbers>)` like `(15)` and the pp defined must be as follows: `X Lvl. X PP` with that exact capitalization and punctuation. so `50 Lvl. 3 PP` would work but not `50 lvl 3 pP`. 

I could address it, but I feel that consistency is king when making Artifacts by hand. 


# Requirements
You can install [Poetry](https://python-poetry.org/docs/#installation) and run `poetry install` 


# Running

If you're running it without poetry:
`python ./src/artifactcalculator/main.py`

With poetry:
`poetry run python ./src/artifactcalculator/main.py`

Windows Executable from [Release Page](https://github.com/edwinmillan/artifactcalculator/releases/)
`artifactcalculator.exe`