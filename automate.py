# structure d'un automate celluraie
class AutomateCellulaire:
    def __init__(self, etats: list, regles: dict,  etat_vide='□'):
        """
        :param etats: Liste des etats possibles (ex: [0, 1] ou ['A', 'B', 'C'])
        :param regles: Dictionnaire {(gauche, centre, droite): nouvel_etat}
        :param etat_vide: Etat pour les cellules non definies (defaut '□')
        """

        self.etats = etats
        self.regles = regles
        self.etat_vide = etat_vide

    def transition(self, voisins: tuple) -> str :  
        """
        :param voisins: Tuple (gauche, centre, droite)
        :return: Nouvel etat de la cellule centrale
        Si la combinaison (gauche, centre, droite) n’est pas trouvee, retourne l’etat par defaut.

        """
        return self.regles.get(voisins, self.etat_vide)
    



# structure d'une configuration
class Configuration:
    def __init__(self, etats: list):
        self.etats = etats  # Liste des etats des cellules à l’instant t
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
    Calcule la prochaine configuration apres un pas de calcul.
    Les bords sont traites avec '0' comme voisin.
    """
    nouveaux_etats = []
    n = len(config.etats)
    
    for i in range(n):
        # Regles de transition : les bords voient '0' comme voisin
        gauche = config.etats[i-1] if i > 0 else '0'
        centre = config.etats[i]
        droite = config.etats[i+1] if i < n-1 else '0'
        
        nouvel_etat = automate.transition((gauche, centre, droite))
        nouveaux_etats.append(nouvel_etat)
    
    return Configuration(nouveaux_etats)



# Question 5

def simuler_automate(automate: AutomateCellulaire, config_initiale: Configuration, 
                    mode_arret: str = 'pas', valeur_arret=None, afficher: bool = True) -> list:
    configurations = [config_initiale]
    pas = 0
    
    if afficher:
        print(f"Configuration initiale: {''.join(config_initiale.etats)}")
    
    while True:
        current_config = ''.join(configurations[-1].etats)
        
        if mode_arret == 'transition' and valeur_arret in current_config:
            if afficher:
                print(f"Motif '{valeur_arret}' atteint apres {pas} pas")
            break
            
        if mode_arret == 'pas' and pas >= valeur_arret:
            break
            
        nouvelle_config = calculer_prochaine_configuration(automate, configurations[-1])
        configurations.append(nouvelle_config)
        pas += 1
        
        if afficher:
            print(f"Pas {pas}: {''.join(nouvelle_config.etats)}")
        
        if mode_arret == 'stabilisation' and nouvelle_config.etats == configurations[-2].etats:
            if afficher:
                print(f"Stabilisation atteinte apres {pas} pas")
            break
    
    return configurations

"""automate, config = lire_automate_et_mot("examples/regles.txt", "0001000")
print("Etats possibles :", automate.etats)
print("Configuration initiale :", config.etats)
print("Transition (1,1,0) ->", automate.transition(("1", "1", "0")))"""


# Question 6
def simuler_automate_avec_affichage(automate: AutomateCellulaire, config_initiale: Configuration, 
                                   mode_arret: str = 'pas', valeur_arret=None) -> list:
    """
    Simule l'automate cellulaire en affichant chaque configuration de manière visuelle.
    :param automate: L'automate cellulaire à simuler
    :param config_initiale: Configuration de départ
    :param mode_arret: 'pas', 'transition' ou 'stabilisation'
    :param valeur_arret: Nombre de pas ou motif à atteindre
    :return: Liste des configurations successives
    """
    configurations = [config_initiale]
    pas = 0
    
    # Affichage initial
    print("Configuration initiale:")
    print(''.join(config_initiale.etats))
    print()
    
    while True:
        current_config = ''.join(configurations[-1].etats)
        
        # Conditions d'arrêt
        if mode_arret == 'transition' and valeur_arret in current_config:
            print(f"Motif '{valeur_arret}' atteint après {pas} pas")
            break
            
        if mode_arret == 'pas' and pas >= valeur_arret:
            break
            
        # Calcul de la nouvelle configuration
        nouvelle_config = calculer_prochaine_configuration(automate, configurations[-1])
        configurations.append(nouvelle_config)
        pas += 1
        
        # Affichage visuel
        print(f"Pas {pas}:")
        # Remplacer les états par des caractères plus visuels
        visuel = ''.join(['■' if e == '1' else '□' if e == '0' else e for e in nouvelle_config.etats])
        print(visuel)
        print()  # Ligne vide pour séparer les pas
        
        if mode_arret == 'stabilisation' and nouvelle_config.etats == configurations[-2].etats:
            print(f"Stabilisation atteinte après {pas} pas")
            break
    
    return configurations







if __name__ == "__main__":
    """automate, config = lire_automate_et_mot("examples/regles.txt", "0001000")
    print("Etats possibles :", automate.etats)
    print("Configuration initiale :", config.etats)
    nouvelle_config = calculer_prochaine_configuration(automate, config)
    print("Nouvelle Configuration  :", nouvelle_config.etats) """

    """# Regles uniques pour tous les tests (Regle 110)
    regles_110 = {
        ('0', '0', '0'): '0',
        ('0', '0', '1'): '1',
        ('0', '1', '0'): '1',
        ('0', '1', '1'): '1',
        ('1', '0', '0'): '0',
        ('1', '0', '1'): '1',
        ('1', '1', '0'): '1',
        ('1', '1', '1'): '0'
    }

    automate = AutomateCellulaire(etats=['0', '1'], regles=regles_110)

    print("=== Test 1: Arret apres 5 pas ===")
    config1 = Configuration(['0', '0', '0', '1', '0', '0', '0'])
    simuler_automate(automate, config1, mode_arret='pas', valeur_arret=5)

    print("\n=== Test 2: Arret quand '111' apparait ===")
    config2 = Configuration(['0', '0', '0', '1', '0', '0', '0'])
    simuler_automate(automate, config2, mode_arret='transition', valeur_arret='111')

    # Regles qui stabilisent en 2 pas
    regles_stab = {
        ('0','0','0'): '0',
        ('0','0','1'): '0',
        ('0','1','0'): '0',
        ('0','1','1'): '0',
        ('1','0','0'): '1',  # Seule regle conservant 1
        ('1','0','1'): '0',
        ('1','1','0'): '0',
        ('1','1','1'): '0'
    }
    
    automate = AutomateCellulaire(etats=['0','1'], regles=regles_stab)
    config = Configuration(['1','1','0','1','1'])
    
    print("\n=== Test 3: Vraie stabilisation avec verification ===")
    simuler_automate(automate, config, mode_arret='stabilisation')"""

    # Exemple pour la fonction d'affichage
    """regles_110 = {
        ('0', '0', '0'): '0',
        ('0', '0', '1'): '1',
        ('0', '1', '0'): '1',
        ('0', '1', '1'): '1',
        ('1', '0', '0'): '0',
        ('1', '0', '1'): '1',
        ('1', '1', '0'): '1',
        ('1', '1', '1'): '0'
    }

    automate = AutomateCellulaire(etats=['0', '1'], regles=regles_110)
    config = Configuration(['0', '0', '0', '1', '0', '0', '0'])

    # Simulation avec affichage visuel
    simuler_automate_avec_affichage(automate, config, mode_arret='pas', valeur_arret=5)"""