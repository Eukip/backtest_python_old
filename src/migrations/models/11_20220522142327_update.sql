-- upgrade --
CREATE TABLE IF NOT EXISTS "resultstrategy" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "count_orders" INT ,
    "v_minus" INT,
    "v_plus" INT,
    "v_zero" INT,
    "not_closed" INT,
    "profit" INT,
    "strategy_id" BIGINT NOT NULL REFERENCES "strategy" ("id") ON DELETE CASCADE
);

COMMENT ON TABLE "resultstrategy" IS 'The ResultStrategy model';

-- downgrade --
DROP TABLE IF EXISTS "resultstrategy";
