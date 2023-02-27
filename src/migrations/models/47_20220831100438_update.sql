-- upgrade --
ALTER TABLE "symbols" RENAME COLUMN "exchange_id_id" TO "exchange_id";
-- downgrade --
ALTER TABLE "symbols" RENAME COLUMN "exchange_id" TO "exchange_id_id";
