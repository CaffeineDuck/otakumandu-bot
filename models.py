from tortoise import Model, fields


class WelcomeModel(Model):
    id = fields.IntField(pk=True)
    guild_id = fields.BigIntField(unique=True)
    channel = fields.BigIntField(unique=True)
    message = fields.TextField()
    title = fields.TextField()
    color = fields.IntField(null=True)
    footer_image = fields.TextField(null=True)
    footer_text = fields.TextField(null=True)
    image_thumbnail = fields.TextField(null=True)
    image = fields.TextField(null=True)

    class Meta:
        table = "welcomes"
        description = "Contains data about welcome message configuration"


class InviteModel(Model):
    code = fields.TextField(pk=True)
    inviter = fields.BigIntField()
    uses = fields.IntField(default=0)

    class Meta:
        table = "invites"
        description = "Contains data about user invites and their uses"
