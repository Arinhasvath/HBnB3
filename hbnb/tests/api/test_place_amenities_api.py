class TestPlaceAmenitiesAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.user = User(
                email='owner@test.com',
                password='test123',
                first_name='Owner',
                last_name='User'
            )
            db.session.add(self.user)
            db.session.commit()
            
            self.place = Place(
                title='Beach House',
                price=150.0,
                owner_id=self.user.id
            )
            db.session.add(self.place)
            
            self.amenity = Amenity(name='WiFi')
            db.session.add(self.amenity)
            db.session.commit()

    def test_add_amenity_to_place(self):
        response = self.client.post(f'/api/v1/places/{self.place.id}/amenities/{self.amenity.id}')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(f'/api/v1/places/{self.place.id}/amenities')
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'WiFi')