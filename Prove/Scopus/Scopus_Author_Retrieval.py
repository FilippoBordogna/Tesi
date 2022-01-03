import pandas as pd
from datetime import datetime
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus.utils import config

# print("My API-Key: "+config['Authentication']['APIKey']+"\nMy Token: "+config['Authentication']['InstToken'])

### AuthorRetrieval(author_id, refresh=False, view='ENHANCED')
ar=AuthorRetrieval(author_id="6603694127", refresh=False, view="ENHANCED");

for numero in range(5):
    print("******************************************************************************************************************************************************");
print("*****************************************************************INIZIO DEL PROGRAMMA*****************************************************************");
for numero in range(5):
    print("******************************************************************************************************************************************************");

# INFORMAZIONI GENERALI
#print(ar);

# AFFILIAZIONI CORRENTI E PASSATE
print("AFFILIATION(S):\n- CURRENT:");
print(pd.DataFrame(ar.affiliation_current));
print("- HISTORY:");
print(pd.DataFrame(ar.affiliation_history));

# ALIAS (PROFILO "FUSO")
print("\nALIAS:");
print(pd.DataFrame(ar.alias));

# CITAZIONI
print("\nCITATION COUNT: "+str(ar.citation_count)+"\nCITED BY COUNT: "+str(ar.cited_by_count));

# COAUTORI
print("\nCOAUTHOR(S):\n- COUNT: "+str(ar.coauthor_count)+"\n- COAUTHOR PAGE LINK: "+ar.coauthor_link);

# DATA DI CREAZIONE DEL RECORD
date=datetime(ar.date_created[0], ar.date_created[1], ar.date_created[2]);
print("\nDATE CREATED: "+str(date));

# DATI
print("\nDATA:\n- EID: "+ar.eid+"\n- ID: "+str(ar.identifier)+"\n- ORCID: "+ar.orcid+"\n- HISTORICAL IDENTIFIER");
print(pd.DataFrame(ar.historical_identifier));
print("- GIVEN FULL NAME: "+ar.given_name+" "+ar.surname+"\n- INDEXED NAME: "+ar.indexed_name+"\n- INITIALS: "+ar.initials+" "+ar.surname+"\n- NAME VARIANTS:");
print(pd.DataFrame(ar.name_variants)); 
print("- DOCUMENT COUNT: "+str(ar.document_count)); # CONTATORE DEI DOCUMENTI PRODOTTI (ESCLUSI NOTE E CAPITOLI DI LIBRI)
print("- PUBBLICATION RANGE: "+str(ar.publication_range[0])+" - "+str(ar.publication_range[1])+"\n- H-INDEX: "+str(ar.h_index));
print("- LINK(S):\n\tSCOPUS AUTHOR: "+ar.scopus_author_link+"\n\tSEARCH: "+ar.search_link+"\n\tSELF: "+ar.self_link+"\n\tAUTHOR API PAGE: "+ar.url);
print("- AUTHOR STATUS: "+ar.status);

# CLASSIFICAZIONE MEDIANTE GRUPPI
print("\nCLASSIFICATION GROUP:");
print(pd.DataFrame(ar.classificationgroup)); # (ID, N° DOCUMENTI)

# MATERIE DI COMPETENZA
print("SUBJECT AREAS:");
print(pd.DataFrame(ar.subject_areas));

# COAUTORI (?)
#print(ar.get_coauthors());

# TUTTI I DOCUMENTI
#print(ar.get_documents());
#print(ar.get_document_eids());

# DATI API
# print("\n\nAPI:\nRimanenti: "+ar.get_key_remaining_quota()+"\nRefresh: "+ar.get_key_reset_time());