-- SQLite Dummy Data: Library System
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nationality TEXT
);

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER REFERENCES authors (id),
    title TEXT NOT NULL,
    genre TEXT,
    published INTEGER, -- year
    pages INTEGER,
    available INTEGER DEFAULT 1 -- 1=yes, 0=checked out
);

CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    joined TEXT DEFAULT(date('now'))
);

CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER REFERENCES books (id),
    member_id INTEGER REFERENCES members (id),
    loaned_at TEXT DEFAULT(datetime('now')),
    due_date TEXT,
    returned_at TEXT
);

-- Authors
INSERT INTO
    authors (name, nationality)
VALUES ('Naguib Mahfouz', 'Egyptian'),
    ('George Orwell', 'British'),
    (
        'Gabriel García Márquez',
        'Colombian'
    ),
    ('Toni Morrison', 'American'),
    ('Haruki Murakami', 'Japanese');

-- Books
INSERT INTO
    books (
        author_id,
        title,
        genre,
        published,
        pages,
        available
    )
VALUES (
        1,
        'Cairo Trilogy',
        'Fiction',
        1956,
        1350,
        1
    ),
    (
        1,
        'Children of the Alley',
        'Allegory',
        1959,
        430,
        0
    ),
    (
        2,
        '1984',
        'Dystopian',
        1949,
        328,
        1
    ),
    (
        2,
        'Animal Farm',
        'Satire',
        1945,
        112,
        1
    ),
    (
        3,
        'One Hundred Years of Solitude',
        'Magical Realism',
        1967,
        417,
        0
    ),
    (
        4,
        'Beloved',
        'Historical',
        1987,
        321,
        1
    ),
    (
        5,
        'Norwegian Wood',
        'Romance',
        1987,
        296,
        1
    ),
    (
        5,
        'Kafka on the Shore',
        'Magical Realism',
        2002,
        467,
        1
    );

-- Members
INSERT INTO
    members (name, email)
VALUES (
        'Layla Hassan',
        'layla@lib.eg'
    ),
    ('Mark Spencer', 'mark@lib.eg'),
    (
        'Yasmine Farouk',
        'yasmine@lib.eg'
    ),
    ('Tom Bradley', 'tom@lib.eg');

-- Loans
INSERT INTO
    loans (
        book_id,
        member_id,
        loaned_at,
        due_date,
        returned_at
    )
VALUES (
        2,
        1,
        '2026-02-01',
        '2026-02-15',
        '2026-02-14'
    ),
    (
        5,
        2,
        '2026-02-20',
        '2026-03-06',
        NULL
    ),
    (
        3,
        3,
        '2026-03-01',
        '2026-03-15',
        NULL
    ),
    (
        1,
        4,
        '2026-01-10',
        '2026-01-24',
        '2026-01-23'
    );

SELECT '✅ SQLite: library.db loaded with authors, books, members, loans' AS status;