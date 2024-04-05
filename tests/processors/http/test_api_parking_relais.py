from pytest import mark
from src.processors.http.api_parking_relais import SELECT_ATTENDU, BaseUrl, print_resultat_csv
from src.processors.http.helper import retourne_extra_param, ajoute_liste_select
import tempfile
import os

from src.processors.http.model import ParkingInformationLeger

@mark.parametrize(
    ['val1', 'val2'],
    [(100, 'A'),('a', 0),(0, 0),(None, None)]
)
def test_base_url_extra_param(val1, val2):
    """
    Test la concatenation clef et valeur pour construire une liste de critere de recherche"""
    result = retourne_extra_param(clef=val1,clef1=val2)
    assert result =='clef='+str(val1)+'&clef1='+str(val2)

def test_ajoute_liste_select():
    """
    Test la concatenation des donnée à remonter
    """
    result = ajoute_liste_select(("val","val1"))
    assert result =='val, val1'
    result = ajoute_liste_select(SELECT_ATTENDU)
    assert result =='idobj, nom_complet, libtype, commune, capacite_voiture, capacite_pmr, capacite_vehicule_electrique, capacite_moto, capacite_velo'

# @mark.parametrize(
#     ['model_data'],
#     [ ParkingInformationLeger(), ParkingInformationLeger()]
# )
# def test_print_resultat_csv(model_data: ParkingInformationLeger):
#     with tempfile.TemporaryDirectory() as tempdir:
#         ficher_csv_tmp = os.path.join(tempdir, 'data_csv.csv')
#         print_resultat_csv(model_data, ficher_csv_tmp)
#         with open(ficher_csv_tmp, 'r') as tmpfile:
#             ltmpfile.read