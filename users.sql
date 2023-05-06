DROP TABLE IF EXISTS users;

CREATE TABLE users(id SERIAL PRIMARY KEY, email TEXT NOT NOT NULL, user_name TEXT NOT NULL, password_hash TEXT NOT NULL);

INSERT INTO users(email, name, password_hash) VALUES
    ('admin@gmail.com', 'admin', 'password');