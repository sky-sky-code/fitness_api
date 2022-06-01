-- upgrade --
ALTER TABLE "purchasedsubscription" ALTER COLUMN "date_sale" SET DEFAULT '2022-06-01 11:29:43.959770';
-- downgrade --
ALTER TABLE "purchasedsubscription" ALTER COLUMN "date_sale" DROP DEFAULT;
