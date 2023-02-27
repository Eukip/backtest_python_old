-- upgrade --
ALTER TABLE "order" ADD "status" BOOL;
ALTER TABLE "order" ADD "base_price" DOUBLE PRECISION;
-- downgrade --
ALTER TABLE "order" DROP COLUMN "status";
ALTER TABLE "order" DROP COLUMN "base_price";
