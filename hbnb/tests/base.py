"""Base test configuration."""
import unittest
import os
from app import create_app
from app.db import db
from app.models import User, Place, Review, Amenity

class TestBase(unittest.TestCase):
    """Base test case class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

    def setUp(self):
        """Set up before each test."""
        db.session.begin()

    def tearDown(self):
        """Clean up after each test."""
        db.session.rollback()
        db.session.remove()

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        cls.app_context.pop()