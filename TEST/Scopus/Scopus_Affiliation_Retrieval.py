from datetime import datetime
import pandas as pd
from pybliometrics.scopus import AffiliationRetrieval
from pybliometrics.scopus.utils import config

# print("My API-Key: "+config['Authentication']['APIKey']+"\nMy Token: "+config['Authentication']['InstToken'])

### AffiliationRetrieval(aff_id, refresh=False, view='STANDARD', **kwds) ###
ar=AffiliationRetrieval(aff_id="60028218", refresh=False, view="STANDARD");

for numero in range(5):
    print("******************************************************************************************************************************************************");
print("*****************************************************************INIZIO DEL PROGRAMMA*****************************************************************");
for numero in range(5):
    print("******************************************************************************************************************************************************");

# INFORMAZIONI GENERALI (TUTTE UNITE)
# print("Informazioni generali: "+ar);

# DATI PRINCIPALI
print("PRINCIPAL DATA:")
print("- EID: "+ar.eid);
print("- Identifier: "+str(ar.identifier));
print("- Name: "+ar.affiliation_name);
print("- Address: "+ar.address);
print("- City: "+ar.city+"("+ar.state+")");
print("- Country: "+ar.country);
print("- Postal Code: "+ar.postal_code);
print("- Author count: "+str(ar.author_count));
print("- Document count: "+str(ar.document_count));
#print("- ORG domain: "+ar.org_domain);
print("- ORG type: "+ar.org_type);

# LINKS
print("\nLINKS: ")
print("- ORG URL: "+ar.org_URL); # SITO AFFILIAZIONE
print("- Scopus link: "+ar.scopus_affiliation_link); # PAGINA SCOPUS DELL'AFFILIAZIONE
print("- Self link: "+ar.self_link); # PAGINA CHE REINDIRIZZA A SE STESSI
#print("URL: "+ar.url);
print("- Search link: "+ar.search_link); # PAGINA SCOPUS DELL'AFFILIAZIONE RICAVATA CON RICERCA (QUERY)

# ALTRI DATI
print("\nOTHER DATA:")
print("- Sort Name: "+ar.sort_name);
print("- Variant(s): "); # VARIANTI: COPPIE (NOME, N° DOCUMENTI)
print(pd.DataFrame(ar.name_variants));
date=datetime(ar.date_created[0],ar.date_created[1],ar.date_created[2]);
print("- Record date of creation: "+str(date)); # DATA DI CREAZIONE DEL RECORD

# DATI API
#print("\n\nAPI:\nRimanenti: "+ar.get_key_remaining_quota()+"\nRefresh: "+ar.get_key_reset_time());