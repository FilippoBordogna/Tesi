from typing import Iterable
import pandas as pd
from pybliometrics.scopus import AbstractRetrieval
from pybliometrics.scopus.utils import config

# print("My API-Key: "+config['Authentication']['APIKey']+"\nMy Token: "+config['Authentication']['InstToken'])

### AbstractRetrieval(identifier=None, refresh=False, view='META_ABS', id_type=None, **kwds) ###
ab=AbstractRetrieval(identifier="85113200085", refresh=False, view="FULL", id_type="scopus_id");

for numero in range(5):
    print("******************************************************************************************************************************************************");
print("*****************************************************************INIZIO DEL PROGRAMMA*****************************************************************");
for numero in range(5):
    print("******************************************************************************************************************************************************");
# DESCRIZIONE
print("\nDOCUMENT DESCRIPTION:");
if(ab.description):
    print(ab.description);
else:
    print(ab.abstract);

# PAROLE CHIAVE
print("\nKEY WORDS("+str(len(ab.authkeywords))+"):");
for a in ab.authkeywords:
    print("- "+a);
    
# INDICI
print("\nINDEXES:")
for i in ab.idxterms:
    print("- "+i);
    
# MATERIE
print("\nSUBJECT:\n- AREA:")
for s in ab.subject_areas:
    print("\t"+s.area+"("+s.abbreviation+" - "+str(s.code)+")");
print("- TYPE DESCRIPTION: "+ab.subtypedescription+"("+ab.subtype+")");
    
# DATI
print ("\nDATA:\n- DOI: "+ab.doi+"\n- EID: "+ab.eid);
if(ab.pii):
    print("- PII: "+ab.pii);
if(ab.issn):
    print("- ISSN: "+ab.issn);
if(ab.isbn):
    print("- ISBN: ",end="");
    for i in ab.isbn:
        print(str(i)+" ; ");
if(ab.identifier):
    print("- SCOPUS_ID: "+str(ab.identifier));
print("- PUBLICATION NAME: "+ab.publicationName);
print("- PUBLISHER: "+ab.publisher);
if(ab.publisheraddress):
    print("- PUBLISHER ADDRESS: "+ab.publisheraddress);
if(ab.pubmed_id):
    print("- PUBMED_ID: "+ab.pubmed_id);
print("- REFERENCE(S)("+str(ab.refcount)+"):");
for r in ab.references:
    print("\t"+r.position+") "+r.sourcetitle+"("+r.publicationyear+")");
    if(r.id):
        print("\t\tID: "+r.id);
    if(r.doi):
        print("\t\tDOI: "+r.doi);
    if(r.title):
        print("\t\tTITLE: "+r.title);
    if(r.authors):
        print("\t\tAUTHOR(S): "+r.authors);
    if(r.authors_auid):
        print("\t\tAUTHOR(S) AUID: "+r.authors_auid);
    if(r.authors_affiliationid):
        print("\t\tAUTHOR(S) AFFILIATION ID: "+r.authors_affiliationid)
    if(r.volume):
        print("\t\tVOLUME: "+r.volume);
if(ab.pageRange):
    print("- PAGE RANGE: "+ab.pageRange);
elif(ab.startingPage and ab.endingPage):
    print("- PAGE RANGE: "+ab.startingPage+"-"+ab.endingPage)
elif(ab.endingPage):
    print("- NUMBER OF PAGES: "+ab.endingPage);
print("- LANGUAGE: "+ab.language)
print("- TITLE: "+ab.title);
print("- URL: "+ab.url);
if(ab.volume):
    print("- VOLUME: "+ab.volume);
print("- WEBSITE: "+ab.website);

# LINKS
print("\nLINKS:")       
print("- SCOPUS: "+ab.scopus_link);
print("- SELF: "+ab.self_link);

# AUTORI
print("\nAUTHOR(S)("+str(len(ab.authorgroup))+"):");
for a in ab.authorgroup:
    print("- "+a.given_name+" "+a.surname+"("+str(a.auid)+")\n\tIndexed Name: "+a.indexed_name)
    if(a.city):
        print("\tOrganization: "+a.organization+" "+a.city+"("+str(a.affiliation_id)+")");
    else:
        print("\tOrganization: "+a.organization+"("+str(a.affiliation_id)+")");
    print("\tCountry: "+a.country);
# print(ab.authors)

# AFFILIAZIONI
print("AFFILIATION(S)("+str(len(ab.affiliation))+"):");
for a in ab.affiliation:
    print("- "+a.name+"\n\tID: "+str(a.id)+"\n\tCity: "+a.city+"("+a.country+")");
    
# print(ab.aggregationType)

# FONDAZIONI
print("\nFUNDING(S):\n- AGENCY:")
for f in ab.funding:
    print("\t"+f.agency+"("+f.acronym+")");  
#print("- TEXT:"+ab.funding_text)

# SORGENTE
print("\nSOURCE:")
print("- ID: "+str(ab.source_id));
print("- TITLE ABBREVIATION: "+ab.sourcetitle_abbreviation);

# CITAZIONI
print("\nNUMBER OF CITATIONS: "+str(ab.citedby_count)+" ("+ab.citedby_link+")");

#print(ab.chemicals)

# CONFERENZA
"""
print("\nCONFERENCE:\n\t"+ab.confname+"("+str(ab.confcode)+")");
date="";
for d in ab.confdate:
    date+=str(d[2])+"/"+str(d[1])+"/"+str(d[0])+" ; ";
print("\tDate: "+date);
if(ab.conflocation):
    print("\tLocation: "+ab.conflocation+"\n\tSponsor(s)");

if(isinstance(ab.confsponsor, Iterable)):
    for s in ab.confsponsor:
        print("\t\t"+s); """

# CONTRIBUENTI
# print(ab.contributor_group)

# CORRISPONDENZE
# print(ab.correspondence)
    
#print(ab.issueIdentifier);
#print(ab.issuetitle);

#print(ab.openaccess)
#print(ab.openaccessFlag)

#print(ab.sequencebank);

#print(ab.srctype);

#print(ab.startingPage);

print(ab.get_key_remaining_quota())
print(ab.get_key_reset_time())

#print(pd.DataFrame(ab.authorgroup))