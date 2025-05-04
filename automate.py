import sys
sys.stdout.reconfigure(encoding='utf-8')

# Question 1
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
    


#Question 2
# structure d'une configuration
class Configuration:
    def __init__(self, etats: list):
        self.etats = etats  # Liste des etats des cellules a l’instant t
        self.etats = [str(e) for e in etats]  # Conversion en string


# Question 3
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


# Question 6
def simuler_automate_avec_affichage(automate: AutomateCellulaire, config_initiale: Configuration, 
                                    mode_arret: str = 'pas', valeur_arret=None) -> list:
    """
    Version finale avec symboles "✓" (vrai) et "✗" (faux) pour une meilleure lisibilite
    """
    configurations = [config_initiale]
    pas = 0
    
    def afficher_config(etats):
        """Convertit les etats en symboles visuels explicites"""
        visuel = []
        for e in etats:
            if e == '0':
                visuel.append('✗')  # Etat faux/inactif
            elif e == '1':
                visuel.append('✓')  # Etat vrai/actif
            elif e == automate.etat_vide:
                visuel.append('.')  # Etat vide == .
            else:
                visuel.append(e)     # Autres etats (affiches tels quels)
        return ''.join(visuel)
    
    print("Configuration initiale:")
    print(f"|{afficher_config(config_initiale.etats)}|")  
    print()
    
    while True:
        current_config = configurations[-1].etats
        
        if mode_arret == 'transition' and valeur_arret in ''.join(current_config):
            print(f"Motif '{valeur_arret}' atteint apres {pas} pas")
            break
        if mode_arret == 'pas' and pas >= valeur_arret:
            break
            
        nouvelle_config = calculer_prochaine_configuration(automate, configurations[-1])
        configurations.append(nouvelle_config)
        pas += 1
        
        print(f"Pas {pas}:")
        print(f"|{afficher_config(nouvelle_config.etats)}|")
        print()
        
        if mode_arret == 'stabilisation' and nouvelle_config.etats == configurations[-2].etats:
            print(f"Stabilisation atteinte apres {pas} pas")
            break
    
    return configurations


# Question 8 
# structure de maching de turing 
class TuringMachine:
    def __init__(self):
        self.etats = set()           # Ensemble des etats (ex: {'q0', 'q1', 'q_accept', 'q_reject'})
        self.alphabet = {'0', '1', '□'} # Alphabet de travail (0, 1, et le symbole blanc □)
        self.blank_symbol = '□'        # Symbole blanc
        self.input_alphabet = {'0', '1'} # Alphabet d'entre (sous-ensemble de l'alphabet de travail)
        
        # Fonction de transition : un dictionnaire de dictionnaires de tuples
        # Format : {état: {symbole: (nouvel_état, symbole_écrit, direction)}}
        self.transitions = {}
        
        self.etat_initial = None      # Etat initial (ex: 'q0')
        self.etat_accept = None       # Etat acceptant (ex: 'q_accept')
        self.etat_reject = None       # Etat rejetant (ex: 'q_reject')


# Question 9 
# Structure d'une configuration 
# deque (double-ended queue) Ajouter a gauche ou a droite (appendleft, append)
from collections import deque
class TuringConfiguration:
    def __init__(self, tape, head_position, current_state):
        self.tape = tape                   # deque(['1','0','1','□',...])
        self.head_position = head_position # Index entier
        self.current_state = current_state # ex: 'q0'

# Question 10

def lire_machine_turing(fichier: str, mot_entree: str) -> tuple[TuringMachine, TuringConfiguration]:
    tm = TuringMachine()
    
    with open(fichier, 'r', encoding='utf-8') as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne or ligne.startswith('#'):
                continue

            if '->' in ligne:
                # Ligne de transition : q0,0 -> q1,1,D
                gauche, droite = ligne.split('->')
                etat_actuel, symbole_lu = [x.strip() for x in gauche.strip().split(',')]
                nouvel_etat, symbole_ecrit, direction = [x.strip() for x in droite.strip().split(',')]

                if etat_actuel not in tm.transitions:
                    tm.transitions[etat_actuel] = {}

                tm.transitions[etat_actuel][symbole_lu] = (nouvel_etat, symbole_ecrit, direction)
                tm.etats.update([etat_actuel, nouvel_etat])
                tm.alphabet.update([symbole_lu, symbole_ecrit])

            elif ligne.startswith('init:'):
                tm.etat_initial = ligne.split(':')[1].strip()
            elif ligne.startswith('accept:'):
                tm.etat_accept = ligne.split(':')[1].strip()
            elif ligne.startswith('reject:'):
                tm.etat_reject = ligne.split(':')[1].strip()

    # Initialisation de la bande et de la configuration
    tape = deque(mot_entree)
    config = TuringConfiguration(tape=tape, head_position=0, current_state=tm.etat_initial)

    return tm, config

# Question 11

def calculer_pas(tm: TuringMachine, config: TuringConfiguration) -> TuringConfiguration:
    etat_actuel = config.current_state
    position_tete = config.head_position
    tape = config.tape
    
    # Verifier si l'etat actuel et le symbole sur la bande existent dans les transitions
    if etat_actuel not in tm.transitions:
        raise ValueError(f"Etat {etat_actuel} non valide dans les transitions de la machine.")

    # Lire le symbole sur la bande a la position de la tete
    symbole_lu = tape[position_tete] if 0 <= position_tete < len(tape) else '□'

    # Verifier si la transition existe pour l'etat actuel et le symbole lu
    if symbole_lu not in tm.transitions[etat_actuel]:
        raise ValueError(f"Aucune transition definie pour l'etat {etat_actuel} avec le symbole {symbole_lu}.")

    # Appliquer la transition
    nouvel_etat, symbole_ecrit, direction = tm.transitions[etat_actuel][symbole_lu]
    
    # ecrire le symbole sur la bande a la position de la tete
    tape[position_tete] = symbole_ecrit
    
    # Deplacer la tete
    if direction == 'D':  # Droite
        position_tete += 1
        if position_tete == len(tape):  # Ajouter un espace vide a la fin de la bande si neecessaire
            tape.append('□')
    elif direction == 'G':  # Gauche
        position_tete -= 1
        if position_tete < 0:  # Ajouter un espace vide au debut de la bande si necessaire
            tape.appendleft('□')
            position_tete = 0
    
    # Retourner la nouvelle configuration
    return TuringConfiguration(tape=tape, head_position=position_tete, current_state=nouvel_etat)


# Question 12

def simuler_machine_turing(mot: str, tm: TuringMachine) -> str:
    """
    Simule le calcul d'une machine de Turing sur un mot donne et retourne 
    "ACCEPT" si la machine accepte le mot, "REJECT" si elle le rejette.
    
    Args:
        mot (str): Le mot d'entre a traiter
        tm (TuringMachine): La machine de Turing aS simuler
        
    Returns:
        str: "ACCEPT" ou "REJECT" selon le resultat du calcul
    """
    # Initialisation de la configuration
    config = TuringConfiguration(
        tape=deque(mot),
        head_position=0,
        current_state=tm.etat_initial
    )
    
    # Simulation jusqu'a atteindre un etat acceptant ou rejetant
    while True:
        # Verifier si on est dans un etat final
        if config.current_state == tm.etat_accept:
            return "ACCEPT"
        if config.current_state == tm.etat_reject:
            return "REJECT"
        
        # Calculer le prochain pas
        try:
            config = calculer_pas(tm, config)
        except (ValueError, IndexError) as e:
            # Si une erreur survient (transition non definie), considerer comme rejet
            return "REJECT"


# Question 13 
def machine_turing_vers_automate(tm: TuringMachine) -> AutomateCellulaire:
    """
    Convertit une machine de Turing en un automate cellulaire qui la simule.

    Args:
        tm (TuringMachine): La machine de Turing à simuler

    Returns:
        AutomateCellulaire: L'automate cellulaire équivalent
    """

    # Création de (ensemble) l'espace d'états de l'automate cellulaire pour stocker les états, ignorer les doublons
    etats_automate = set()

    # États pour les cellules sans tête: (*, symbole) pour prépararer de tous les états possibles sans tete 
    #(*, '0'), (*, '1'), (*, '□') pour tout l'alphabet de MT
    for symbole in tm.alphabet:
        etats_automate.add(('*', symbole))

    # États pour les cellules avec tête: (etat_mt, symbole), initialise toutes les combinaisons possibles
    # ('q0', '0'), ('q0', '1'), ('q0', '□') pour tout l'alphabet de cette etat
    for etat in tm.etats:
        for symbole in tm.alphabet:
            etats_automate.add((etat, symbole))

    # Construction (dictionnaire) des règles de transition
    regles = {}

    # Cas 1: La tête n'est dans aucun des 3 cellules du voisinage ( ('*', s1), ('*', s2), ('*', s3) )
    # Dans ce cas, on ne change rien
    for s1 in tm.alphabet:
        for s2 in tm.alphabet:
            for s3 in tm.alphabet:
                regles[(('*', s1), ('*', s2), ('*', s3))] = ('*', s2)

    # Cas 2: La tête est sur la cellule centrale
    # transition : {état: {symbole: (nouvel_état, symbole_écrit, direction)}}  = {'q0': {'0': ('q1', '1', 'R')}}
    for etat in tm.transitions:
        for symbole in tm.transitions[etat]:
            nouvel_etat, nouveau_symbole, direction = tm.transitions[etat][symbole]

            # Pour tous les symboles possibles à gauche et à droite
            for s_gauche in tm.alphabet:
                for s_droite in tm.alphabet:
                    if direction == 'D':  # Tête se déplace à droite
                        regles[(('*', s_gauche), (etat, symbole), ('*', s_droite))] = ('*', nouveau_symbole)
                        regles[((etat, symbole), ('*', s_droite), ('*', s_droite))] = (nouvel_etat, s_droite)

                    elif direction == 'G':  # Tête se déplace à gauche
                        regles[(('*', s_gauche), (etat, symbole), ('*', s_droite))] = ('*', nouveau_symbole)
                        regles[(('*', s_gauche), ('*', s_gauche), (etat, symbole))] = (nouvel_etat, s_gauche)

    return AutomateCellulaire(etats=list(etats_automate), 
                              regles=regles, 
                              etat_vide=('*', tm.blank_symbol))


def config_mt_vers_config_ac(config_mt: TuringConfiguration) -> Configuration:
    """
    Convertit une configuration de machine de Turing en configuration d'automate cellulaire.

    Args:
        config_mt (TuringConfiguration): Configuration de la MT

    Returns:
        Configuration: Configuration équivalente pour l'automate cellulaire
    """
    etats_ac = []
    for i, symbole in enumerate(config_mt.tape):
        if i == config_mt.head_position:
            etats_ac.append((config_mt.current_state, symbole))
        else:
            etats_ac.append(('*', symbole))

    return Configuration([str(e) for e in etats_ac])


def simuler_mt_avec_ac(tm: TuringMachine, ac: AutomateCellulaire):
    print("simulation n'est pas encore faite")

        

        

# Question 14 
 
"""Le probleme HALTING-CELLULAR-AUTOMATON demande si un automate cellulaire A, partant d'un etat s et d'un mot w, atteindra un etat contenant s lors de son evolution. 
 Notre code simule cet automate en appliquant des regles de transition et verifie si l'etat cible est atteint. 
 Cependant, ce probleme est indecidable, car les automates cellulaires peuvent simuler n'importe quelle machine de Turing, y compris des calculs infinis. 
 Ainsi, determiner si l'automate atteindra s revient au probleme de l'arret, qui est indecidable (aucun algorithme ne peut toujours repondre).
 Ce qui fait que la simulation peut donc boucler indefiniment pour certaines configurations, confirmant qu'il n'existe pas de methode generale pour resoudre ce probleme.
 Seules des restrictions (automates finis ou regles simplifies) le rendent decidable."""


if __name__ == "__main__":
    #q1 -- q3
    """automate, config = lire_automate_et_mot("examples/regles.txt", "0001000")
    print("Etats possibles :", automate.etats)
    print("Configuration initiale :", config.etats)
    print("Transition (1,1,0) ->", automate.transition(("1", "1", "0")))"""



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


    """mot = "10101"
    tm, config = lire_machine_turing("examples/machine_exemple.txt", mot)

    print("Etat initial :", tm.etat_initial)
    print("Etat acceptant :", tm.etat_accept)
    print("Transitions :")
    for etat, trans in tm.transitions.items():
        for symbole, action in trans.items():
            print(f"  {etat}, {symbole} -> {action}")

    print("\nConfiguration initiale :")
    print("Bande :", ''.join(config.tape))
    print("Position de la tete :", config.head_position)
    print("Symbole sous la tete :", config.tape[config.head_position])
    print("Etat courant :", config.current_state)"""


    """"mot = "10101"
    tm, config = lire_machine_turing("examples/machine_exemple.txt", mot)

    print("Avant le pas :")
    print("  Etat :", config.current_state)
    print("  Tete position :", config.head_position)
    print("  Bande :", list(config.tape))

    config = calculer_pas(tm, config)

    print("Apres un pas :")
    print("  Etat :", config.current_state)
    print("  Tete position :", config.head_position)
    print("  Bande :", list(config.tape))"""


    # Exemple 1 : Mot qui devrait etre accepte
    """mot1 = "101"
    tm, config = lire_machine_turing("examples/machine_exemple.txt", mot1)  # Appel de lire_machine_turing
    resultat1 = simuler_machine_turing(mot1, tm)  # Simulation avec la machine de Turing
    print(f"Resultat pour '{mot1}': {resultat1}")  # Resultat attendu : "accepte"

    # Exemple 2 : Mot qui devrait etre rejete
    mot2 = "110"
    tm, config = lire_machine_turing("examples/machine_exemple.txt", mot2)  # Appel de lire_machine_turing
    resultat2 = simuler_machine_turing(mot2, tm)  # Simulation avec la machine de Turing
    print(f"Resultat pour '{mot2}': {resultat2}")  # Resultat attendu : "rejete"""

    automate, config = lire_automate_et_mot("examples/Q7_3_regle90.txt", "000100")
    simuler_automate(automate, config, mode_arret='pas', valeur_arret=15, afficher=True)





