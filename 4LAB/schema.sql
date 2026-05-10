CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    last_name TEXT,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO roles (id, name, description) VALUES
    (1, 'Администратор', 'Полный доступ к системе'),
    (2, 'Пользователь', 'Ограниченный доступ');

-- Default admin: login=admin, password=Admin123!
INSERT OR IGNORE INTO users (id, login, password_hash, first_name, last_name, middle_name, role_id)
VALUES (1, 'admin',
    'pbkdf2:sha256:260000$placeholder$placeholder',
    'Админ', 'Системный', NULL, 1);
