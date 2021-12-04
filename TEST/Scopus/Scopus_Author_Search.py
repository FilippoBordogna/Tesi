import pandas as pd
from datetime import datetime
from pybliometrics.scopus import AuthorSearch
from pybliometrics.scopus.utils import config

#print("My API-Key: "+config['Authentication']['APIKey']+"\nMy Token: "+config['Authentication']['InstToken'])

### AuthorSearch(query, refresh=False, verbose=False, download=True, integrity_fields=None, integrity_action='raise', count=200 (DEPRECATED), **kwds)
q="af-id(60005254)";
aus=AuthorSearch(query=q, refresh=False, download=True, integrity_fields=None, integrity_action='raise');

for numero in range(5):
    print("******************************************************************************************************************************************************");
print("*****************************************************************INIZIO DEL PROGRAMMA*****************************************************************");
for numero in range(5):
    print("******************************************************************************************************************************************************");

print("Author Search Results (\""+q+"\"):\nNumber of Results: "+str(aus.get_results_size()));
print(pd.DataFrame(aus.authors));

# DATI API
#print("\n\nAPI:\nRimanenti: "+aus.get_key_remaining_quota()+"\nRefresh: "+aus.get_key_reset_time());