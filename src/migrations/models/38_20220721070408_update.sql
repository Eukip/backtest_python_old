-- upgrade --
ALTER TABLE "timeinterval" ADD "master_time_id" BIGINT;
ALTER TABLE "timeinterval" ADD CONSTRAINT "fk_timeinte_masterti_58497c8d" FOREIGN KEY ("master_time_id") REFERENCES "mastertimeinterval" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "timeinterval" DROP CONSTRAINT "fk_timeinte_masterti_58497c8d";
ALTER TABLE "timeinterval" DROP COLUMN "master_time_id";
