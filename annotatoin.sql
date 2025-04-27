CREATE TABLE IF NOT EXISTS annotations (
    slide_id TEXT,
    key TEXT,
    value TEXT,
    PRIMARY KEY (slide_id, key)
);
