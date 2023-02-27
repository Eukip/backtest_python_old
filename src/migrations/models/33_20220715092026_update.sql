-- upgrade --

ALTER TABLE "order" DROP COLUMN "is_active";
-- downgrade --
ALTER TABLE "order" ADD "is_active" BOOL;
