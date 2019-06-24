#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Jennifer Cao
# Email: jennifer.cao@wisc.edu
# File Name: models.py
"""
from __future__ import unicode_literals
#import uuid
from django.db import models
from django.contrib.auth.models import User#,AbstractUser
from django.db.models.signals import post_save
from django.contrib.postgres.fields import JSONField
MAJOR_VOTE = 1
AGE_CHOICES = ((0, 'not sure'),
        (1, 'under 10'),
        (2, '11 to 20'),
        (3, '21 to 30'),
        (4, '31 to 40'),
        (5, 'above 41'))
GENDER_CHOICES = ((0, 'not sure'), (1, 'female'), (2, 'male'))

class UserProfile(models.Model):
    """
        User Profile, extension for User class
        store user profiles. These information are used to filter users and verify users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.IntegerField(default = 0)
    age = models.IntegerField(default = 0)
    gender = models.IntegerField(choices = GENDER_CHOICES, default = 0)
    career = models.IntegerField(default = 0)
    approval_rate = models.DecimalField(max_digits = 5, decimal_places = 4, default = 1)
    approval_HIT_number = models.IntegerField(default = 0)

    class Meta:
        verbose_name = 'User Profile'
    def __str__(self):
         return self.user.__str__()
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)

class Project(models.Model):
    """
        store project profiles. A table is one to one related with a project.
    """
    name = models.CharField(max_length = 50, null = False, blank = False)
    owner = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    worker_id_set = JSONField(default = list, null = True, blank = True)
    descriptions = models.TextField(null = True, blank = True)
    keywords = models.TextField(null = True, blank = True)
    HIT_capacity = models.IntegerField(default = 5) # number of questions in a HIT
    label_policy = models.IntegerField(default = MAJOR_VOTE)
    assignment_total = models.IntegerField(default = 2) # the least number that a HIT should be assigned to.
    # filters for hit-worker
    age = models.IntegerField(choices = AGE_CHOICES, default = 0)
    gender = models.IntegerField(choices = GENDER_CHOICES, default = 0)
    career = models.IntegerField(default = 0)
    location = models.IntegerField(default = 0)
    approval_rate = models.DecimalField(max_digits = 5, decimal_places = 4, default = 0)
    approval_HIT_number = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    expiry_time = models.DateTimeField()
    uploaded_file = models.FileField(upload_to="data/", blank=True, null=True)
    complete_indicator = models.BooleanField(default = False) # If all tuples in a project are labeled,
                                                              # then the project is complete.
    table_complete_indicator = models.BooleanField(default = False) # If a table has no new tuples unlabeled,
                                                                    # then the table is complete.
    csv_header = JSONField(default = list, null = False, blank = False)

    def __str__(self):
        return "[{0}] {1}".format(self.id, self.name)

class HIT(models.Model):
    """
        dynamic information of all HITs, it will be updated
         once an assignment created or an assignment finished.
    """
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    label_examples = JSONField(default = list, null = True, blank = True)
    # assignment_num = "how many assignments to be generated for this HIT."
    assignment_num = models.IntegerField(null = False, blank = False)
    # assignment_complete_num = "how many assignments of current HIT is complete."
    assignment_complete_num = models.IntegerField(null = False, blank = False)
    assignment_id_list = JSONField(default = list, null = True, blank = True)
    user_id_list = JSONField(default = list, null = True, blank = True)
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    expiry_time = models.DateTimeField()

    def __str__(self):
        return str(self.id)

class Assignment(models.Model):
    """Assignment will be created when a user select a HIT. """
    hit = models.ForeignKey('HIT', on_delete=models.CASCADE)
    worker = models.ForeignKey('UserProfile')
    label_examples = JSONField(default = list, null = True, blank = True)
    complete_indicator = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now =  True)
    expiry_time = models.DateTimeField()

    def __str__(self):
        return str(self.id)

class Table(models.Model):
    """ class for tables uploaded by csv files. Currently a csv file is related to a project. """
    project = models.ForeignKey('Project')
    example = JSONField(null = False, blank = False)
    label = models.CharField(default = '', max_length = 10, null = False, blank = False)
    complete_indicator = models.BooleanField(default = False)
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now =  True)

    def __str__(self):
        return str(self.id)
