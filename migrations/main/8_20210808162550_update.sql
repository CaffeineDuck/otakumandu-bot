-- upgrade --
CREATE UNIQUE INDEX "uid_welcomes_guild_i_44687e" ON "welcomes" ("guild_id");
-- downgrade --
DROP INDEX "idx_welcomes_guild_i_44687e";
