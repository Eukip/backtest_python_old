-- upgrade --
ALTER TABLE "order" DROP COLUMN "direction";
-- downgrade --
ALTER TABLE "order" ADD "direction" VARCHAR(4) NOT NULL;
