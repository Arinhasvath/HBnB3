#!/bin/bash

echo "Creating base.py..."
mkdir -p tests
cat > tests/base.py << 'END'
import unittest
from collections.abc import Mapping
from flask_testing import TestCase
from app import create_app
from app.db import db

class BaseTestCase(TestCase):
   def create_app(self):
       app = create_app('testing')
       app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
       app.config['TESTING'] = True
       return app

   def setUp(self):
       db.create_all()

   def tearDown(self):
       db.session.remove()
       db.drop_all()
END

echo "Updating test files..."
find tests/ -name "test_*.py" -type f -exec sed -i '1i\from tests.base import BaseTestCase' {} \;
find tests/ -name "test_*.py" -type f -exec sed -i 's/class Test\([a-zA-Z]*\)(.*)/class Test\1(BaseTestCase)/' {} \;

echo "Done! Try running tests now."
