"""Parse the openfootball 2026 World Cup fixture files into a tidy CSV.

Usage: python3 parse_schedule.py cup.txt cup_finals.txt wc2026_matches.csv

Input files: https://github.com/openfootball/worldcup, folder 2026--canada-usa-mexico.
"""
import re
import sys
import csv

MONTHS = {"Jun": 6, "June": 6, "Jul": 7, "July": 7}

CITY_TO_METRO = {
    "Mexico City": ("Mexico City", "MX"),
    "Guadalajara": ("Guadalajara", "MX"),
    "Monterrey": ("Monterrey", "MX"),
    "Atlanta": ("Atlanta", "US"),
    "Boston": ("Boston", "US"),
    "Dallas": ("Dallas", "US"),
    "Houston": ("Houston", "US"),
    "Kansas City": ("Kansas City", "US"),
    "Los Angeles": ("Los Angeles", "US"),
    "Miami": ("Miami", "US"),
    "New York/New Jersey": ("New York/New Jersey", "US"),
    "Philadelphia": ("Philadelphia", "US"),
    "San Francisco Bay Area": ("San Francisco Bay Area", "US"),
    "Seattle": ("Seattle", "US"),
    "Toronto": ("Toronto", "CA"),
    "Vancouver": ("Vancouver", "CA"),
}

DATE_RE = re.compile(r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(Jun|June|Jul|July)\s+(\d{1,2})\s*$")
STAGE_RE = re.compile(r"^▪\s+(.+?)\s*$")
GROUP_RE = re.compile(r"^▪\s+Group ([A-L])\s*$")
# e.g. "  (73) 12:00 UTC-7  South Africa 0-1 (0-0) Canada   @ Los Angeles (Inglewood)   ## 2A v 2B"
MATCH_RE = re.compile(
    r"^\s*(?:\((\d+)\)\s*)?(\d{1,2}:\d{2})\s+UTC([+-]\d+)\s+(.+?)\s+@\s+([^#]+?)\s*(?:##.*)?$"
)
SCORE_RE = re.compile(r"^(.+?)\s+(\d+-\d+(?:\s+a\.e\.t\.)?(?:\s*\([^)]*\))?(?:,\s*\d+-\d+\s+pen\.)?)\s+(.+)$")


def parse(path, stage_default=None):
    rows = []
    stage = stage_default
    group = None
    date = None
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            m = GROUP_RE.match(line)
            if m:
                group = m.group(1)
                stage = "Group stage"
                continue
            m = STAGE_RE.match(line)
            if m and "Matchday" not in m.group(1):
                stage = m.group(1).strip()
                group = None
                continue
            m = DATE_RE.match(line.strip())
            if m:
                date = f"2026-{MONTHS[m.group(2)]:02d}-{int(m.group(3)):02d}"
                continue
            m = MATCH_RE.match(line)
            if m and date:
                num, local_time, utc_off, teams, city = m.groups()
                city = city.strip()
                base_city = re.sub(r"\s*\(.*\)\s*$", "", city).strip()
                metro, country = CITY_TO_METRO[base_city]
                sm = SCORE_RE.match(teams.strip())
                if sm:
                    home, score, away = sm.group(1).strip(), sm.group(2).strip(), sm.group(3).strip()
                else:
                    home, score, away = teams.strip(), "", ""
                rows.append({
                    "match_no": num or "",
                    "date": date,
                    "local_time": local_time,
                    "utc_offset": utc_off,
                    "stage": stage,
                    "group": group or "",
                    "home": home,
                    "away": away,
                    "score": score,
                    "city": base_city,
                    "venue_city": city,
                    "metro": metro,
                    "country": country,
                })
    return rows


def main():
    groups, finals, out = sys.argv[1:4]
    rows = parse(groups) + parse(finals)
    rows.sort(key=lambda r: (r["date"], r["local_time"]))
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "matches written to", out)


if __name__ == "__main__":
    main()
