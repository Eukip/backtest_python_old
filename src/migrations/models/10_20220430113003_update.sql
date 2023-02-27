-- upgrade --
DROP TABLE IF EXISTS "strategy_order";
CREATE TABLE IF NOT EXISTS "strategyorder" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "order_id" BIGINT NOT NULL REFERENCES "order" ("id") ON DELETE CASCADE,
    "strategy_id" BIGINT NOT NULL REFERENCES "strategy" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "strategyorder" IS 'The StrategyOrder model';-- downgrade --
DROP TABLE IF EXISTS "strategyorder";
CREATE TABLE "strategy_order" ("order_id" BIGINT NOT NULL REFERENCES "order" ("id") ON DELETE CASCADE,"strategy_id" BIGINT NOT NULL REFERENCES "strategy" ("id") ON DELETE CASCADE);
