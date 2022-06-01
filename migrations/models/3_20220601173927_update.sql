-- upgrade --
CREATE TABLE IF NOT EXISTS "service" (
    "uid" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL,
    "price" INT NOT NULL,
    "description" TEXT
);
CREATE TABLE IF NOT EXISTS "purchasedservice" (
    "uid" UUID NOT NULL  PRIMARY KEY,
    "date_sale" DATE NOT NULL  DEFAULT '2022-06-01T17:39:27.073410',
    "client_id" UUID NOT NULL REFERENCES "profile" ("uid") ON DELETE CASCADE,
    "service_id" UUID NOT NULL REFERENCES "service" ("uid") ON DELETE RESTRICT
);;
ALTER TABLE "purchasedsubscription" ALTER COLUMN "date_sale" SET DEFAULT '2022-06-01 17:39:27.065361';
-- downgrade --
ALTER TABLE "purchasedsubscription" ALTER COLUMN "date_sale" SET DEFAULT '2022-06-01 11:29:55.054213';
DROP TABLE IF EXISTS "purchasedservice";
DROP TABLE IF EXISTS "service";
