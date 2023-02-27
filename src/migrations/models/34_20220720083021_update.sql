-- upgrade --
ALTER TABLE "strategy" ADD "moment_max_drawdown" INT   DEFAULT -123;
ALTER TABLE "strategy" ADD "all_order_max_drawdown" INT   DEFAULT -123;
ALTER TABLE "strategy" RENAME COLUMN "deal_depth" TO "deal_depth_3";
ALTER TABLE "strategy" ADD "archived" BOOL   DEFAULT False;
ALTER TABLE "strategy" ADD "deal_depth_1" DOUBLE PRECISION;
ALTER TABLE "strategy" ADD "deal_depth_2" DOUBLE PRECISION;
-- downgrade --
ALTER TABLE "strategy" RENAME COLUMN "deal_depth_3" TO "deal_depth";
ALTER TABLE "strategy" DROP COLUMN "moment_max_drawdown";
ALTER TABLE "strategy" DROP COLUMN "all_order_max_drawdown";
ALTER TABLE "strategy" DROP COLUMN "archived";
ALTER TABLE "strategy" DROP COLUMN "deal_depth_1";
ALTER TABLE "strategy" DROP COLUMN "deal_depth_2";
