-- upgrade --
ALTER TABLE "order" ALTER COLUMN "profit_cer_period" TYPE DOUBLE PRECISION USING "profit_cer_period"::DOUBLE PRECISION;
ALTER TABLE "order" ALTER COLUMN "profit_to_deposit" TYPE DOUBLE PRECISION USING "profit_to_deposit"::DOUBLE PRECISION;
ALTER TABLE "order" ALTER COLUMN "absolute_profit" TYPE DOUBLE PRECISION USING "absolute_profit"::DOUBLE PRECISION;
ALTER TABLE "resultstrategy" ADD "profit_cer_period" DOUBLE PRECISION;
ALTER TABLE "resultstrategy" ADD "profit_to_deposit" DOUBLE PRECISION;
ALTER TABLE "resultstrategy" ADD "absolute_profit" DOUBLE PRECISION;
ALTER TABLE "resultstrategy" DROP COLUMN "profit";
-- downgrade --
ALTER TABLE "order" ALTER COLUMN "profit_cer_period" TYPE INT USING "profit_cer_period"::INT;
ALTER TABLE "order" ALTER COLUMN "profit_to_deposit" TYPE INT USING "profit_to_deposit"::INT;
ALTER TABLE "order" ALTER COLUMN "absolute_profit" TYPE INT USING "absolute_profit"::INT;
ALTER TABLE "resultstrategy" ADD "profit" INT;
ALTER TABLE "resultstrategy" DROP COLUMN "profit_cer_period";
ALTER TABLE "resultstrategy" DROP COLUMN "profit_to_deposit";
ALTER TABLE "resultstrategy" DROP COLUMN "absolute_profit";
