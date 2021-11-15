import pandas as pd
from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus.utils import config

# print("My API-Key: "+config['Authentication']['APIKey']+"\nMy Token: "+config['Authentication']['InstToken'])

### ScopusSearch(query, refresh=False, view=None, verbose=False, download=True, integrity_fields=None, integrity_action='raise', subscriber=True, **kwds) ###
q="AUTHOR-NAME(Paraboschi, S.)";
sc=ScopusSearch(query=q, refresh=False, view="COMPLETE", verbose=False, download=True, integrity_fields=None, integrity_action='raise', subscriber=True);

for numero in range(5):
    print("******************************************************************************************************************************************************");
print("*****************************************************************INIZIO DEL PROGRAMMA*****************************************************************");
for numero in range(5):
    print("******************************************************************************************************************************************************");

# PREVIEW
#print(sc);

print("Search Results (\""+q+"\"):\nNumber of Results: "+str(sc.get_results_size()));
print(pd.DataFrame(sc.results));

# DATI API
#print("\n\nAPI:\nRimanenti: "+sc.get_key_remaining_quota()+"\nRefresh: "+sc.get_key_reset_time());