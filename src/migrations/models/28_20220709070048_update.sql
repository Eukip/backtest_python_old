-- upgrade --
ALTER TABLE "strategy" DROP CONSTRAINT "fk_strategy_strategy_48021a78";
ALTER TABLE "strategy" DROP COLUMN "self_relation_master_id";
-- downgrade --
ALTER TABLE "strategy" ADD "self_relation_master_id" BIGINT;
ALTER TABLE "strategy" ADD CONSTRAINT "fk_strategy_strategy_48021a78" FOREIGN KEY ("self_relation_master_id") REFERENCES "strategy" ("id") ON DELETE CASCADE;
