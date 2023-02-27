-- upgrade --
CREATE TABLE IF NOT EXISTS "timeinterval" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "datetime_from" TIMESTAMPTZ NOT NULL,
    "datetime_to" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "timeinterval" IS 'The TimeFrame model';;
CREATE TABLE IF NOT EXISTS "mastertimeinterval" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL
);
COMMENT ON TABLE "mastertimeinterval" IS 'The MasterTimeFrame model';;
DROP TABLE IF EXISTS "timeframe";
DROP TABLE IF EXISTS "mastertimeframe";
-- downgrade --
DROP TABLE IF EXISTS "timeinterval";
DROP TABLE IF EXISTS "mastertimeinterval";
