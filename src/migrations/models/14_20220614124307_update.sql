-- upgrade --
ALTER TABLE "order" ADD "profit_to_deposit" INT;
ALTER TABLE "order" ADD "profit_cer_period" INT;
ALTER TABLE "order" ADD "absolute_profit" INT;
ALTER TABLE "order" ADD "deep" DOUBLE PRECISION;
CREATE TABLE IF NOT EXISTS "timeframe" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "datetime_from" TIMESTAMPTZ NOT NULL,
    "datetime_to" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "timeframe" IS 'The TimeFrame model';-- downgrade --
ALTER TABLE "order" DROP COLUMN "profit_to_deposit";
ALTER TABLE "order" DROP COLUMN "profit_cer_period";
ALTER TABLE "order" DROP COLUMN "absolute_profit";
ALTER TABLE "order" DROP COLUMN "deep";
DROP TABLE IF EXISTS "timeframe";
