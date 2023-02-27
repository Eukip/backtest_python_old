-- upgrade --
ALTER TABLE "strategy" ALTER COLUMN "formula" DROP NOT NULL;
-- downgrade --
ALTER TABLE "strategy" ALTER COLUMN "formula" SET NOT NULL;
