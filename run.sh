#!/bin/bash

# Létrehozza a venv-et, ha nem létezik
if [ ! -d "venv" ]; then
    echo "Virtuális környezet létrehozása..."
    python3 -m venv venv
fi

# Aktiválja a venv-et
source venv/bin/activate

# Telepíti a függőségeket
pip install -r requirements.txt

# Elindítja a programot
python main.py
