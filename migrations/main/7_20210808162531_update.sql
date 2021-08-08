-- upgrade --
ALTER TABLE "welcomes" RENAME COLUMN "guild_id" TO "id";
ALTER TABLE "welcomes" ADD "guild_id" BIGINT NOT NULL;
-- downgrade --
ALTER TABLE "welcomes" RENAME COLUMN "id" TO "guild_id";
ALTER TABLE "welcomes" DROP COLUMN "guild_id";
