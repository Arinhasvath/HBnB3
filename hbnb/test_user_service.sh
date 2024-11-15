import pytest
from app.services.user_service import UserService
from app.models.user import User

# Configuration des fixtures
@pytest.fixture
def mock_facade(mocker):
    """Créer un mock du facade pour les tests"""
    return mocker.Mock()

@pytest.fixture
def user_service(mock_facade):
    """Créer une instance du service utilisateur avec le mock facade"""
    return UserService(mock_facade)

# Test de récupération d'un utilisateur par ID
def test_get_user_by_id(user_service, mock_facade):
    # Préparation
    mock_user = User(id="1", email="test@test.com", is_admin=False)
    mock_facade.get_user.return_value = mock_user
    
    # Exécution
    result = user_service.get_user_by_id("1")
    
    # Vérification
    assert result == mock_user
    mock_facade.get_user.assert_called_once_with("1")

# Test de récupération d'un utilisateur par email
def test_get_user_by_email(user_service, mock_facade):
    # Préparation
    mock_user = User(id="1", email="test@test.com", is_admin=False)
    mock_facade.get_user_by_email.return_value = mock_user
    
    # Exécution
    result = user_service.get_user_by_email("test@test.com")
    
    # Vérification
    assert result == mock_user
    mock_facade.get_user_by_email.assert_called_once_with("test@test.com")

# Test de création d'utilisateur
def test_create_user(user_service, mock_facade):
    # Préparation
    user_data = {
        "email": "new@test.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    mock_user = User(
        id="1",
        email=user_data["email"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"]
    )
    mock_facade.create_user.return_value = mock_user
    
    # Exécution
    result = user_service.create_user(user_data)
    
    # Vérification
    assert result == mock_user
    mock_facade.create_user.assert_called_once_with(user_data)

# Test de mise à jour d'utilisateur
def test_update_user(user_service, mock_facade):
    # Préparation
    user_id = "1"
    update_data = {"first_name": "Updated"}
    mock_user = User(id=user_id, email="test@test.com")
    mock_facade.get_user.return_value = mock_user
    mock_facade.update_user.return_value = mock_user
    
    # Exécution
    result = user_service.update_user(user_id, update_data)
    
    # Vérification
    assert result == mock_user
    mock_facade.update_user.assert_called_once_with(user_id, update_data)

# Test de mise à jour avec email en double
def test_update_user_duplicate_email(user_service, mock_facade):
    # Préparation
    user_id = "1"
    new_email = "existing@test.com"
    update_data = {"email": new_email}
    
    # Configuration du mock pour simuler un utilisateur existant
    mock_user = User(id=user_id, email="old@test.com")
    mock_existing_user = User(id="2", email=new_email)
    mock_facade.get_user.return_value = mock_user
    mock_facade.get_user_by_email.return_value = mock_existing_user
    
    # Exécution et vérification
    with pytest.raises(ValueError, match="Email already in use"):
        user_service.update_user(user_id, update_data)

# Test des privilèges administrateur
def test_is_admin(user_service, mock_facade):
    # Préparation
    mock_admin = User(id="1", email="admin@test.com", is_admin=True)
    mock_facade.get_user.return_value = mock_admin
    
    # Exécution
    result = user_service.is_admin("1")
    
    # Vérification
    assert result is True
    mock_facade.get_user.assert_called_once_with("1")

def test_is_not_admin(user_service, mock_facade):
    # Préparation
    mock_user = User(id="1", email="user@test.com", is_admin=False)
    mock_facade.get_user.return_value = mock_user
    
    # Exécution
    result = user_service.is_admin("1")
    
    # Vérification
    assert result is False
    