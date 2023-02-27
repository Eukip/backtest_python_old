-- upgrade --
ALTER TABLE "strategy" DROP COLUMN "formula";
-- downgrade --
ALTER TABLE "strategy" ADD "formula" TEXT;
