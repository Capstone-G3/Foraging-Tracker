from django.db.models import Model, AutoField, CharField, ForeignKey, CASCADE

from foraging_app.models import user


class Group(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=120, unique=True, null=False)
    category = CharField(max_length=120, null=False)
    description = CharField(max_length=512)
    user_admin = ForeignKey('foraging_app.user', on_delete=CASCADE, null=False)


    def save(self, **kwargs):
        super().save(**kwargs)

    def delete(self, **kwargs):
        super().delete(**kwargs)

    def __str__(self) -> str:
        return self.name

    def getAdmin(self): # -> user.User: circular issue
        return self.user_admin