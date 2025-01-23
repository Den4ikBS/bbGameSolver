#!/usr/bin/bash

cd "$(dirname "$0")"
source ".venv/bin/activate"
cd "./src"
python3 -m bbGameSolver.gui.App

