-- upgrade --
ALTER TABLE "welcomes" RENAME COLUMN "guild_model" TO "guild_id";
-- downgrade --
ALTER TABLE "welcomes" RENAME COLUMN "guild_id" TO "guild_model";
