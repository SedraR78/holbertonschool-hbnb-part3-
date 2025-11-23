-- HBnB Initial Data
-- Insert initial administrator and amenities

-- Insert Administrator User (password: admin1234 - hashed with bcrypt)
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0L8k7OeY8J4d4E8bE8j8N8cYbY8c8Y8c8Y8c8Y', 
    TRUE
);


INSERT INTO amenities (id, name) VALUES 
    (uuid(), 'WiFi'),
    (uuid(), 'Swimming Pool'), 
    (uuid(), 'Air Conditioning');