-- upgrade --
ALTER TABLE "order" ADD "predicted_time" TIMESTAMPTZ;
ALTER TABLE "order" ALTER COLUMN "status" TYPE VARCHAR(17) USING "status"::VARCHAR(17);
-- downgrade --
ALTER TABLE "order" DROP COLUMN "predicted_time";
ALTER TABLE "order" ALTER COLUMN "status" TYPE BOOL USING "status"::BOOL;
