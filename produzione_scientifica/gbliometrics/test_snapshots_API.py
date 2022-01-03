from datetime import date, datetime
import os
from django.core.files.base import ContentFile
from django.utils import timezone
from django.test import TestCase
from django.urls.base import reverse
import json

from gbliometrics.models import Agroup, CustomUser, Snapshot
from gbliometrics.serializers import SnapshotSerializer

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

def createSnapshot(user, title, filepath):
    '''
        Funzione che crea uno snapshot
    '''
    
    snapshot = Snapshot(user=user, title=title, creation=timezone.now()) # Creazione dello snapshot
    snapshot.informations=filepath
    snapshot.save() # Salvataggio dello snapshot
    return snapshot

def createFile3():
    '''
        Funzione che crea il file snapshots/user_0/2021-12-14_03-31-03_02_prova3.json
    '''
    
    if (os.path.isfile("snapshots/user_0/2021-12-14_03-31-03_02_prova3.json")):
        f = open("snapshots/user_0/2021-12-14_03-31-03_02_prova3.json", "w")
    else:
        f = open("snapshots/user_0/2021-12-14_03-31-03_02_prova3.json", "x")
    f2 = open("snapshots/user_0/2021-12-14_03-31-03_02_prova2.json", "r")
    f.write(f2.read())
    f.close

#######################################################################################################
######################################## TEST API AFFILIAZIONI ########################################
#######################################################################################################

class SnapshotsAPITest(TestCase):
    '''
        Classe contente i casi di test delle API riguardanti gli snapshot
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
        
        # Aggiunta autori ai gruppi
        auth_set1 = {
                        "scopusIds": [
                            6603694127,
                            56875463900,
                            8680609500
                        ]
                    }
        
        # Login come user1
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        response = self.client.post(reverse('api:group-add-multiple-authors', kwargs={'groupId':group1.id}), auth_set1, content_type="application/json")
        
        # Login come user2
        logged_in = self.client.login(email="test2@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        response = self.client.post(reverse('api:group-add-multiple-authors', kwargs={'groupId':group2.id}), auth_set1, content_type="application/json")
        self.client.logout()
           
        snapshot1 = createSnapshot(user1, "snapshot-test", "snapshots/user_0/2021-12-14_03-31-03_02_prova1.json")
        snapshot2 = createSnapshot(user2, "snapshot-test2", "snapshots/user_0/2021-12-14_03-31-03_02_prova2.json")
        snapshot3 = createSnapshot(user1, "snapshot-test2", "snapshots/user_0/2021-12-14_03-31-03_02_prova3.json")
        
        createFile3()
        
    def test_snapshotsAPIOverview(self):
        '''
            Test riguardante l'API snapshotsAPIOverview:
            Mi aspetto un codice 200 in ogni caso
        '''
                
        response = self.client.get(reverse('api:snapshots-api-overview'))
        self.assertEqual(response.status_code, 200)
        
        # Richiesta avendo effettuato il login
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        response = self.client.get(reverse('api:snapshots-api-overview'))
        self.assertEqual(response.status_code, 200)
        
    def test_snapshotsList(self):
        '''
            Test riguardante l'API snapshotsList:
            Mi aspetto un codice 500 se non loggato
            Mi aspetto un codice 200 se loggato
            Se loggato come user 1 mi aspetto di ricevere solo lo snapshot1 e non lo snapshot 2
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        
        response = self.client.get(reverse('api:snapshots-list'))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        user2 = CustomUser.objects.get(email="test2@gmail.com")
        
        # Snapshot
        
        snapshot1 = Snapshot.objects.get(title="snapshot-test", user=user1)
        snapshot2 = Snapshot.objects.get(title="snapshot-test2", user=user2)
       
        response = self.client.get(reverse('api:snapshots-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(SnapshotSerializer(snapshot1).data, response.json())
        self.assertNotIn(SnapshotSerializer(snapshot2).data, response.json())
        
    def test_snapshotGet(self):
        '''
            Test riguardante l'API snapshotGet:
            Mi aspetto un codice 500:
                - Se non loggato
                - Se provo a richiedere uno snapshot di cui non sono proprietario o inesistente
            Mi aspetto un codice 200 se richiedo uno snapshot di cui sono proprietario
        '''
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        user2 = CustomUser.objects.get(email="test2@gmail.com")
        
        # Snapshot
        
        snapshot1 = Snapshot.objects.get(title="snapshot-test", user=user1)
        snapshot2 = Snapshot.objects.get(title="snapshot-test2", user=user2)
        id1 = snapshot1.id
        id2 = snapshot2.id
        
        # File
        file = json.load(snapshot1.informations)
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.get(reverse('api:snapshot-get', kwargs={'snapshotId':id1}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Richiesta corretta
        response = self.client.get(reverse('api:snapshot-get', kwargs={'snapshotId':id1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(file,response.json())
        
        # Richiesta di uno snapshot di cui non sono proprietario
        response = self.client.get(reverse('api:snapshot-get', kwargs={'snapshotId':id2}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("non di tua proprieta", response.json()['message'])
        
         # Richiesta di uno snapshot non esistente
        response = self.client.get(reverse('api:snapshot-get', kwargs={'snapshotId':1000}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("snapshot inesistente", response.json()['message'])
        
    def test_snapshotCompute(self):
        '''
            Test riguardante l'API snapshotCompute:
            Mi aspetto un codice 500:
                - Se non loggato
                - Se provo a richiedere lo snapshot di un gruppo di cui non sono proprietario o inesistente
            Mi aspetto un codice 200 se richiedo lo snapshot di un gruppo di cui sono proprietario
        '''   
             
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        user2 = CustomUser.objects.get(email="test2@gmail.com")
        
        # Gruppi
        group1 = Agroup.objects.get(name="test-group", user=user1)
        group2 = Agroup.objects.get(name="test-group", user=user2)
        
        response = self.client.get(reverse('api:snapshot-compute', kwargs={'groupId':group1.id}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Richiesta corretta
        response = self.client.get(reverse('api:snapshot-compute', kwargs={'groupId':group1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(group1.id, response.json()['groupId'])
        
        # Richiesta di uno snapshot di cui non sono proprietario
        response = self.client.get(reverse('api:snapshot-compute', kwargs={'groupId':group2.id}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("non di tua proprieta", response.json()['message'])
        
         # Richiesta di uno snapshot non esistente
        response = self.client.get(reverse('api:snapshot-compute', kwargs={'groupId':1000}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("gruppo inesistente", response.json()['message'])
        
    def test_snapshotSave(self):
        '''
            Test riguardante l'API snapshotSave():
            Mi aspetto un codice 500 se non loggato
            Mi aspetto un codice 200 se loggato
        '''
        
        # Richiesta senza aver effettuato il login
        string_no_auth = "Non sei loggato"
        
        response = self.client.post(reverse('api:snapshot-save', kwargs={'title':"snapshotText3"}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        
        # Gruppi
        group1 = Agroup.objects.get(name="test-group", user=user1)
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        computated_snapshot = self.client.get(reverse('api:snapshot-compute', kwargs={'groupId':group1.id})).json()

        # Richiesta corretta
        response = self.client.post(reverse('api:snapshot-save', kwargs={'title':"snapshotText3"}), computated_snapshot, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("salvato con successo", response.json()['message'])
        self.assertTrue(Snapshot.objects.filter(id=response.json()['id']).exists())
        
        Snapshot.objects.filter(title="snapshotText3").delete()
     
    def test_snapshotDelete(self):
        '''
            Test riguardante l'API snapshotDelete:
            Mi aspetto di ricevere un codice 500 se:
                - Non loggato
                - Se provo ad eliminare uno snapshot di cui non sono proprietario o inesistente
            Mi aspetto di ricevere un codice 200 se elimino uno snapshot di mia proprietà
        '''
        
        string_no_auth = "Non sei loggato"
        
        response = self.client.delete(reverse('api:snapshot-delete', kwargs={'snapshotId':1}))
        self.assertEqual(response.status_code, 500)
        self.assertIn(string_no_auth, response.json()['message'])
        
        # Richiesta avendo effettuato il login
        
        # Utenti
        user1 = CustomUser.objects.get(email="test@gmail.com")
        user2 = CustomUser.objects.get(email="test2@gmail.com")
        
        # Snapshot
        
        snapshot1 = Snapshot.objects.get(title="snapshot-test", user=user1)
        snapshot2 = Snapshot.objects.get(title="snapshot-test2", user=user2)
        snapshot3 = Snapshot.objects.get(title="snapshot-test2", user=user1)
        id1 = snapshot1.id
        id2 = snapshot2.id
        id3 = snapshot3.id
        
        logged_in = self.client.login(email="test@gmail.com", password="test")
        self.assertTrue(logged_in) # Login andato a buon fine
        
        # Richiesta corretta
        response = self.client.delete(reverse('api:snapshot-delete', kwargs={'snapshotId':id3}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("eliminato con successo", response.json()['message'])
        self.assertFalse(Snapshot.objects.filter(id=id3).exists())
        
        # Richiesta eliminazione di uno snapshot di cui non sono proprietario
        response = self.client.delete(reverse('api:snapshot-delete', kwargs={'snapshotId':id2}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("non di tua proprieta", response.json()['message'])
        self.assertTrue(Snapshot.objects.filter(id=id2).exists())
        
       # Richiesta eliminazione di uno snapshot inesistente
        response = self.client.delete(reverse('api:snapshot-delete', kwargs={'snapshotId':id3}))
        self.assertEqual(response.status_code, 500)
        self.assertIn("snapshot inesistente", response.json()['message'])