from automate import *

def test_q1_automate():
    print(">>> Test Q1 : AutomateCellulaire")

    """Test Q1: Vérifie que l'espace d'états est bien spécifié A, 0 ... """
    etats_permis = ['0', '1', 'A', '□']
    automate = AutomateCellulaire(etats=etats_permis, regles={})
    
    assert automate.etats == etats_permis, "L'espace d'états doit être conservé exactement"
    assert '□' in automate.etats, "L'état vide doit faire partie des etats"


    """Test Q1: Vérifie le rejet des états non déclarés"""
    try:
        AutomateCellulaire(etats=['0','1'], regles={('2','0','1'): '0'})
        assert False, "Devrait refuser les états non déclarés"
    except AssertionError:
        pass  # Comportement attendu


def test_q2_configuration():
    print(">>> Test Q2 : Configuration")
    # Création d'une configuration
    config = Configuration(["0", "1", "0", "1"])
    
    # Vérification du contenu
    assert config.etats == ["0", "1", "0", "1"]
    
    # Affichage pour visualisation
    print("Configuration : ", config.etats)


def test_q3_lire_automate_et_mot():
    print(">>> Test Q3 : Lecture depuis fichier")

    # Création temporaire d’un fichier de règles
    with open("regles_test.txt", "w") as f:
        f.write("""(1,1,1) -> 0
(1,1,0) -> 1
(1,0,1) -> 1
(0,0,0) -> 0
""")

    automate, config = lire_automate_et_mot("regles_test.txt", "101")

    assert isinstance(automate, AutomateCellulaire)
    assert isinstance(config, Configuration)
    assert config.etats == ["1", "0", "1"]
    assert automate.transition(("1", "1", "0")) == "1"
    assert automate.transition(("0", "0", "0")) == "0"

    print("Lecture et initialisation réussies")


def test_q4_calculer_prochaine_configuration():
    print(">>> Test Q4 : Calcul de la prochaine configuration")

    # Création d'un automate avec des règles
    etats_permis = ['0', '1']
    regles = {
        ('1', '1', '1'): '0',
        ('1', '1', '0'): '1',
        ('1', '0', '1'): '1',
        ('1', '0', '0'): '0',
        ('0', '1', '1'): '1',
        ('0', '1', '0'): '1',
        ('0', '0', '1'): '1',
        ('0', '0', '0'): '0',
    }
    automate = AutomateCellulaire(etats=etats_permis, regles=regles)

    # Configuration initiale
    config = Configuration(["0", "0", "0", "1", "0", "0", "0"])
    print("Configuration initiale :", config.etats)

    # Calcul de la nouvelle configuration
    nouvelle_config = calculer_prochaine_configuration(automate, config)

    # Configuration attendue avec les bords '□' inclus
    expected = ['□', '0', '0', '1', '1', '0', '0', '0', '□']
    print("Nouvelle Configuration avec bords :", nouvelle_config.etats)

    # Vérification du résultat
    assert nouvelle_config.etats == expected, f"Erreur dans la mise à jour de la configuration, attendu {expected}, obtenu {nouvelle_config.etats}"




# Lancer tous les tests
def run_all_tests():
    test_q1_automate()
    test_q2_configuration()
    test_q3_lire_automate_et_mot()
    test_q4_calculer_prochaine_configuration()


# Lancer un test spécifique depuis la ligne de commande
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        run_all_tests()
    else:
        test_name = sys.argv[1]
        if test_name == "q1":
            test_q1_automate()
        elif test_name == "q2":
            test_q2_configuration()
        elif test_name == "q3":
            test_q3_lire_automate_et_mot()
        elif test_name == "q4":
            test_q4_calculer_prochaine_configuration()

        else:
            print(f"Aucun test nommé '{test_name}'")
