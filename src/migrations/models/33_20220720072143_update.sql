-- upgrade --
ALTER TABLE "order" DROP COLUMN "time_in_order_field";
-- downgrade --
ALTER TABLE "order" ADD "time_in_order_field" INT;
