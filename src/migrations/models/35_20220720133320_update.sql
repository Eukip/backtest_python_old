-- upgrade --
ALTER TABLE "resultstrategy" DROP COLUMN "strategy_id";
-- downgrade --
ALTER TABLE "resultstrategy" ADD "strategy_id" BIGINT NOT NULL;
