-- upgrade --
ALTER TABLE "strategy" ADD "v_minus" INT;
ALTER TABLE "strategy" RENAME COLUMN "profit_to_depoz" TO "profit_to_deposit";
ALTER TABLE "strategy" ADD "v_plus" INT;
ALTER TABLE "strategy" ADD "v_zero" INT;
ALTER TABLE "strategy" ADD "count_orders" INT;
ALTER TABLE "strategy" ADD "not_closed" INT;
ALTER TABLE "strategy" DROP COLUMN "profit_to_deal";
DROP TABLE IF EXISTS "resultstrategy";
-- downgrade --
ALTER TABLE "strategy" RENAME COLUMN "profit_to_deposit" TO "profit_to_depoz";
ALTER TABLE "strategy" RENAME COLUMN "profit_to_deposit" TO "profit_to_deal";
ALTER TABLE "strategy" DROP COLUMN "v_minus";
ALTER TABLE "strategy" DROP COLUMN "v_plus";
ALTER TABLE "strategy" DROP COLUMN "v_zero";
ALTER TABLE "strategy" DROP COLUMN "count_orders";
ALTER TABLE "strategy" DROP COLUMN "not_closed";
