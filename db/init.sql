CREATE TABLE IF NOT EXISTS customers (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO customers (name, email)
VALUES
    ('Test Customer One', 'customer1@example.com'),
    ('Test Customer Two', 'customer2@example.com')
ON CONFLICT (email) DO NOTHING;
