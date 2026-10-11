# Ruang — Sarawak cultural heritage

A local Streamlit prototype with a searchable seed catalogue, community and theme filters, heritage map, session-based favourites, JSON export, and downloadable visit outline.

## Run

From this directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (normally http://localhost:8501).

Content is an introductory demonstration drawn from the linked Sarawak Tourism Board and Sarawak Museum Department sources. The map contains one approximate museum location; traditions are not assigned map coordinates. No copyrighted photographs or cultural motifs are reproduced. Community review and consented media should precede public release.

Favourites persist only during a Streamlit browser session. No database, bookings, or visitor data collection is implemented. The visit planner is an outline and does not verify opening hours or availability.
