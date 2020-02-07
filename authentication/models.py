from django.db import models
from django.contrib.auth.models import User
import authentication.constants as CONSTANTS
from django.db.models.signals import post_save
from django.dispatch import receiver


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    student_id = models.IntegerField(primary_key=True)
    major = models.CharField(null=True, max_length=2, choices=CONSTANTS.MAJORS)
    first_name = models.CharField(null=True, max_length=20)
    last_name = models.CharField(null=True, max_length=20)
    entrance_year = models.IntegerField(null=True)
    description = models.TextField(null=True)

    def get_full_name(self):
        if self.first_name is not None and self.last_name is not None:
            return self.first_name + ' ' + self.last_name
        elif self.first_name is not None:
            return self.first_name
        elif self.last_name is not None:
            return self.last_name
        else:
            return ''

    def get_entrance_year(self):
        if self.entrance_year:
            return self.entrance_year
        else:
            return 'Not Available'

    def get_major(self):
        print(self.get_major_display())
        if self.major:
            return self.get_major_display()
        return 'Not Available'

    def get_description(self):
        if self.description:
            return self.description
        return ''


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, max_length=20)
    last_name = models.CharField(null=True, max_length=20)
    rank = models.CharField(null=True, max_length=20, choices=CONSTANTS.RANKS)
    description = models.TextField(null=True)

    def get_full_name(self):
        if self.first_name is not None and self.last_name is not None:
            return self.first_name + ' ' + self.last_name
        elif self.first_name is not None:
            return self.first_name
        elif self.last_name is not None:
            return self.last_name
        else:
            return ''

    def get_description(self):
        if self.description:
            return self.description
        return ''

    def get_rank(self):
        if self.rank:
            return self.rank
        return ''

