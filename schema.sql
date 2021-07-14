DROP TABLE IF EXISTS cache;

CREATE TABLE cache (
    dfr3_id TEXT,
    sample_size INTEGER,
    data TEXT
);

CREATE INDEX idx_dfr3_id
ON cache(dfr3_id);