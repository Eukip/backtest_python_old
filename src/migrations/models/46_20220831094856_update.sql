-- upgrade --
CREATE TABLE IF NOT EXISTS "exchange" (
    "exchange_id" VARCHAR(127) NOT NULL  PRIMARY KEY,
    "website" VARCHAR(55),
    "name" VARCHAR(55),
    "data_symbols_count" INT
);;
CREATE TABLE IF NOT EXISTS "symbols" (
    "symbol_id" VARCHAR(127) NOT NULL  PRIMARY KEY,
    "symbol_type" VARCHAR(55),
    "asset_id_base" VARCHAR(55),
    "asset_id_quote" VARCHAR(55),
    "asset_id_unit" VARCHAR(55),
    "data_start" VARCHAR(55),
    "data_end" VARCHAR(55),
    "data_quote_start" VARCHAR(100),
    "data_quote_end" VARCHAR(100),
    "quantity_broken_candles" BIGINT,
    "exchange_id_id" VARCHAR(127) NOT NULL REFERENCES "exchange" ("exchange_id") ON DELETE CASCADE
);-- downgrade --
DROP TABLE IF EXISTS "exchange";
DROP TABLE IF EXISTS "symbols";
