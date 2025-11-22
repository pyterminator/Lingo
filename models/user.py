from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField(unique=True)

    username = fields.CharField(max_length=255, null=True, unique=True)
    email = fields.CharField(max_length=255, null=True, unique=True)
    
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)

    language_code = fields.CharField(max_length=10, null=True)

    is_bot = fields.BooleanField(default=False)
    
    level = fields.IntField(default=1)
    score = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"