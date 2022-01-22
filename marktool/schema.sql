-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS temp_users;
DROP TABLE IF EXISTS furs;

CREATE TABLE users (date text NOT NULL, gln text NOT NULL UNIQUE,
                    password text NOT NULL, email text NOT NULL UNIQUE);

CREATE TABLE temp_users (date text NOT NULL, gln text NOT NULL UNIQUE,
                    password text NOT NULL, email text NOT NULL UNIQUE, token text NOT NULL UNIQUE);

CREATE TABLE furs (gln text, gtin text, kiz text, tid text, sgtin text, sgtin_hex text,
                    FOREIGN KEY(gln) REFERENCES users(gln));
