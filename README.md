# Simulateur d'Automate Cellulaire

Le but de ce projet est de simuler des automates cellulaires `a une dimension et de s’en servir pour simuler une machine de Turing.

## Comment utiliser

### Installation

```bash
git clone git@github.com:slimanebou/Projet-M-etasimulation.git
cd Projet-M-etasimulation
```

### Exécution

- Tous les tests :

```bash
make tests
```

- Test spécifique (ex Q4, Q5...) :

```bash
make test_q4
```

- Lancer un exemple :

```bash
make
```

### Fichiers importants

- `automate.py` : Implémentation principale
- `tests.py` : Contient les tests par question
- `examples/` : Exemples d'automates

## Questions implémentées

| Question | Statut |
| -------- | ------ |
| Q1       | ✅     |
| Q2       | ✅     |
| Q3       | ✅     |
| Q4       | ✅     |
