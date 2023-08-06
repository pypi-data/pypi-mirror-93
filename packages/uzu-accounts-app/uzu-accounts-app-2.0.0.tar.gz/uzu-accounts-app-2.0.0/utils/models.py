from django.db import models
from hashlib import sha256
from .shortcuts import update_obj

class PasswordField(models.CharField):
    def __init__(self, **kwargs):
        self.char_field = models.CharField(editable=False, max_length=64, **kwargs)
    
    def __get__(self, instance, owner):
        return self.char_field
    
    def __set__(self, instance, value):
        hasher = sha256()
        hasher.update(value)
        self.char_field = hasher.hexdigest()

    def __eq__(self, other):
        if other is PasswordField:
            return self.char_field == other.char_field
        else:
            hasher = sha256()
            hasher.update(other)
            return self.char_field == hasher.hexdigest()
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __getattribute__(self, name):
        return object.__getattribute__(self, "char_field").__getattribute__(name)

class ModelMixin():
    Fillable = set([])
    Guarded = set([])

    def update(self, **data):
        data = self._strip_dict(data)
        if len(data) < 1:
            raise Exception('Invalid update data')
        update_obj(self, data)
        self.save()

    def _strip_dict(self, data):
        data = self._strip_empty(data)
        data = self._remove_nonfillable(data)
        data = self._strip_guarded(data)
        return data

    def _remove_nonfillable(self, data):
        if not self.__class__.Fillable:
            return data
        for key in list(data.keys()):
            if key not in self.__class__.Fillable:
                data.pop(key)
        return data

    def _strip_empty(self, data):
        for key in list(data.keys()):
            if not data[key]:
                data.pop(key)
        return data

    def _strip_guarded(self, data):
        if not self.__class__.Guarded:
            return data
        for key in list(data.keys()):
            if key in self.__class__.Guarded:
                data.pop(key)
        return data