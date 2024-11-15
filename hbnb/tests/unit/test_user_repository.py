"""test_user_repository.py"""
from tests.unit.test_base_repository import TestBaseRepository
from app.repositories.user_repository import UserRepository

class TestUserRepository(TestBaseRepository):
    def setUp(self):
        super().setUp()
        self.repo = UserRepository()

    def test_get_by_email(self):
        user = User(email='test@test.com',
                   password='test123',
                   first_name='Test',
                   last_name='User')
        self.repo.add(user)
        
        found_user = self.repo.get_by_email('test@test.com')
        self.assertEqual(found_user.email, user.email)

    def test_get_by_admin(self):
        admin = User(email='admin@test.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='User',
                    is_admin=True)
        self.repo.add(admin)
        
        admins = self.repo.get_by_admin()
        self.assertEqual(len(admins), 1)
        self.assertTrue(admins[0].is_admin)