CREATE TABLE specialists (
    specialist_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL
);

CREATE TABLE cases (
    case_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    specialist_id INTEGER,
    date_opened TEXT NOT NULL,
    due_date TEXT NOT NULL,
    date_resolved TEXT,
    FOREIGN KEY (specialist_id)
        REFERENCES specialists(specialist_id)
);
