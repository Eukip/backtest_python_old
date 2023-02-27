-- upgrade --
ALTER TABLE "strategy" ALTER COLUMN "name" TYPE VARCHAR(25) USING "name"::VARCHAR(25);
-- downgrade --
ALTER TABLE "strategy" ALTER COLUMN "name" TYPE VARCHAR(15) USING "name"::VARCHAR(15);
