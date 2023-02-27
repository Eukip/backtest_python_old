-- upgrade --
CREATE TABLE IF NOT EXISTS "strategy" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(15) NOT NULL UNIQUE
);
COMMENT ON TABLE "strategy" IS 'The Strategy model';;
CREATE TABLE "strategy_order" ("strategy_id" BIGINT NOT NULL REFERENCES "order" ("id") ON DELETE CASCADE,"order_id" BIGINT NOT NULL REFERENCES "strategy" ("id") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "strategy_order";
DROP TABLE IF EXISTS "strategy";
