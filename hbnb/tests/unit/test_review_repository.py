"""test_review_repository.py"""
class TestReviewRepository(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db.create_all()
            self.repo = ReviewRepository()
            
            # Create test user and place
            self.user = User(email='test@test.com', password='test123',
                           first_name='Test', last_name='User')
            db.session.add(self.user)
            
            self.place = Place(title='Test Place', price=100,
                             owner_id=self.user.id)
            db.session.add(self.place)
            db.session.commit()

    def test_create_review(self):
        with self.app.app_context():
            review = Review(
                text='Great place!',
                rating=5,
                user_id=self.user.id,
                place_id=self.place.id
            )
            saved_review = self.repo.add(review)
            self.assertEqual(saved_review.rating, 5)

    def test_get_average_rating(self):
        with self.app.app_context():
            review1 = Review(text='Review 1', rating=4, 
                           user_id=self.user.id, place_id=self.place.id)
            review2 = Review(text='Review 2', rating=5,
                           user_id=self.user.id, place_id=self.place.id)
            self.repo.add(review1)
            self.repo.add(review2)

            avg = self.repo.get_average_rating_for_place(self.place.id)
            self.assertEqual(avg, 4.5)
