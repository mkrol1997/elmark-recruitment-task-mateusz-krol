from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    StringField,
)
from rest_framework.serializers import ValidationError


class Categories(Document):
    name = StringField(
        required=True,
        null=False,
        unique=True,
    )
    parent_name = StringField(required=True, null=True, default="")

    def clean(self):
        if self.name == self.parent_name:
            raise ValidationError("Name and parent_name can not be equal.")
        return super().clean()


class PartLocation(EmbeddedDocument):
    room = StringField(required=True, null=False)
    bookcase = IntField(min_value=0, required=True, null=False)
    shelf = IntField(min_value=0, required=True, null=False)
    cuvette = IntField(min_value=0, required=True, null=False)
    column = IntField(min_value=0, required=True, null=False)
    row = IntField(min_value=0, required=True, null=False)


class Parts(Document):
    serial_number = StringField(required=True, unique=True, null=False)
    name = StringField(required=True, null=False)
    description = StringField(required=True, null=False)
    category = StringField(required=True, null=False)
    quantity = IntField(min_value=0, required=True, null=False)
    price = FloatField(min_value=0, required=True, null=False)
    location = EmbeddedDocumentField(PartLocation)

    meta = {
        "ordering": ["serial_number", "name", "description", "category", "quantity", "price", "location"],
    }
