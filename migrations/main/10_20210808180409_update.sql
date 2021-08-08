-- upgrade --
ALTER TABLE "welcomes" ALTER COLUMN "color" DROP DEFAULT;
ALTER TABLE "welcomes" ALTER COLUMN "color" DROP NOT NULL;
-- downgrade --
ALTER TABLE "welcomes" ALTER COLUMN "color" SET NOT NULL;
ALTER TABLE "welcomes" ALTER COLUMN "color" SET DEFAULT 7506394;
