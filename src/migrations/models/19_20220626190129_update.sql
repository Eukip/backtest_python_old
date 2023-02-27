-- upgrade --
CREATE TABLE IF NOT EXISTS "deal" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "formula" TEXT NOT NULL,
    "indicators" JSONB NOT NULL,
    "strategy_id" BIGINT NOT NULL REFERENCES "strategy" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "deal" IS 'The Deal model';
-- downgrade --
DROP TABLE IF EXISTS "deal";
