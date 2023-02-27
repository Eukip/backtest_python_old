-- upgrade --
ALTER TABLE "resultstrategy" ADD "strategy_id" BIGINT  UNIQUE;
-- downgrade --
ALTER TABLE "resultstrategy" DROP COLUMN "strategy_id";
