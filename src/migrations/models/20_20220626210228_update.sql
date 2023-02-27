-- upgrade --
ALTER TABLE "strategy" ADD "daily_turnover_to" INT;
ALTER TABLE "strategy" ADD "base" VARCHAR(5);
ALTER TABLE "strategy" ADD "daily_turnover_from" INT;
ALTER TABLE "strategy" ADD "deal_depth" DOUBLE PRECISION;
-- downgrade --
ALTER TABLE "strategy" DROP COLUMN "daily_turnover_to";
ALTER TABLE "strategy" DROP COLUMN "base";
ALTER TABLE "strategy" DROP COLUMN "daily_turnover_from";
ALTER TABLE "strategy" DROP COLUMN "deal_depth";
