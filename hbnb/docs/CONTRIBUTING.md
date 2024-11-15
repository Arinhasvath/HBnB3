# 🤝 Guide de Contribution HBNB

## 📋 Table des Matières
1. [Introduction](#introduction)
2. [Code de Conduite](#code-de-conduite)
3. [Mise en Place de l'Environnement](#mise-en-place)
4. [Workflow de Développement](#workflow)
5. [Standards de Code](#standards)
6. [Tests](#tests)
7. [Documentation](#documentation)
8. [Soumission de Pull Requests](#pull-requests)

## 🎯 Introduction

Merci de contribuer au projet HBNB! Ce document fournit les lignes directrices pour contribuer efficacement au projet.

### 💼 Types de Contributions
- 🐛 Corrections de bugs
- ✨ Nouvelles fonctionnalités
- 📚 Documentation
- 🧪 Tests
- 🎨 Design et UI/UX

## 📜 Code de Conduite

### Principes Fondamentaux
- Respect mutuel
- Communication constructive
- Collaboration positive
- Inclusivité

## 🛠️ Mise en Place

### Prérequis
```bash
# Versions requises
Python 3.8+
Docker 20.10+
Git 2.30+
```

### Installation
```bash
# 1. Fork et clone
git clone https://github.com/VOTRE-USERNAME/hbnb.git
cd hbnb

# 2. Créer branche
git checkout -b feature/ma-fonctionnalite

# 3. Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# 4. Dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 🌊 Workflow de Développement

### 1. Branches
```bash
main        # Production
develop     # Développement
feature/*   # Nouvelles fonctionnalités
bugfix/*    # Corrections
hotfix/*    # Corrections urgentes
```

### 2. Commits
```bash
# Format
<type>(<scope>): <description>

# Types
feat:     Nouvelle fonctionnalité
fix:      Correction de bug
docs:     Documentation
test:     Tests
refactor: Refactoring
style:    Formatage
```

## 📐 Standards de Code

### Python
```python
# ✅ Bon
def calculate_total(items):
    """Calculate total price of items."""
    return sum(item.price for item in items)

# ❌ À éviter
def calc_tot(i):
    return sum([x.price for x in i])
```

### Tests
```python
# ✅ Bon test
def test_user_creation():
    """Test user creation with valid data."""
    user = User(
        email="test@example.com",
        password="secure_password",
        first_name="John"
    )
    assert user.email == "test@example.com"
    assert user.verify_password("secure_password")
```

## 🧪 Tests

### Exécution des Tests
```bash
# Tests unitaires
pytest tests/unit

# Tests d'intégration
pytest tests/integration

# Couverture
pytest --cov=app tests/
```

## 📝 Documentation

### Docstrings
```python
def process_booking(booking_id: str) -> dict:
    """
    Process a booking and update related systems.

    Args:
        booking_id (str): The unique identifier of the booking

    Returns:
        dict: Processing result with status and details

    Raises:
        BookingNotFoundError: If booking_id is invalid
        PaymentError: If payment processing fails
    """
```

## 🔄 Soumission de Pull Requests

### Checklist PR
- [ ] Tests ajoutés/mis à jour
- [ ] Documentation mise à jour
- [ ] Code formaté selon les standards
- [ ] Changements testés localement
- [ ] Description claire des changements

### Template PR
```markdown
## Description
[Description détaillée des changements]

## Type de Changement
- [ ] 🐛 Bug fix
- [ ] ✨ Nouvelle fonctionnalité
- [ ] 📚 Documentation
- [ ] 🔄 Refactoring

## Tests
[Description des tests effectués]

## Screenshots (si applicable)
```

## 📊 Processus de Review

### Critères de Review
1. ✅ Qualité du Code
   - Lisibilité
   - Maintenabilité
   - Performance

2. 🧪 Tests
   - Couverture
   - Cas d'erreur
   - Edge cases

3. 📚 Documentation
   - Clarté
   - Complétude
   - Exemples

## 🎉 Après Merge

1. 🧹 Nettoyage
```bash
git checkout main
git pull origin main
git branch -d feature/ma-fonctionnalite
```

2. 📢 Communication
- Mettre à jour le ticket associé
- Informer l'équipe des changements
- Mettre à jour la documentation si nécessaire

## 🙏 Remerciements

Merci de contribuer à HBNB! Votre aide est précieuse pour améliorer le projet.
