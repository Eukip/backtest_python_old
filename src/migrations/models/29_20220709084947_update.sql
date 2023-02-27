-- upgrade --
ALTER TABLE "strategy" DROP CONSTRAINT "fk_strategy_masterst_c892f5dc";
ALTER TABLE "strategy" RENAME COLUMN "master_id" TO "self_id";
DROP TABLE IF EXISTS "dealorder";
DROP TABLE IF EXISTS "masterstrategy";
ALTER TABLE "strategy" ADD CONSTRAINT "fk_strategy_strategy_19c9f66a" FOREIGN KEY ("self_id") REFERENCES "strategy" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "strategy" DROP CONSTRAINT "fk_strategy_strategy_19c9f66a";
ALTER TABLE "strategy" RENAME COLUMN "self_id" TO "master_id";
ALTER TABLE "strategy" ADD CONSTRAINT "fk_strategy_masterst_c892f5dc" FOREIGN KEY ("master_id") REFERENCES "masterstrategy" ("id") ON DELETE CASCADE;
