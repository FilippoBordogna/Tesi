from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


from gbliometrics.models import Agroup, CustomUser
from gbliometrics.serializers import AgroupSerializer

#######################################################################################################
########################################### SEZIONE COMUNE ############################################
#######################################################################################################

def createUser(username, email, password):
    '''
        Funzione che crea un utente
    '''
    
    user = CustomUser.objects.create(username=username, email=email)
    user.set_password(password)
    user.save()
    return user

def createGroup(user, name):
    '''
        Funzione che crea un gruppo
    '''
    
    creation = last_update = timezone.now()
    group = Agroup.objects.create(user=user, name=name, creation=creation, last_update=last_update)
    group.save()
    return group

#######################################################################################################
########################################### TEST API GRUPPI ###########################################
#######################################################################################################

class GroupsAPITest(TestCase):
    '''
        Classe contente i casi di test delle API riguardanti i gruppi
    '''
    
    def setUp(self):
        '''
            Funzione che crea gli oggetti nel DB di test
        '''
        # Creazione utenti
        user1 = createUser(username="user-test", email="test@gmail.com", password="test")
        user2 = createUser(username="user-test2", email="test2@gmail.com", password="test")
        
        # Creazione gruppi
        group1 = createGroup(user1, "test-group") 
        group2 = createGroup(user2, "test-group")
        group3 = createGroup(user1, "test-group2")
    
    def test_groupApiOverview(self):
        '''
            Test riguardante l'API groupAPIOverview:
            Mi aspetto un codice 200 in ogni caso
        '''
        
        response = self.client.get(reverse('api:group-api-overview'))
        self.assertEqual(response.status_code, 200)

    def test_groupList(self):
        '''
            Test riguardante l'API groupList:
            Mi aspetto un codice 500 se non loggato
            Se loggato come user 1 mi aspetto di ricevere solo il gruppo 1 e non il gruppo 2
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.get(reverse('api:groups-list'))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        user2 = CustomUser.objects.get(email="test2@gmail.com")
        
        # Gruppi
        group1 = Agroup.objects.get(name="test-group", user=user1)
        group2 = Agroup.objects.get(user=user2, name="test-group")
        
        response = self.client.get(reverse('api:groups-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(AgroupSerializer(group1).data, response.json())
        self.assertNotIn(AgroupSerializer(group2).data, response.json())
        
    def test_groupDetails(self):
        '''
            Test riguardante l'API groupDetails:
            Mi aspetto di ricevere un codice 500 se:
                - Non loggato
                - Provo a richiedere i dettagli di un gruppo non esistente o non di mia proprietà 
            Mi aspetto di ricevere un codice 200 se richiedo i dettagli di un gruppo di mia proprietà
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.get(reverse('api:group-details', kwargs={'groupId':1}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        user2 = CustomUser.objects.get(email="test2@gmail.com")
        
        # Gruppi
        group1 = Agroup.objects.get(name="test-group", user=user1)
        group2 = Agroup.objects.get(name="test-group", user=user2)
        
        # Richiesta corretta
        response = self.client.get(reverse('api:group-details', kwargs={'groupId':group1.id}))
        self.assertEqual(response.status_code, 200)
        
        # Richiesta di un gruppo non di proprietà dell'utente
        response = self.client.get(reverse('api:group-details', kwargs={'groupId':group2.id}))
        self.assertEqual(response.status_code, 500)
        self.assertIn('inesistente o non di tua proprieta',response.json()['message'])
        
        # Richiesta di un gruppo non esistente
        response = self.client.get(reverse('api:group-details', kwargs={'groupId':1000}))
        self.assertEqual(response.status_code, 500)
        self.assertIn('inesistente o non di tua proprieta',response.json()['message'])
        
        
    def test_groupCreate(self):
        '''
            Test riguardante l'API groupDetails:
            Mi aspetto di ricevere un codice 500:
                - Se non loggato
                - Se creo un gruppo con un nome già presente nel DB
                - Se il formato dei dati passati tramite post non è corretto
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.post(reverse('api:group-create'))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Creazione corretta
        response = self.client.post(reverse('api:group-create'), {"name": "Prova"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Agroup.objects.filter(name="Prova", user=user1).exists())
        
        # Creazione di un duplicato
        response = self.client.post(reverse('api:group-create'), {"name": "Prova"}, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertIn("già presente",response.json()['message'])
        self.assertTrue(Agroup.objects.filter(name="Prova").count()==1)
        
        # JSON passato nella POST errato (mancanza del campo name obbligatorio)
        response = self.client.post(reverse('api:group-create'), {"name2": "Prova"}, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertIn("name è obbligatorio",response.json()['message'])
        
    def test_groupUpdate(self):
        '''
            Test riguardante l'API groupUpdate:
            Mi aspetto di ricevere un codice 500 se:
                - Non loggato
                - Cerco di modificare un gruppo non di mia proprietà o non esistente
                - Il gruppo che modifico porta ad un duplicato
            Mi aspetto di riceve un codice 200 se modifico un gruppo di mia proprietà e la modifica non crea duplicati
            
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.post(reverse('api:group-update', kwargs={'groupId':1}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        user2 = CustomUser.objects.get(email="test2@gmail.com")
        
        # Gruppi
        group1 = Agroup.objects.get(name="test-group", user=user1)
        group2 = Agroup.objects.get(name="test-group", user=user2)
        group3 = Agroup.objects.get(name="test-group2", user=user1)
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine

        # Modifica corretta
        response = self.client.post(reverse('api:group-update', kwargs={'groupId': group1.id}), {"name": "updated-group"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Agroup.objects.filter(name="updated-group", user=user1).exists())
        
        # Modifica non autorizzata
        response = self.client.post(reverse('api:group-update', kwargs={'groupId': group2.id}), {"name": "updated-group"}, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertIn('non di tua proprieta',response.json()['message'])
        self.assertTrue(Agroup.objects.filter(name="test-group").exists())
        
        # Modifica di un gruppo inesistente
        response = self.client.post(reverse('api:group-update', kwargs={'groupId': 1000}), {"name": "updated-group"}, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertIn('gruppo inesistente',response.json()['message'])
        
        # Modifica che crea duplicato
        response = self.client.post(reverse('api:group-update', kwargs={'groupId': group3.id}), {"name": "updated-group"}, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertIn('già presente',response.json()['message'])
        self.assertTrue(Agroup.objects.filter(name="updated-group", user=user1).count() == 1)
        
    def test_groupDelete(self):
        '''
            Test riguardante l'API groupDelete:
            Mi aspetto di ricevere un codice 500 se:
                - Non loggato
                - Se provo ad eliminare un gruppo di cui non sono proprietario o inesistente
            Mi aspetto di ricevere un codice 200 se elimino un gruppo di mia proprietà
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.delete(reverse('api:group-delete', kwargs={'groupId':1}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        user2 = CustomUser.objects.get(email="test2@gmail.com")
        
        # Gruppi
        group3 = Agroup.objects.get(name="test-group2", user=user1)
        group2 = Agroup.objects.get(name="test-group", user=user2)
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Cancellazione corretta
        response = self.client.delete(reverse('api:group-delete', kwargs={'groupId':group3.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Agroup.objects.filter(id=group3.id).exists())
        
        # Cancellazione di un gruppo di cui non sono proprietario
        response = self.client.delete(reverse('api:group-delete', kwargs={'groupId':group2.id}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("non di tua proprieta", response.json()['message'])
        self.assertTrue(Agroup.objects.filter(name="test-group", user=user2).exists())
        
        # Cancellazione di un gruppo non esistente
        response = self.client.delete(reverse('api:group-delete', kwargs={'groupId':1000}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("gruppo inesistente", response.json()['message'])
        
    def test_groupAddAuthor(self):
        '''
            Test riguardante l'API groupAddAuthor:
            Mi aspetto di ricevere un codice 500 se:
                - Non loggato
                - Provo ad aggiungere un autore già presente nel gruppo o inesistente
                - Provo ad aggiungere un autore ad un gruppo di cui non sono proprietario o inesistente
            Mi aspetto di ricevere un codice 200 se aggiungo un autore che non è già presente nel gruppo
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.post(reverse('api:group-add-author', kwargs={'groupId':1, 'authorScopusId':1}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        user2 = CustomUser.objects.get(email="test2@gmail.com")
        
        # Gruppi
        group1 = Agroup.objects.get(name="test-group", user=user1)
        group2 = Agroup.objects.get(name="test-group", user=user2)
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Aggiunta corretta
        response = self.client.post(reverse('api:group-add-author', kwargs={'groupId':group1.id, 'authorScopusId':6603694127}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(group1.authors.count() == 1)
        
        # Aggiunta duplicata
        response = self.client.post(reverse('api:group-add-author', kwargs={'groupId':group1.id, 'authorScopusId':6603694127}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("già presente", response.json()['message'])
        self.assertTrue(group1.authors.count() == 1)
        
        # Aggiunta di un autore non esistente
        response = self.client.post(reverse('api:group-add-author', kwargs={'groupId':group1.id, 'authorScopusId':66036941}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("Non esiste un autore", response.json()['message'])
        self.assertFalse(group1.authors.filter(scopusId=66036941).exists())
        
        # Aggiunta di un autore ad un gruppo di cui non sono proprietario
        response = self.client.post(reverse('api:group-add-author', kwargs={'groupId':group2.id, 'authorScopusId':6603694127}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("non di tua proprieta", response.json()['message'])
        self.assertFalse(group2.authors.filter(scopusId=6603694127).exists())
        
        # Aggiunta di un autore ad un gruppo non esistente
        response = self.client.post(reverse('api:group-add-author', kwargs={'groupId':1000, 'authorScopusId':6603694127}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("gruppo inesistente", response.json()['message'])
        
    def test_groupAddMultipleAuhtors(self):
        '''
            Test riguardante l'API groupAddMultipleAuhtors:
            Mi aspetto di ricevere un codice 500 se:
                - Non loggato
                - Tutti gli autori specificati non esistono o sono già presenti
                - Provo ad aggiungere autori ad un gruppo di cui non sono proprietario o inesistente
            Mi aspetto di ricevere un codice 200 se aggiungo almeno un autore che non è già presente nel gruppo
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.post(reverse('api:group-add-multiple-authors', kwargs={'groupId':1}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        user2 = CustomUser.objects.get(email="test2@gmail.com")
        
        # Gruppi
        group1 = Agroup.objects.get(name="test-group", user=user1)
        group2 = Agroup.objects.get(name="test-group", user=user2)
        
        # Contenuti JSON da passare
        correct_add = {
                        "scopusIds": [
                            6701743648,
                            14066377200,
                            55897877400
                        ]
                    }
        semi_correct_add = {
                                "scopusIds": [
                                    24483009100,
                                    20,
                                    10
                                ]
                            }
        wrong_add = {
                                "scopusIds": [
                                    30,
                                    20,
                                    10
                                ]
                            }
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Aggiunta corretta
        response = self.client.post(reverse('api:group-add-multiple-authors', kwargs={'groupId':group1.id}), correct_add, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['added_authors_number'] == 3)
        self.assertTrue(group1.authors.filter(scopusId=6701743648).exists())
        
        # Aggiunta con 2 errori su 3 autori
        response = self.client.post(reverse('api:group-add-multiple-authors', kwargs={'groupId':group1.id}), semi_correct_add, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['added_authors_number'] == 1)
        self.assertTrue(group1.authors.filter(scopusId=24483009100).exists())
        
        # Aggiunta errata
        response = self.client.post(reverse('api:group-add-multiple-authors', kwargs={'groupId':group1.id}), wrong_add, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertIn("Tutti gli autori specificati sono inesistenti", response.json()['message'])
        
        # Aggiunta duplicata (Tutti gli autori sono già presenti)
        response = self.client.post(reverse('api:group-add-multiple-authors', kwargs={'groupId':group1.id}), correct_add, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertIn("già presenti nel gruppo", response.json()['message'])
        self.assertTrue(group1.authors.filter(scopusId=6701743648).count() == 1)
        
        # Aggiunta ad un gruppo non di cui non sono proprietario
        response = self.client.post(reverse('api:group-add-multiple-authors', kwargs={'groupId':group2.id}), correct_add, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertIn("non di tua proprieta", response.json()['message'])
        self.assertFalse(group2.authors.filter(scopusId=6701743648).exists())
        
        # Aggiunta ad un gruppo inesistente
        response = self.client.post(reverse('api:group-add-multiple-authors', kwargs={'groupId':1000}), correct_add, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertIn("gruppo inesistente", response.json()['message'])
        
    def test_groupRemoveAuhtor(self):
        '''
            Test riguardante l'API groupAddMultipleAuhtors:
            Mi aspetto di ricevere un codice 500 se:
                - Non loggato 
                - Provo ad eliminare un autore non presente nel gruppo
                - Provo ad eliminare un autore da un gruppo di cui non sono proprietario o inesistente
            Mi aspetto di ricevere un codice 200 se elimino un autore che è presente nel gruppo
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.post(reverse('api:group-remove-author', kwargs={'groupId':1, 'authorId':1}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        user2 = CustomUser.objects.get(email="test2@gmail.com")
        
        # Gruppi
        group1 = Agroup.objects.get(name="test-group", user=user1)
        group2 = Agroup.objects.get(name="test-group", user=user2)
        
        # Mi loggo come user2
        logged_in = self.client.login(email="test2@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Aggiunta autori
        response = self.client.post(reverse('api:group-add-author', kwargs={'groupId':group2.id, 'authorScopusId':6603694127}))
        
        # Mi loggo come user1
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        response = self.client.post(reverse('api:group-add-author', kwargs={'groupId':group1.id, 'authorScopusId':6603694127}))
        id = group1.authors.first().id
        
        # Eliminazione corretta
        response = self.client.post(reverse('api:group-remove-author', kwargs={'groupId':group1.id, 'authorId':id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(group1.authors.filter(scopusId=6603694127).exists())
        
        # Eliminazione di un autore non presente nel gruppo
        response = self.client.post(reverse('api:group-remove-author', kwargs={'groupId':group1.id, 'authorId':id}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("non è presente nel gruppo", response.json()['message'])
        
        # Eliminazione di un autore da un gruppo di cui non sono proprietario
        response = self.client.post(reverse('api:group-remove-author', kwargs={'groupId':group2.id, 'authorId':id}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("non di tua proprieta", response.json()['message'])
        #self.assertTrue(group2.authors.filter(scopusId=6603694127).exists())
        
        # Eliminazione di un autore da un gruppo inesistente
        response = self.client.post(reverse('api:group-remove-author', kwargs={'groupId':group2.id, 'authorId':id}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("gruppo inesistente", response.json()['message'])