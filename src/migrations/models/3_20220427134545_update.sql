-- upgrade --
ALTER TABLE "user" ADD "email" VARCHAR(128);
ALTER TABLE "user" DROP COLUMN "phone";
-- downgrade --
ALTER TABLE "user" ADD "phone" BIGINT;
ALTER TABLE "user" DROP COLUMN "email";
