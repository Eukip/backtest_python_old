-- upgrade --
ALTER TABLE "timeframe" ADD "master_time_id" BIGINT;
ALTER TABLE "timeframe" DROP COLUMN "name";
CREATE TABLE IF NOT EXISTS "mastertimeframe" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL
);
COMMENT ON TABLE "mastertimeframe" IS 'The MasterTimeFrame model';;
ALTER TABLE "timeframe" ADD CONSTRAINT "fk_timefram_masterti_3334a328" FOREIGN KEY ("master_time_id") REFERENCES "mastertimeframe" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "timeframe" DROP CONSTRAINT "fk_timefram_masterti_3334a328";
ALTER TABLE "timeframe" ADD "name" VARCHAR(128) NOT NULL;
ALTER TABLE "timeframe" DROP COLUMN "master_time_id";
DROP TABLE IF EXISTS "mastertimeframe";
