-- upgrade --
ALTER TABLE "masterstrategy" ALTER COLUMN "formula" DROP NOT NULL;
-- downgrade --
ALTER TABLE "masterstrategy" ALTER COLUMN "formula" SET NOT NULL;
