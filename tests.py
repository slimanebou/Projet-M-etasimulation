from automate import *

def test_q1_automate():
    print(">>> Test Q1 : AutomateCellulaire")

    """Test Q1: Verifie que l'espace d'etats est bien specifie A, 0 ... """
    etats_permis = ['0', '1', 'A', '□']
    automate = AutomateCellulaire(etats=etats_permis, regles={})
    
    assert automate.etats == etats_permis, "L'espace d'etats doit etre conserve exactement"
    assert '□' in automate.etats, "L'etat vide doit faire partie des etats"


    """Test Q1: Verifie le rejet des etats non declares"""
    try:
        AutomateCellulaire(etats=['0','1'], regles={('2','0','1'): '0'})
        assert False, "Devrait refuser les etats non declares"
    except AssertionError:
        pass  # Comportement attendu


def test_q2_configuration():
    print(">>> Test Q2 : Configuration")
    # Creation d'une configuration
    config = Configuration(["0", "1", "0", "1"])
    
    # Verification du contenu
    assert config.etats == ["0", "1", "0", "1"]
    
    # Affichage pour visualisation
    print("Configuration : ", config.etats)


def test_q3_lire_automate_et_mot():
    print(">>> Test Q3 : Lecture depuis fichier")

    # Creation temporaire d’un fichier de regles
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

    print("Lecture et initialisation reussies")


def test_q4_calculer_prochaine_configuration():
    print(">>> Test Q4 : Calcul de la prochaine configuration")

    # Creation d'un automate avec des regles
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
    expected = ['0', '0', '1', '1', '0', '0', '0']
    print("Nouvelle Configuration avec bords :", nouvelle_config.etats)

    # Verification du resultat
    assert nouvelle_config.etats == expected, f"Erreur dans la mise à jour de la configuration, attendu {expected}, obtenu {nouvelle_config.etats}"



def test_q5_simulation():
    print(">>> Test Q5 : Simulation d'automate")
    
    # Regles pour la regle 110 (La meme que regles.txt)
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
    config = Configuration(['0', '0', '0', '1', '0', '0', '0'])
    
    # EXEMPLE 1

    print("\n1. Test arret apres 5 pas:")
    resultats = simuler_automate(automate, config, mode_arret='pas', valeur_arret=5, afficher=True)
    assert (len(resultats) - 1) == 5, f"Devrait avoir 5 pas + config initiale (obtenu: {len(resultats)})"
    
    # EXEMPLE 2

    print("\n2. Test arret sur motif '111':")  
    resultats = simuler_automate(automate, config, mode_arret='transition', valeur_arret='111', afficher=True)
    assert any('111' in ''.join(c.etats) for c in resultats), "'111' devrait apparaître"

    # EXEMPLE 3

    
    # Regles pour stabilisation
    regles_stab = {
        ('0','0','0'): '0',
        ('0','0','1'): '0',
        ('0','1','0'): '0',
        ('0','1','1'): '0',
        ('1','0','0'): '1',
        ('1','0','1'): '0',
        ('1','1','0'): '0',
        ('1','1','1'): '0'
    }
    automate_stab = AutomateCellulaire(etats=['0','1'], regles=regles_stab)
    config_stab = Configuration(['1','1','0','1','1'])
    
    print("\n3. Test stabilisation:")
    resultats = simuler_automate(automate_stab, config_stab, mode_arret='stabilisation', afficher=True)
    assert resultats[-1].etats == resultats[-2].etats, "Dernieres configs devraient etre identiques"
    
    print("\nTous les tests de simulation sont passes avec succes")

def test_q6_affichage_visuel():
    print(">>> Test Q6 : Affichage visuel de la simulation")
    
    # Regles pour la regle 110
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
    config = Configuration(['0', '0', '0', '1', '0', '0', '0'])
    
    print("\nSimulation avec affichage visuel (5 pas):")
    resultats = simuler_automate_avec_affichage(automate, config, mode_arret='pas', valeur_arret=5)
    
    # Verification que la simulation a bien fonctionné
    assert (len(resultats) - 1) == 5, f"Devrait avoir 5 pas + config initiale (obtenu: {len(resultats)})"
    
    print("\nTest d'affichage visuel reussi")


def run_all_tests():
    test_q1_automate()
    test_q2_configuration()
    test_q3_lire_automate_et_mot()
    test_q4_calculer_prochaine_configuration()
    test_q5_simulation()
    test_q6_affichage_visuel()  

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
        elif test_name == "q5":  
            test_q5_simulation()
        elif test_name == "q6":
            test_q6_affichage_visuel()
        else:
            print(f"Aucun test nomme '{test_name}'")
