from django.db import models
import ast
import json
import django
from django.core.serializers.json import DjangoJSONEncoder

'''
Taken from https://stackoverflow.com/questions/5216162/how-to-create-list-field-in-django#7394475
Modified to work with Django 2.0.
'''
class ListField(models.TextField):
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


'''
Taken from https://github.com/skorokithakis/django-annoying

License:
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the 
following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following 
      disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the 
      following disclaimer in the documentation and/or other materials provided with the distribution.
    * Neither the name of the author nor the names of its contributors may be used to endorse or promote products 
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE 
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
class JSONField(models.TextField):
    """
    JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly.
    Django snippet #1478
    Custom serializer/deserializer functions can be used to customize field's behavior.
    Defaults:
     - serializer: json.dumps(value, cls=DjangoJSONEncoder, sort_keys=True, indent=2, separators=(',', ': '))
     - deserializer: json.loads(value)
    example:
        class Page(models.Model):
            data = JSONField(blank=True, null=True)
        page = Page.objects.get(pk=5)
        page.data = {'title': 'test', 'type': 3}
        page.save()
    """

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer', dumps)
        self.deserializer = kwargs.pop('deserializer', json.loads)

        super(JSONField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(JSONField, self).deconstruct()
        kwargs['serializer'] = self.serializer
        kwargs['deserializer'] = self.deserializer
        return name, path, args, kwargs

    def to_python(self, value):
        """
        Convert a string from the database to a Python value.
        """
        if value == "":
            return None

        try:
            if isinstance(value, six.string_types):
                return self.deserializer(value)
            elif isinstance(value, bytes):
                return self.deserializer(value.decode('utf8'))
        except ValueError:
            pass
        return value

    def get_prep_value(self, value):
        """
        Convert the value to a string so it can be stored in the database.
        """
        if value == "":
            return None
        if isinstance(value, (dict, list)):
            return self.serializer(value)
        return super(JSONField, self).get_prep_value(value)

    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def get_default(self):
        # Override Django's `get_default()` to avoid stringification.
        if self.has_default():
            return self.default() if callable(self.default) else self.default
        return ""

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, (dict, list)):
            return self.serializer(value)
        else:
            return super(JSONField,
                         self).get_db_prep_save(value, *args, **kwargs)

    def value_from_object(self, obj):
        value = super(JSONField, self).value_from_object(obj)
        if self.null and value is None:
            return None
        return self.serializer(value)