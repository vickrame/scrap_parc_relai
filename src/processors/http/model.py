from collections.abc import Iterable
from dataclasses import dataclass, asdict


@dataclass
class Location:
    lon:float
    lat:float

@dataclass
class ParkingInformation:
    idobj: str
    nom_complet: str
    libtype: str
    commune: str
    adresse: str
    code_postal:int
    long_wgs84:float
    lat_wgs84:float
    location : Location
    presentation: str
    capacite_voiture:int
    capacite_pmr:int
    capacite_vehicule_electrique: int
    capacite_moto: int
    capacite_velo: int
    stationnement_velo:bool
    stationnement_velo_securise:bool
    autres_service_mob_prox: str
    services:str
    conditions_d_acces: str
    exploitant:str
    service_velo:str =""
    telephone: str = ""
    site_web: str = ""
    twitter: str = ""
    moyen_paiement:str = ""

@dataclass
class ParkingRelaisResultatList:
    total_count: int
    results : tuple[ParkingInformation]

@dataclass
class ParkingInformationLeger:
    idobj: str
    nom_complet: str
    libtype: str
    commune: str
    capacite_voiture:int
    capacite_pmr:int
    capacite_vehicule_electrique: int
    capacite_moto: int
    capacite_velo: int
    
    def print_to_csv(self):
        return self.idobj+";"+self.nom_complet+";"+self.libtype+";"+self.commune+";"+str(self.capacite_voiture)+";"+str(self.capacite_pmr)+";"+str(self.capacite_vehicule_electrique)+";"+str(self.capacite_moto)+";"+str(self.capacite_velo)