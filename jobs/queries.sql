-- SQLite
DROP TABLE IF EXISTS application;

CREATE TABLE IF NOT EXISTS application (
    id INTEGER PRIMARY KEY,
    job_id INTEGER,
    name VARCHAR NOT NULL,
    file_name VARCHAR NOT NULL,
    cover_letter TEXT NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY (job_id) 
      REFERENCES job (id) 
          ON DELETE CASCADE
          ON UPDATE NO ACTION
);