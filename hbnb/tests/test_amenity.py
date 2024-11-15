from app.models.amenity import Amenity

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")

    assert amenity.name == "Wi-Fi"
    assert isinstance(amenity.name, str)
    print("Amenity creation test passed!")

test_amenity_creation()
