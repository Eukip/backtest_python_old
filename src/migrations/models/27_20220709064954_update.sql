-- upgrade --
ALTER TABLE "strategy" ADD "self_relation_master_key" INT;
-- downgrade --
ALTER TABLE "strategy" DROP COLUMN "self_relation_master_key";
