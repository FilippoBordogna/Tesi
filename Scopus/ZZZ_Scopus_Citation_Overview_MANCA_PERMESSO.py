from datetime import date
import pandas as pd
from pybliometrics.scopus import CitationOverview
from pybliometrics.scopus.utils import config

# print("My API-Key: "+config['Authentication']['APIKey']+"\nMy Token: "+config['Authentication']['InstToken'])

### CitationOverview(identifier, start, end=2021, id_type='scopus_id', eid=None, refresh=False, citation=None, **kwds) ###
co=CitationOverview(identifier="85113200085", start=1992, end=date.today().year, id_type='scopus_id', eid=None, refresh=False, citation=None);

for numero in range(2):
    print("******************************************************************************************************************************************************");
print("*****************************************************************INIZIO DEL PROGRAMMA*****************************************************************");
for numero in range(2):
    print("******************************************************************************************************************************************************");



# DATI API
print("\n\nAPI:\nRimanenti: "+co.get_key_remaining_quota()+"\nRefresh: "+co.get_key_reset_time());