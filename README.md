# Forty-eight hours before kick-off: International air arrivals at the 2026 World Cup host airports

Data and code for the research note of the same title by Manuele Leonelli (School of Science and Technology, IE University, Madrid).

The note follows non-US-citizen air arrivals, day by day, at the sixteen airports serving ten US host areas of the 2026 FIFA World Cup, using the passport-control counts published by U.S. Customs and Border Protection, and compares them with nineteen US airports that hosted no matches.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/manueleleonelli/worldcup2026-arrivals/blob/main/analysis.ipynb)

## Contents

| Path | Description |
|---|---|
| `analysis.ipynb` | Reproduces Table 1, Figures 1 to 3 and every number in the text; Section 7 adds the checks requested in review (synthetic-control weights and fit, placebo-calibrated intervals, weeks after the final, overlapping match windows, connecting-hub checks) |
| `data/daily_by_airport.csv` | Daily passport-control counts and waiting times for 36 airports, 3 May 2023 to 6 October 2026 |
| `data/wc2026_matches.csv` | The 104 matches of the tournament with date, venue, stage and result |
| `data/airports.csv`, `data/us_states.geojson` | Airport coordinates and state boundaries for the map in Figure 1 |
| `output/` | Tables, figures and synthetic-control weights produced by the notebook; `output/supplement/` holds the review checks |
| `scripts/parse_schedule.py` | Builds `wc2026_matches.csv` from the openfootball fixture files |
| `scripts/make_map_data.py` | Builds `airports.csv` and `us_states.geojson` from OurAirports and Natural Earth |

## Running the analysis

In Google Colab, click the badge and choose *Runtime > Run all*; the data are read directly from this repository. Locally:

```
pip install -r requirements.txt
jupyter notebook analysis.ipynb
```

The notebook runs in about two minutes. Setting `DOWNLOAD = True` in the first cell rebuilds `data/daily_by_airport.csv` from the CBP site, which takes about 30 minutes.

## Data

**Passport-control counts.** U.S. Customs and Border Protection publishes, for every airport and terminal at which it processes international arrivals, hourly counts of arriving passengers and their waiting times at passport control, separately for US and non-US citizens ([Airport Wait Times](https://awt.cbp.gov)). The hourly records were aggregated to days. Columns of `daily_by_airport.csv`:

| Column | Description |
|---|---|
| `airport` | IATA code |
| `date` | Calendar day |
| `usa`, `nonusa`, `total` | Passengers processed: US citizens, non-US citizens, all |
| `flights` | Arriving international flights |
| `usa_max_wait`, `nonusa_max_wait`, `all_max_wait` | Largest hourly maximum wait of the day, in minutes |
| `nonusa_avg_wait`, `all_avg_wait` | Passenger-weighted average wait, in minutes |

Host airports: JFK, EWR (New York/New Jersey); LAX, ONT, SNA (Los Angeles); SFO, SJC, OAK (San Francisco Bay Area); MIA, FLL (Miami); DFW (Dallas); IAH (Houston); BOS; PHL; SEA; ATL. Kansas City has no passport-control reporting. Comparison airports (US international airports without matches that report on at least 98% of days): ORD, IAD, BWI, CLT, RDU, DTW, MSP, STL, DEN, SLC, PHX, LAS, SAN, PDX, HNL, MCO, TPA, AUS, SAT. Cincinnati (CVG) is in the daily file but not used, as it reports on only 91% of days. The connecting-traffic checks leave out the hubs ORD, IAD, DEN, DTW, MSP, CLT, PHX and SLC.

**Match schedule.** Taken from the public-domain [openfootball](https://github.com/openfootball/worldcup) fixture files for the 2026 tournament.

**Map.** Airport coordinates from [OurAirports](https://github.com/davidmegginson/ourairports-data) and state boundaries from [Natural Earth](https://www.naturalearthdata.com), both in the public domain.

## Licence

Code: MIT licence. The CBP data are a work of the US Government and in the public domain; the openfootball, OurAirports and Natural Earth data are in the public domain.
