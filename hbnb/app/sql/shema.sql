CREATE TABLE users (
   id CHAR(36) PRIMARY KEY,
   email VARCHAR(120) NOT NULL UNIQUE,
   password VARCHAR(255) NOT NULL,
   first_name VARCHAR(100) NOT NULL,
   last_name VARCHAR(100) NOT NULL,
   is_admin BOOLEAN DEFAULT FALSE,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE places (
   id CHAR(36) PRIMARY KEY,
   title VARCHAR(255) NOT NULL,
   description TEXT,
   price DECIMAL(10, 2) NOT NULL,
   latitude FLOAT,
   longitude FLOAT,
   owner_id CHAR(36) NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE amenities (
   id CHAR(36) PRIMARY KEY,
   name VARCHAR(128) NOT NULL UNIQUE,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE place_amenities (
   place_id CHAR(36) NOT NULL,
   amenity_id CHAR(36) NOT NULL,
   PRIMARY KEY (place_id, amenity_id),
   FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
   FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

CREATE TABLE reviews (
   id CHAR(36) PRIMARY KEY,
   text TEXT NOT NULL,
   rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
   user_id CHAR(36) NOT NULL,
   place_id CHAR(36) NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
   FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
   UNIQUE KEY unique_user_place_review (user_id, place_id)
);
