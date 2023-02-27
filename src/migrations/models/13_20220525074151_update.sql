-- upgrade --
ALTER TABLE "strategy" ADD "formula" TEXT NOT NULL;
-- downgrade --
ALTER TABLE "strategy" DROP COLUMN "formula";
