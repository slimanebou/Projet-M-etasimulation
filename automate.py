# structure d'un automate celluraie
class AutomateCellulaire:
    def __init__(self, etats: list, regles: dict,  etat_vide='□'):
        """
        :param etats: Liste des états possibles (ex: [0, 1] ou ['A', 'B', 'C'])
        :param regles: Dictionnaire {(gauche, centre, droite): nouvel_état}
        :param etat_vide: État pour les cellules non définies (défaut '□')
        """

        self.etats = etats
        self.regles = regles
        self.etat_vide = etat_vide

    def transition(self, voisins: tuple) -> str :  
        """
        :param voisins: Tuple (gauche, centre, droite)
        :return: Nouvel état de la cellule centrale
        Si la combinaison (gauche, centre, droite) n’est pas trouvée, retourne l’état par défaut.

        """
        return self.regles.get(voisins, self.etat_vide)
    



# structure d'une configuration
class Configuration:
    def __init__(self, etats: list):
        self.etats = etats  # Liste des états des cellules à l’instant t
        self.etats = [str(e) for e in etats]  # Conversion en string


def lire_automate_et_mot(fichier: str, mot_entree: str) -> tuple[AutomateCellulaire, Configuration]:
    etats = set()
    transitions = {}

    with open(fichier, 'r') as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne or "->" not in ligne:
                continue
            gauche, droite = ligne.split("->")
            triplet = tuple(gauche.strip(" ()").split(","))
            resultat = droite.strip()
            transitions[triplet] = resultat
            etats.update(triplet)
            etats.add(resultat)

    config = Configuration([c for c in mot_entree])
    return AutomateCellulaire(etats, transitions, etat_vide="□"), config


# Question 4
def calculer_prochaine_configuration(automate: AutomateCellulaire, config: Configuration) -> Configuration:
    """
    Calcule la prochaine configuration après un pas de calcul.
    Les bords sont traités avec '0' comme voisin, mais l'affichage inclut □ pour représenter l'extension.
    """
    nouveaux_etats = []
    n = len(config.etats)
    
    for i in range(n):
        # Règles de transition : les bords voient '0' comme voisin
        gauche = config.etats[i-1] if i > 0 else '0'
        centre = config.etats[i]
        droite = config.etats[i+1] if i < n-1 else '0'
        
        nouvel_etat = automate.transition((gauche, centre, droite))
        nouveaux_etats.append(nouvel_etat)
    
    # On ajoute □ aux extrémités pour l'affichage, mais en interne, les transitions utilisent '0'
    return Configuration([automate.etat_vide] + nouveaux_etats + [automate.etat_vide])





"""automate, config = lire_automate_et_mot("examples/regles.txt", "0001000")
print("États possibles :", automate.etats)
print("Configuration initiale :", config.etats)
print("Transition (1,1,0) ->", automate.transition(("1", "1", "0")))"""







if __name__ == "__main__":
    automate, config = lire_automate_et_mot("examples/regles.txt", "0001000")
    print("États possibles :", automate.etats)
    print("Configuration initiale :", config.etats)
    nouvelle_config = calculer_prochaine_configuration(automate, config)
    print("Nouvelle Configuration  :", nouvelle_config.etats) 
