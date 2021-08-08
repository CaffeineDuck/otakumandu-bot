-- upgrade --
ALTER TABLE "welcomes" RENAME COLUMN "id" TO "guild_model";
-- downgrade --
ALTER TABLE "welcomes" RENAME COLUMN "guild_model" TO "id";
