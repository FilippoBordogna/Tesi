from numpy import array
import pandas as pd
from pybliometrics.scopus import SubjectClassifications
from pybliometrics.scopus.utils import config
import json

# print("My API-Key: "+config['Authentication']['APIKey']+"\nMy Token: "+config['Authentication']['InstToken'])

### SubjectClassifications(query, refresh=False, fields=None, **kwds) ###
q={"abbrev":"COMP"}; # Computer science
qs=json.dumps(q, separators=(',', ':'));
f=["code", "abbrev", "description", "detail"]; # Campi da visualizzare
sc=SubjectClassifications(query=q, refresh=False, fields=f);

for numero in range(5):
    print("******************************************************************************************************************************************************");
print("*****************************************************************INIZIO DEL PROGRAMMA*****************************************************************");
for numero in range(5):
    print("******************************************************************************************************************************************************");

print("Search Results ("+qs+"):\nNumber of Results: "+str(sc.get_results_size()));
print(pd.DataFrame(sc.results));

# DATI API
#print("\n\nAPI:\nRimanenti: "+sc.get_key_remaining_quota()+"\nRefresh: "+sc.get_key_reset_time());