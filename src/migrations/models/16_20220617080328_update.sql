-- upgrade --
ALTER TABLE "strategy" ADD "master_id" BIGINT NOT NULL;
CREATE TABLE IF NOT EXISTS "masterstrategy" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(15) NOT NULL UNIQUE,
    "formula" TEXT NOT NULL
);
COMMENT ON TABLE "masterstrategy" IS 'The MasterStrategy model';;
ALTER TABLE "strategy" ADD CONSTRAINT "fk_strategy_masterst_c892f5dc" FOREIGN KEY ("master_id") REFERENCES "masterstrategy" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "strategy" DROP CONSTRAINT "fk_strategy_masterst_c892f5dc";
ALTER TABLE "strategy" DROP COLUMN "master_id";
DROP TABLE IF EXISTS "masterstrategy";
