-- upgrade --
ALTER TABLE "strategy" ADD "deposit_limit" INT   DEFAULT 10;
-- downgrade --
ALTER TABLE "strategy" DROP COLUMN "deposit_limit";
