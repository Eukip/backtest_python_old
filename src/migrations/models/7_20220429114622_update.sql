-- upgrade --
ALTER TABLE "order" ADD "is_active" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "order" DROP COLUMN "is_active";
