-- upgrade --
ALTER TABLE "strategy" ALTER COLUMN "archived" SET NOT NULL;
-- downgrade --
ALTER TABLE "strategy" ALTER COLUMN "archived" DROP NOT NULL;
