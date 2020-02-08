from django.db import models

from broker.constants import *
from authentication.models import Instructor, Student


class Course(models.Model):
    course_id = models.CharField("course ID", max_length=10)
    course_name = models.CharField("course Name", max_length=10)
    requirement = models.TextField("course Requirements")

    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')


class ApplicationForm(models.Model):
    # course_id = models.CharField("course_id", max_length=10)
    creator = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='forms')
    release_date = models.DateField("release_date", auto_now=True)
    deadline = models.DateField("deadline")
    info = models.CharField("information", max_length=1000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='forms')

    def get_responses(self):
        return self.responses


class Question(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint(fields=['form', 'number'], name='unique_form_number')]

    form = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, related_name="questions")
    question = models.CharField("question", max_length=QUESTION_MAX_LENGTH, blank=False, null=False)
    number = models.IntegerField()
    type = models.CharField("type", max_length=255)

    def save(self, *args, **kwargs):
        self.type = self.__class__.__name__
        super().save(*args, **kwargs)

    def typed(self):
        if self.type:
            return self.__getattribute__(self.type.lower())
        else:
            return self

    def make_answer(self):
        raise NotImplementedError

    def __str__(self):
        return self.question



class ApplicationResponse(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='responses')
    date = models.DateField("date_submitted", auto_now=True)
    state = models.CharField(max_length=1, choices=APPLICATION_STATES)
    form = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, related_name='responses')

    def get_form(self):
        return self.form



class Answer(models.Model):
    response = models.ForeignKey(ApplicationResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    type = models.CharField("type", max_length=255)

    def save(self, *args, **kwargs):
        self.type = self.__class__.__name__
        super().save(*args, **kwargs)

    def typed(self):
        if self.type:
            return self.__getattribute__(self.type.lower())
        else:
            return self

class TextualQuestion(Question):
    def make_answer(self):
        t = TextualAnswer()
        t.question = self
        return t

class TextualAnswer(Answer):
    value = models.CharField('text_value', max_length=100, default="")
    def __str__(self):
        return self.value

class MultiChoiceQuestion(Question):
    def make_answer(self):
        t = MultiChoiceAnswer()
        t.question = self

class MultiChoiceAnswer(Answer):
    value = models.CharField("choice_value", max_length=CHOICE_MAX_LENGTH)

    def __str__(self):
        return self.value


class NumericalQuestion(Question):
    def make_answer(self):
        t = NumericalAnswer()
        t.question = self
        return t

class NumericalAnswer(Answer):
    value = models.IntegerField('int_value')

    def __str__(self):
        return str(self.value)
