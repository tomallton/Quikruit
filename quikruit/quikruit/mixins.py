from django.db import models
from django.utils.crypto import get_random_string
import string

def _id_gen(length=15):
    allowed_chars = string.ascii_lowercase + string.digits
    return get_random_string(length, allowed_chars)
def id_gen():
    return _id_gen(15)

class StringBasedModelIDMixin(models.Model):
    model_id = models.CharField(
        max_length=9,
        unique=True,
        default=id_gen,
        primary_key=True,
        editable=False
    )

    class Meta:
        abstract = True