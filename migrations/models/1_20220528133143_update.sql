-- upgrade --
ALTER TABLE "subscription" ALTER COLUMN "description" DROP NOT NULL;
-- downgrade --
ALTER TABLE "subscription" ALTER COLUMN "description" SET NOT NULL;
