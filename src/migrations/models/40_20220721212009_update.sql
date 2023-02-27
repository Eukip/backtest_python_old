-- upgrade --
ALTER TABLE "strategy" DROP CONSTRAINT "fk_strategy_strategy_19c9f66a";
ALTER TABLE "strategy" RENAME COLUMN "self_id" TO "self_master_id";
ALTER TABLE "strategy" ADD CONSTRAINT "fk_strategy_strategy_182d88b9" FOREIGN KEY ("self_master_id") REFERENCES "strategy" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "strategy" DROP CONSTRAINT "fk_strategy_strategy_182d88b9";
ALTER TABLE "strategy" RENAME COLUMN "self_master_id" TO "self_id";
ALTER TABLE "strategy" ADD CONSTRAINT "fk_strategy_strategy_19c9f66a" FOREIGN KEY ("self_id") REFERENCES "strategy" ("id") ON DELETE CASCADE;
