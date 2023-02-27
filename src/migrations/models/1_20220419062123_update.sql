-- upgrade --
CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "login" VARCHAR(128),
    "phone" BIGINT,
    "password" VARCHAR(128) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "user" IS 'The User model';
-- downgrade --
DROP TABLE IF EXISTS "user";
