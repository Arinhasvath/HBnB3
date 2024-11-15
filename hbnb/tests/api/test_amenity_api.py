class TestAmenityAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities', json={
            'name': 'WiFi'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'WiFi')

    def test_get_amenities(self):
        self.client.post('/api/v1/amenities', json={'name': 'Pool'})
        response = self.client.get('/api/v1/amenities')
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Pool')
