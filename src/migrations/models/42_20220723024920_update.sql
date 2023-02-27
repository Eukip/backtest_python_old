-- upgrade --
ALTER TABLE "order" ADD "seconds_in_order" INT;
-- downgrade --
ALTER TABLE "order" DROP COLUMN "seconds_in_order";
