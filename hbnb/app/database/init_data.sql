INSERT INTO users (
   id, email, password, first_name, last_name, is_admin
) VALUES (
   '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
   'admin@hbnb.io',
   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/.4BW8HmlqyfD2f/2q',
   'Admin',
   'HBnB',
   TRUE
);

INSERT INTO amenities (id, name) VALUES 
(UUID(), 'WiFi'),
(UUID(), 'Swimming Pool'),
(UUID(), 'Air Conditioning');
