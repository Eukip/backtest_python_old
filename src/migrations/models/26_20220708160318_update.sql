-- upgrade --
ALTER TABLE "strategy" ADD "self_relation_master_id" BIGINT;
ALTER TABLE "strategy" ADD "png_from_xmind_output" TEXT;
ALTER TABLE "strategy" ADD "png_from_xmind_input" TEXT;
ALTER TABLE "strategy" ADD CONSTRAINT "fk_strategy_strategy_48021a78" FOREIGN KEY ("self_relation_master_id") REFERENCES "strategy" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "strategy" DROP CONSTRAINT "fk_strategy_strategy_48021a78";
ALTER TABLE "strategy" DROP COLUMN "self_relation_master_id";
ALTER TABLE "strategy" DROP COLUMN "png_from_xmind_output";
ALTER TABLE "strategy" DROP COLUMN "png_from_xmind_input";
