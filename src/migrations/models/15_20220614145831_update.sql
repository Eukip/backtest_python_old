-- upgrade --
ALTER TABLE "order" ADD "base" TEXT;
-- downgrade --
ALTER TABLE "order" DROP COLUMN "base";
