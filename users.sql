DROP TABLE IF EXISTS users;

CREATE TABLE users(id SERIAL PRIMARY KEY, email TEXT NOT NULL, user_name TEXT NOT NULL, password_hash TEXT NOT NULL);

INSERT INTO users(email, user_name) VALUES ('admin@gmail.com', 'admin', 'test');
-- admin@gmail.com, password, admin1@gmail.com, pass