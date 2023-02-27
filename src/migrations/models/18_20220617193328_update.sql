-- upgrade --
ALTER TABLE "strategy" ALTER COLUMN "master_id" DROP NOT NULL;
-- downgrade --
ALTER TABLE "strategy" ALTER COLUMN "master_id" SET NOT NULL;
