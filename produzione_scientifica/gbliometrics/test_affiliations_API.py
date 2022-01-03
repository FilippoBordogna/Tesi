from django.test import TestCase
from django.urls.base import reverse

from gbliometrics.models import Affiliation, CustomUser

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
######################################## TEST API AFFILIAZIONI ########################################
#######################################################################################################

class AffiliationsAPITest(TestCase):
    '''
        Classe contente i casi di test delle API riguardanti le affiliazioni
    '''
    
    def setUp(self):
        '''
            Funzione che crea gli oggetti nel DB di test
        '''
        
        # Creazione utenti
        user1 = createUser(username="user-test", email="test@gmail.com", password="test")
    
    def test_affiliationsAPIOverview(self):
        '''
            Test riguardante l'API affiliationsAPIOverview:
            Mi aspetto un codice 200 in ogni caso
        '''
        
        response = self.client.get(reverse('api:affiliations-api-overview'))
        self.assertEqual(response.status_code, 200)
        
        # Richiesta avendo effettuato il login
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        response = self.client.get(reverse('api:affiliations-api-overview'))
        self.assertEqual(response.status_code, 200)
        
    def test_affiliationDetails(self):
        '''
            Test riguardante l'API affiliationDetails:
            Mi aspetto un codice 200 se chiedo i dettagli di un'affiliazione esistente
            Mi aspetto un codice 500 se chiedo i dettagli di un'affiliazione inesistente
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.get(reverse('api:affiliation-details', kwargs={'affiliationScopusId':60005254}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        scopusId1 = 60005254
        scopusId2 = 60011178
        scopusId3 = 100 # Non esiste un'affiliazione con questo id
        
        # Richiesta di dettagli di una affiliazione non presente nel DB da Scopus
        response = self.client.get(reverse('api:affiliation-details-refresh', kwargs={'affiliationScopusId':scopusId1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(scopusId1, response.json()['scopusId'])
        self.assertTrue(Affiliation.objects.filter(scopusId=scopusId1).exists())
        
        # Richiesta di dettagli di una affiliazione presente nel DB da Scopus
        response = self.client.get(reverse('api:affiliation-details-refresh', kwargs={'affiliationScopusId':scopusId1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(scopusId1, response.json()['scopusId'])
        self.assertTrue(Affiliation.objects.filter(scopusId=scopusId1).count() == 1)
        
        # Richiesta di dettagli dal DB di una affiliazione non presente nel DB
        response = self.client.get(reverse('api:affiliation-details', kwargs={'affiliationScopusId':scopusId2}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(scopusId2, response.json()['scopusId'])
        self.assertTrue(Affiliation.objects.filter(scopusId=scopusId2).exists())
        
        # Richiesta di dettagli dal DB di una affiliazione presente nel DB
        response = self.client.get(reverse('api:affiliation-details', kwargs={'affiliationScopusId':scopusId2}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(scopusId2, response.json()['scopusId'])
        self.assertTrue(Affiliation.objects.filter(scopusId=scopusId2).count() == 1)
        
        # Richiesta di dettagli di una affiliazione non esistente da Scopus
        response = self.client.get(reverse('api:affiliation-details-refresh', kwargs={'affiliationScopusId':scopusId3}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("Non esiste",response.json()['message'])
        self.assertFalse(Affiliation.objects.filter(scopusId=scopusId3).exists())
        
        # Richiesta di dettagli di una affiliazione non esistente dal DB
        response = self.client.get(reverse('api:affiliation-details', kwargs={'affiliationScopusId':scopusId3}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("Non esiste",response.json()['message'])
        self.assertFalse(Affiliation.objects.filter(scopusId=scopusId3).exists()) 