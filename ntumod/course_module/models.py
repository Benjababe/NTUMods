from django.db import models

# Create your models here.


class Course(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    sub_code = models.CharField(max_length=10, null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return f'ID:{self.pk} : {self.code} {self.sub_code} : {self.year} : {self.name} : {self.type}'

    class Meta:
        unique_together = ('code', 'sub_code', 'year', 'type')


class Exam(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()
    time = models.CharField(max_length=10, null=True, blank=True)
    duration = models.CharField(max_length=30, null=True, blank=True)
    semester = models.IntegerField(default=1)
    year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'ID:{self.pk} : Name {self.name} : Date {self.date} : Time {self.time} : Duration {self.duration}'

    class meta:
        unique_together = ('name', 'date', 'time', 'duration')


# Note that you need to manually delete the old Module entry as PATCH
# creates a new entry if you try to change the primary key in django
class Module(models.Model):
    code = models.CharField(
        primary_key=True, max_length=10, null=False, blank=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    grading = models.CharField(max_length=20, null=True, blank=True)
    credits = models.FloatField(null=True, blank=True)
    module_prereq = models.ManyToManyField("self", blank=True)
    exam = models.ManyToManyField(Exam, blank=True)

    def __str__(self):
        return f'MOD Code:{self.code} : {self.name} : {self.desc} : {self.grading} : {self.credits}'


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    module = models.ForeignKey(
        Module, to_field='code', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.course} : {self.module}'

    class Meta:
        ordering = ['course', 'module']
        verbose_name_plural = 'Course Modules'
        unique_together = ('course', 'module')
