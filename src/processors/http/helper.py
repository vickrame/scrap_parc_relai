# TODO les nommer plutot car générique
def retourne_extra_param(**kwargs)-> str:
    """
    Concatenation de la l'uri et de de la sous ressource
    Par exemple:
    {'clef': 'val', 'clef1': 'val1'}
    Resultat clef=val&clef1=val1
    """
    #if len(kwargs) >0 else ""
    # f'{key}={value}' plutot que clef + " ffgdg" + 
    return '&'.join([f'{key}={value}' for key, value in kwargs.items()]) 


def ajoute_liste_select(tuple_select: tuple):
    """
    construction de la requet de select
    Par exemple:
    (clef1,clef2,clef3)
    Resultat clef1, clef2, clef3
    """
    return ', '.join(tuple_select)