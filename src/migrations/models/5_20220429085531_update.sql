-- upgrade --
ALTER TABLE "order" ADD "close_time" TIMESTAMPTZ NOT NULL;
ALTER TABLE "order" ADD "open_time" TIMESTAMPTZ NOT NULL;
-- downgrade --
ALTER TABLE "order" DROP COLUMN "close_time";
ALTER TABLE "order" DROP COLUMN "open_time";
