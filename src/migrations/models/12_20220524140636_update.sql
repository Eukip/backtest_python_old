-- upgrade --
ALTER TABLE "pair" DROP COLUMN "trading_pair";
ALTER TABLE "pair" DROP COLUMN "market";
ALTER TABLE "pair" ADD "trading_pair" VARCHAR(15) NOT NULL;
ALTER TABLE "pair" ADD "market" VARCHAR(25) NOT NULL;
ALTER TABLE "pair" ADD UNIQUE("trading_pair", "market");
-- downgrade --

