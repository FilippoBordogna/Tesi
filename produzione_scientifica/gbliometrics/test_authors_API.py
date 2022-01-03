from django.test import TestCase
from django.urls.base import reverse

from gbliometrics.models import Author, CustomUser

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

#######################################################################################################
########################################### TEST API AUTORI ###########################################
#######################################################################################################

class AuthorsAPITest(TestCase):
    '''
        Classe contente i casi di test delle API riguardanti gli autori
    '''
    
    def setUp(self):
        '''
            Funzione che crea gli oggetti nel DB di test
        '''
        
        # Creazione utenti
        user1 = createUser(username="user-test", email="test@gmail.com", password="test")
    
    def test_authorsAPIOverview(self):
        '''
            Test riguardante l'API affiliationsAPIOverview:
            Mi aspetto un codice 200 in ogni caso
        '''
        
        response = self.client.get(reverse('api:authors-api-overview'))
        self.assertEqual(response.status_code, 200)
        
        # Richiesta avendo effettuato il login
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        response = self.client.get(reverse('api:authors-api-overview'))
        self.assertEqual(response.status_code, 200)
        
    def test_authorDetails(self):
        '''
            Test riguardante l'API authorDetails:
            Mi aspetto un codice 200 se chiedo i dettagli di un autore esistente
            Mi aspetto un codice 500 se chiedo i dettagli di un autore inesistente
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.get(reverse('api:author-details', kwargs={'authorScopusId':6603694127}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        scopusId1 = 6603694127
        scopusId2 = 100 # Non esiste un autore con questo id
        
        # Richiesta di dettagli di un autore non presente nel DB da Scopus
        response = self.client.get(reverse('api:author-details', kwargs={'authorScopusId':scopusId1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(scopusId1, response.json()['scopusId'])
        self.assertTrue(Author.objects.filter(scopusId=scopusId1).exists())
        
        # Richiesta di dettagli di un autore presente nel DB da Scopus
        response = self.client.get(reverse('api:author-details', kwargs={'authorScopusId':scopusId1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(scopusId1, response.json()['scopusId'])
        self.assertTrue(Author.objects.filter(scopusId=scopusId1).count() == 1)
        
        # Richiesta di dettagli di un autore non presente nel DB da Scopus
        response = self.client.get(reverse('api:author-details', kwargs={'authorScopusId':scopusId2}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("Non esiste", response.json()['message'])
        self.assertFalse(Author.objects.filter(scopusId=scopusId2).exists())
        
    def test_authorDetailsDB(self):
        '''
            Test riguardante l'API authorDetailsDB:
            Mi aspetto un codice 200 se chiedo i dettagli di un autore presente nel DB
            Mi aspetto un codice 500 se chiedo i dettagli di un autore non presente nel DB
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.get(reverse('api:author-details-db', kwargs={'authorId':1}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Inserimento autore
        scopusId1 = 6603694127
        response = self.client.get(reverse('api:author-details', kwargs={'authorScopusId':scopusId1}))
        self.assertEqual(response.status_code, 200)
        
        id = Author.objects.get(scopusId=scopusId1).id
        id2 = 1000
        
        # Richiesta di dettagli di un autore presente nel DB da Scopus
        response = self.client.get(reverse('api:author-details-db', kwargs={'authorId':id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(id, response.json()['id'])
        self.assertTrue(Author.objects.filter(id=id).exists())
        
        # Richiesta di dettagli di un autore non presente nel DB da Scopus
        response = self.client.get(reverse('api:author-details-db', kwargs={'authorId':id2}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("Non esiste", response.json()['message'])
        self.assertFalse(Author.objects.filter(id=id2).exists())