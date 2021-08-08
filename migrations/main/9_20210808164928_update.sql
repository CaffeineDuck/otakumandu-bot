-- upgrade --
ALTER TABLE "welcomes" ADD "footer_text" TEXT;
ALTER TABLE "welcomes" ADD "image_thumbnail" TEXT;
ALTER TABLE "welcomes" ADD "image" TEXT;
-- downgrade --
ALTER TABLE "welcomes" DROP COLUMN "footer_text";
ALTER TABLE "welcomes" DROP COLUMN "image_thumbnail";
ALTER TABLE "welcomes" DROP COLUMN "image";
