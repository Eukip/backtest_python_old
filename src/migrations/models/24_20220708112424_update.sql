-- upgrade --
ALTER TABLE "order" ADD "formula_id" BIGINT;
ALTER TABLE "order" ADD "deal_id" BIGINT;
ALTER TABLE "strategy" ADD "profit_to_deal" DOUBLE PRECISION   DEFAULT 22.22;
ALTER TABLE "strategy" ADD "profit_to_depoz" DOUBLE PRECISION   DEFAULT 22.22;
ALTER TABLE "strategy" ADD "absolute_profit" DOUBLE PRECISION   DEFAULT 0.02;
ALTER TABLE "masterstrategy" ADD "png_from_xmind_input" TEXT;
ALTER TABLE "masterstrategy" ADD "png_from_xmind_output" TEXT;
CREATE TABLE IF NOT EXISTS "formula" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100),
    "formula" TEXT,
    "deal_id" BIGINT REFERENCES "deal" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "formula" IS 'The Deal model';;
ALTER TABLE "order" ADD CONSTRAINT "fk_order_formula_6ec0699e" FOREIGN KEY ("formula_id") REFERENCES "formula" ("id") ON DELETE CASCADE;
ALTER TABLE "order" ADD CONSTRAINT "fk_order_deal_f54d2a37" FOREIGN KEY ("deal_id") REFERENCES "deal" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "order" DROP CONSTRAINT "fk_order_deal_f54d2a37";
ALTER TABLE "order" DROP CONSTRAINT "fk_order_formula_6ec0699e";
ALTER TABLE "order" DROP COLUMN "formula_id";
ALTER TABLE "order" DROP COLUMN "deal_id";
ALTER TABLE "strategy" DROP COLUMN "profit_to_deal";
ALTER TABLE "strategy" DROP COLUMN "profit_to_depoz";
ALTER TABLE "strategy" DROP COLUMN "absolute_profit";
ALTER TABLE "masterstrategy" DROP COLUMN "png_from_xmind_input";
ALTER TABLE "masterstrategy" DROP COLUMN "png_from_xmind_output";
DROP TABLE IF EXISTS "formula";
