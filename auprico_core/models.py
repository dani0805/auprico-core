import traceback

import sys
from django.db import models
from django.utils.timezone import now as django_now

# Create your models here.
from django.db.models import PROTECT
from django.utils.translation import ugettext_lazy


class System(models.Model):
    parameter_name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Parameter Name"))
    parameter_value = models.CharField(max_length=4000, verbose_name=ugettext_lazy("Parameter Value"))


class Log(models.Model):
    module = models.CharField(max_length=200, verbose_name=ugettext_lazy("Module"))
    log_level = models.IntegerField(verbose_name=ugettext_lazy("Log Level"))
    text = models.TextField(max_length=60000, verbose_name=ugettext_lazy("Text"))
    created_ts = models.DateTimeField(auto_now_add=True, verbose_name=ugettext_lazy("Created On"))

    ERROR = 3
    WARN = 2
    INFO = 1
    DEBUG = 0

    @staticmethod
    def error(*, module: str, text: str):
        Log.log(module=module, text=text, level=Log.ERROR)

    @staticmethod
    def warn(*, module: str, text: str):
        Log.log(module=module, text=text, level=Log.WARN)

    @staticmethod
    def debug(*, module: str, text: str):
        Log.log(module=module, text=text, level=Log.DEBUG)

    @staticmethod
    def info(*, module: str, text: str):
        Log.log(module=module, text=text, level=Log.INFO)

    @staticmethod
    def log(*, module: str, text: str, level: int):
        try:
            Log.objects.create(module=module[:150], text=text[:59000], log_level=level)
        except:
            # logging should never interrupt execution we rather not having the log then failing
            pass

    @staticmethod
    def log_last_exception(module, text):
        Log.error(module=module, text=text + Log.get_error_description())

    @staticmethod
    def get_error_description() -> str:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = "\n".join(traceback.format_tb(exc_traceback))
        return " {}\n{}\n{}\n".format(exc_type, exc_value, tb)


class Language(models.Model):
    code = models.CharField(max_length=2, verbose_name=ugettext_lazy("Code"))
    name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Name"))


class Country(models.Model):
    code = models.CharField(max_length=3, verbose_name=ugettext_lazy("Code"))
    name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Name"))
    default_language = models.ForeignKey(Language, on_delete=PROTECT, null=True, blank=True,
        verbose_name=ugettext_lazy("Default Language"))
    timezone_code = models.CharField(max_length=20, null=True, verbose_name=ugettext_lazy("Time Zone"))


class Person(models.Model):
    gender = models.CharField(null=True, blank=True, max_length=10)
    title = models.CharField(null=True, blank=True, max_length=40)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True


class Contact(models.Model):
    person = models.ForeignKey(Person, on_delete=PROTECT, null=True, blank=True, related_name='contacts')
    label = models.CharField(max_length=30)
    is_main = models.BooleanField(default=False)
    value = models.CharField(max_length=300)
    created_ts = models.DateTimeField(default=django_now)
    edited_ts = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    edited_by = models.ForeignKey(Person, on_delete=PROTECT, null=True, blank=True, related_name='edited_contacts')

    class Meta:
        abstract = True


class Email(Contact):
    class Meta:
        abstract = True


class Phone(models.Model):
    class Meta:
        abstract = True


class Address(models.Model):
    address_1 = models.CharField(max_length=1000, null=True, blank=True)
    address_2 = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=PROTECT, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)

    @property
    def val(self):
        city_line = ", ".join([str(s) for s in [self.zip_code, self.city] if s is not None])
        country_line = ", ".join([str(s) for s in [self.state, self.country] if s is not None])
        lines = [self.address_1, self.address_2, city_line, country_line]
        return "\n".join([str(s) for s in lines if s is not None])

    class Meta:
        abstract = True



