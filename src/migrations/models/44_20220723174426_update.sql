-- upgrade --
ALTER TABLE "strategy" ADD "profit_cer_period" DOUBLE PRECISION   DEFAULT 22.22;
-- downgrade --
ALTER TABLE "strategy" DROP COLUMN "profit_cer_period";
