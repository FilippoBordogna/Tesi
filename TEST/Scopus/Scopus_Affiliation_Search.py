import pandas as pd
from pybliometrics.scopus import AffiliationSearch
from pybliometrics.scopus.utils import config

# print("My API-Key: "+config['Authentication']['APIKey']+"\nMy Token: "+config['Authentication']['InstToken'])

### AffiliationSearch(query, refresh=False, verbose=False, download=True, integrity_fields=None, integrity_action='raise', count=200, **kwds) ###
q="AFFIL(AFFILCITY(Bergamo) AND AFFILCOUNTRY(Italy))";
afs=AffiliationSearch(query=q, refresh=False, verbose=False, download=True, integrity_fields=None, integrity_action="raise");

for numero in range(5):
    print("******************************************************************************************************************************************************");
print("*****************************************************************INIZIO DEL PROGRAMMA*****************************************************************");
for numero in range(5):
    print("******************************************************************************************************************************************************");

print("Affiliation Search Results (\""+q+"\"):\nNumber of Results: "+str(afs.get_results_size()));
print(pd.DataFrame(afs.affiliations));

# DATI API
#print("\n\nAPI:\nRimanenti: "+afs.get_key_remaining_quota()+"\nRefresh: "+afs.get_key_reset_time());