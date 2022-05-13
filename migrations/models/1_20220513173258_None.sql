-- upgrade --
CREATE TABLE IF NOT EXISTS "admin" (
    "uid" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "surname" VARCHAR(256) NOT NULL,
    "pat_name" VARCHAR(512) NOT NULL,
    "date_birth" DATE NOT NULL,
    "gender" VARCHAR(1) NOT NULL,
    "series_passport" VARCHAR(4),
    "number_passport" VARCHAR(6),
    "phone" VARCHAR(20),
    "email" VARCHAR(512),
    "is_staff" BOOL NOT NULL  DEFAULT False,
    "is_superuser" BOOL NOT NULL  DEFAULT True
);
CREATE TABLE IF NOT EXISTS "gymlesson" (
    "uid" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "type" VARCHAR(12) NOT NULL  DEFAULT 'групповое',
    "duration" VARCHAR(256) NOT NULL
);
COMMENT ON COLUMN "gymlesson"."type" IS 'LESSON_GROUP: групповое\nLESSON_PERSONAL: персональное';
CREATE TABLE IF NOT EXISTS "office" (
    "uid" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "address" VARCHAR(2048) NOT NULL,
    "phone" VARCHAR(30) NOT NULL,
    "site" VARCHAR(512),
    "vk_url" VARCHAR(512),
    "facebook_url" VARCHAR(512),
    "instagram_url" VARCHAR(512),
    "description" TEXT
);
CREATE TABLE IF NOT EXISTS "gymroom" (
    "uid" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "description" TEXT NOT NULL,
    "office_id" UUID NOT NULL REFERENCES "office" ("uid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "subscription" (
    "uid" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "quantity_gym_lesson" INT NOT NULL,
    "quantity_day" INT NOT NULL,
    "price" INT NOT NULL,
    "description" TEXT NOT NULL,
    "gym_lesson_id" UUID NOT NULL REFERENCES "gymlesson" ("uid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "trainer" (
    "uid" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "surname" VARCHAR(256) NOT NULL,
    "pat_name" VARCHAR(512) NOT NULL,
    "date_birth" DATE NOT NULL,
    "gender" VARCHAR(1) NOT NULL,
    "series_passport" VARCHAR(4),
    "number_passport" VARCHAR(6),
    "phone" VARCHAR(20),
    "email" VARCHAR(512),
    "is_staff" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "profile" (
    "uid" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "surname" VARCHAR(256) NOT NULL,
    "pat_name" VARCHAR(512) NOT NULL,
    "date_birth" DATE NOT NULL,
    "gender" VARCHAR(1) NOT NULL,
    "series_passport" VARCHAR(4),
    "number_passport" VARCHAR(6),
    "phone" VARCHAR(20),
    "email" VARCHAR(512),
    "is_staff" BOOL NOT NULL  DEFAULT False,
    "trainer_id" UUID  UNIQUE REFERENCES "trainer" ("uid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "purchasedsubscription" (
    "uid" UUID NOT NULL  PRIMARY KEY,
    "date_sale" DATE NOT NULL,
    "date_activation" DATE NOT NULL,
    "date_endings" DATE NOT NULL,
    "client_id" UUID NOT NULL REFERENCES "profile" ("uid") ON DELETE CASCADE,
    "office_id" UUID NOT NULL REFERENCES "office" ("uid") ON DELETE CASCADE,
    "subscription_id" UUID NOT NULL REFERENCES "subscription" ("uid") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
