-- upgrade --
ALTER TABLE "order" ADD "time_in_order_field" INT;
-- downgrade --
ALTER TABLE "order" DROP COLUMN "time_in_order_field";
