-- upgrade --
CREATE TABLE IF NOT EXISTS "pair" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "trading_pair" VARCHAR(15) NOT NULL UNIQUE,
    "market" VARCHAR(25) NOT NULL UNIQUE
);
COMMENT ON TABLE "pair" IS 'The Pair model';;
CREATE TABLE IF NOT EXISTS "order" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "direction" VARCHAR(4) NOT NULL,
    "open_price" DOUBLE PRECISION NOT NULL,
    "amount" BIGINT NOT NULL,
    "close_price" DOUBLE PRECISION NOT NULL,
    "pair_id" BIGINT NOT NULL REFERENCES "pair" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "order"."direction" IS 'buy: BUY\nsell: SELL';
COMMENT ON TABLE "order" IS 'The Order model';-- downgrade --
DROP TABLE IF EXISTS "pair";
DROP TABLE IF EXISTS "order";
