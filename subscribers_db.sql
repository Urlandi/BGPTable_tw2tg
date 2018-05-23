-- Text encoding used: System

PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: status
DROP TABLE IF EXISTS status;

CREATE TABLE status (
    IPV4 DECIMAL (32) UNIQUE
                   NOT NULL,
    IPV6 DECIMAL (32) UNIQUE
                   NOT NULL
    IPV4_TEXT TEXT (512) NOT NULL,
    IPV6_TEXT TEXT (512) NOT NULL
);

INSERT INTO status (
                       IPV4,
                       IPV6,
		       IPV4_TEXT,
                       IPV6_TEXT
                   )
                   VALUES (
                       1,
                       1,
                       1,
                       1
                   );

-- Table: subscribers
DROP TABLE IF EXISTS subscribers;

CREATE TABLE subscribers (
    subscriber_id DECIMAL (32) PRIMARY KEY
                            UNIQUE
                            NOT NULL,
    IPV4          BOOLEAN   NOT NULL
                            DEFAULT (1),
    IPV6          BOOLEAN   DEFAULT (1)
                            NOT NULL
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
