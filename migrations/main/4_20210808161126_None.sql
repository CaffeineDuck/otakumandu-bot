-- upgrade --
CREATE TABLE IF NOT EXISTS "welcomes" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "channel" BIGINT NOT NULL UNIQUE,
    "message" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "color" INT NOT NULL  DEFAULT 7506394,
    "footer_image" TEXT
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
