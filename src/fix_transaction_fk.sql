PRAGMA foreign_keys=OFF;

CREATE TABLE "Transaction_new" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "amount" real NOT NULL,
    "log_date" date NOT NULL,
    "description" text NOT NULL,
    "note" text NULL,

    "category_name" text NOT NULL
        REFERENCES "Category" ("name")
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    "cycle_id" bigint NOT NULL
        REFERENCES "Cycle" ("id")
        DEFERRABLE INITIALLY DEFERRED
);

INSERT INTO "Transaction_new"
SELECT * FROM "Transaction";

DROP TABLE "Transaction";

ALTER TABLE "Transaction_new"
RENAME TO "Transaction";

CREATE INDEX "Transaction_category_name_b54fe84e"
ON "Transaction" ("category_name");

CREATE INDEX "Transaction_cycle_id_78a7510b"
ON "Transaction" ("cycle_id");

PRAGMA foreign_keys=ON;
