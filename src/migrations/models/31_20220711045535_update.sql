-- upgrade --
CREATE TABLE IF NOT EXISTS "dealorder" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "deal_id" BIGINT NOT NULL REFERENCES "deal" ("id") ON DELETE CASCADE,
    "order_id" BIGINT NOT NULL REFERENCES "order" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "dealorder" IS 'The DealOrder model';
-- downgrade --
DROP TABLE IF EXISTS "dealorder";
