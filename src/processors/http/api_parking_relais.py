import csv
import json
import logging

from requests import get
from dataclasses import asdict, dataclass
from math import floor
from json import JSONDecodeError
from csv import *

from src.processors.http.model import ParkingInformationLeger
from src.processors.http.helper import ajoute_liste_select, retourne_extra_param

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./logs/parking.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# un json est un dict
# () tuple immuable
# [] liste mutable
SELECT_ATTENDU = ("idobj","nom_complet", "libtype", "commune", "capacite_voiture", "capacite_pmr","capacite_vehicule_electrique","capacite_moto","capacite_velo")

class BaseUrl():
    """
    Classe pour attaquer une API rest
    Elle est constituée d'une base + une ressource
    """
    #le dataset est à variabiliser
    uri: str = "https://data.nantesmetropole.fr"
    ressources = "/api/explore/v2.1/catalog/datasets/244400404_parcs-relais-nantes-metropole/records?"
    limite:int =20  
    
    def construire_base_url(self)-> str:
        """
        Concatenation de la l'uri et de de la sous ressource
        """
        return self.uri+self.ressources

class ParkingRelaisQueryMeta(BaseUrl):
    """
    Classe reponse à la requete d'init
    Afin de savoir s'il existe des données et de connaitre le nombre d'iteration à produire en cas de grosse volumétrie (pour la pagination)
    """
    total_element: int=0
    nombre_iteration: int = 0
    
def appel_http(url_final: str):
    """
    Gere les appels en GET 
    """
    retour_http:dict=[]
    try:
        logger.debug("Récupération des méta data de la page pour connaitre le nombre d'element que l'on va traiter")
        contenu = get(url_final).content
        retour_http = json.loads(contenu)
    except JSONDecodeError as json_err:
        print(f'Le retour n''est pas un json')
        logger.error('l''url suivante ne retourne pas un json {url_final}', json_err)
    except Exception as ex:
        logger.error('Exception inattendu', ex)
    return retour_http

def get_information()-> ParkingRelaisQueryMeta:
    """
    Méthode d'appel à l'api pour connaitre le nombre d'iteration à effectuer
    """
    #on fixe l'url pour l'instant:
    #https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets/244400404_parcs-relais-nantes-metropole/records?limit=20
   
    recuperation_meta_data_parking_relai = ParkingRelaisQueryMeta()
    
    try:
        json_dict = appel_http(recuperation_meta_data_parking_relai.construire_base_url()
                      +retourne_extra_param(limit=0,offset=0))

        if len(json_dict)> 0:
            recuperation_meta_data_parking_relai.total_element= json_dict['total_count'] 
            if recuperation_meta_data_parking_relai.total_element > 0:
                recuperation_meta_data_parking_relai.nombre_iteration =  floor(recuperation_meta_data_parking_relai.total_element / recuperation_meta_data_parking_relai.limite) +1
    except JSONDecodeError as json_err:
        print(f'Le retour n''est pas un json')
    return recuperation_meta_data_parking_relai

def download_data(recuperation_meta_data, i):
    offset_val = str(recuperation_meta_data.limite*i)
    limit_val = str(recuperation_meta_data.limite)

    url_final=recuperation_meta_data.construire_base_url()+retourne_extra_param(limit=limit_val, offset=offset_val)+"&select="+ajoute_liste_select(SELECT_ATTENDU)

        #print(f'url dynamique {url_final}')
    json_dict = appel_http(url_final)
    liste_donnee_attendu = json_dict['results']
    return liste_donnee_attendu

def construire_liste_information_parking(recuperation_meta_data: ParkingRelaisQueryMeta):
    """
    Méthode pour une liste d'information sur les parking relai de Nantes.
    Elle se fait par iteération, cad on utilise le systeme de pagination de l'api
    """
    if recuperation_meta_data.total_element==0:
        return []

    # tant que l'on peut boucler suite à de la pagination
    #while(nombre_iteration<=recuperation_meta_data.nombre_iteration):
    return [
        ParkingInformationLeger(**item) 
            for i in range(recuperation_meta_data.nombre_iteration)
            for item in download_data(recuperation_meta_data, i)
        ]



    # for i in range(recuperation_meta_data.nombre_iteration):
    #     liste_donnee_attendu = download_data(recuperation_meta_data, i)
    #     for item in liste_donnee_attendu:
    #         #idobj_val = item['idobj']
    #         # nom_complet_val= item['nom_complet']
    #         # libtype_val= item['libtype']
    #         # commune_val= item['commune']
    #         # capacite_voiture_val= item['capacite_voiture']
    #         # capacite_pmr_val= item['capacite_pmr']
    #         # capacite_vehicule_electrique_val= item['capacite_vehicule_electrique']
    #         # capacite_moto_val= item['capacite_moto']
    #         # capacite_velo_val= item['capacite_velo']
        
    #         # construction auto alimenter par le dict **truc 
    #         # Contrainte meme convention de nommage
    #         resultat_final.append(ParkingInformationLeger(**item))
    #return resultat_final



def print_resultat_csv(resultat_final, chemin_fichier):
    """
    Ecriture final dan sun fichier CSV
    """
    with open(chemin_fichier,'w', encoding="utf-8") as csv_file:
        #flux_ecriture = writer(csv_file, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL)
        #flux_ecriture.writerow(["id","libelle","statut","commune","capacité_voiture"])
        #[ print(f'Item {item.__dict__()}') for item in resultat_final]
        #flux_ecriture.writerows([ item.print_to_csv().split(";") for item in resultat_final])
        flux_ecriture = csv.DictWriter(csv_file, fieldnames=SELECT_ATTENDU)
        flux_ecriture.writeheader()
        flux_ecriture.writerows([ asdict(item) for item in resultat_final])


def execute():
    """
    Mon main
    """
    print("Etape 0 ------ get metadata")
    recuperation_meta_data=get_information()
    print(f'Etape 0 Result : {recuperation_meta_data}' )
    print("Etape 1 ------ iteration")
    resultat_final= construire_liste_information_parking(recuperation_meta_data)

    print(f'Etape 1 Result {len(resultat_final)}')
    print(f'Etape 2 Sauvegarde du resultat en CSV')
    print_resultat_csv(resultat_final, "./data/parking_relais.csv")
    
execute()