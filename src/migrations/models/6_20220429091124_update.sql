-- upgrade --
ALTER TABLE "order" ALTER COLUMN "amount" TYPE DOUBLE PRECISION USING "amount"::DOUBLE PRECISION;
ALTER TABLE "order" ALTER COLUMN "close_price" DROP NOT NULL;
ALTER TABLE "order" ALTER COLUMN "close_time" DROP NOT NULL;
-- downgrade --
ALTER TABLE "order" ALTER COLUMN "amount" TYPE BIGINT USING "amount"::BIGINT;
ALTER TABLE "order" ALTER COLUMN "close_price" SET NOT NULL;
ALTER TABLE "order" ALTER COLUMN "close_time" SET NOT NULL;
