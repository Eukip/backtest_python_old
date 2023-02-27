-- upgrade --
ALTER TABLE "strategy" DROP COLUMN "self_relation_master_key";
-- downgrade --
ALTER TABLE "strategy" ADD "self_relation_master_key" INT;
