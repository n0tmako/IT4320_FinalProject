DROP TABLE IF EXISTS reservations;

CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    row INTEGER NOT NULL,
    column INTEGER NOT NULL,
    price INTEGER NOT NULL,
    reservation_code TEXT NOT NULL UNIQUE
);

DROP TABLE IF EXISTS admins;

CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);