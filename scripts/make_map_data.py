"""Build the two small files behind the airport map (Figure 1).

Usage: python3 make_map_data.py data/

Writes
  data/airports.csv     IATA code, name, latitude and longitude of the 35 study airports and Kansas City,
                        from OurAirports (public domain, https://github.com/davidmegginson/ourairports-data)
  data/us_states.geojson  US state boundaries at 1:50m, from Natural Earth (public domain,
                        https://github.com/nvkelso/natural-earth-vector)
"""
import io, os, sys, json
import pandas as pd
import geopandas as gpd

out = sys.argv[1] if len(sys.argv) > 1 else 'data'
CODES = ['JFK', 'EWR', 'LAX', 'ONT', 'SNA', 'SFO', 'SJC', 'OAK', 'MIA', 'FLL', 'ATL', 'SEA', 'DFW', 'IAH', 'BOS', 'PHL',
         'ORD', 'IAD', 'BWI', 'CLT', 'RDU', 'DTW', 'MSP', 'STL', 'DEN', 'SLC', 'PHX', 'LAS', 'SAN', 'PDX', 'HNL',
         'MCO', 'TPA', 'AUS', 'SAT', 'MCI']

ap = pd.read_csv('https://raw.githubusercontent.com/davidmegginson/ourairports-data/main/airports.csv',
                 usecols=['iata_code', 'name', 'latitude_deg', 'longitude_deg', 'iso_country', 'type'])
ap = ap[(ap.iso_country == 'US') & ap.iata_code.isin(CODES) & ap.type.str.contains('airport')]
ap = (ap.rename(columns={'iata_code': 'iata', 'latitude_deg': 'lat', 'longitude_deg': 'lon'})
        [['iata', 'name', 'lat', 'lon']].drop_duplicates('iata').set_index('iata').loc[CODES].reset_index())
ap['lat'] = ap.lat.round(4); ap['lon'] = ap.lon.round(4)
ap.to_csv(os.path.join(out, 'airports.csv'), index=False)

st = gpd.read_file('https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'
                   'ne_50m_admin_1_states_provinces.geojson')
st = st[st.adm0_a3 == 'USA'][['postal', 'name', 'geometry']].reset_index(drop=True)
st['geometry'] = st.geometry.simplify(0.02, preserve_topology=True)
st.to_file(os.path.join(out, 'us_states.geojson'), driver='GeoJSON', COORDINATE_PRECISION=3)
print(len(ap), 'airports,', len(st), 'states')
