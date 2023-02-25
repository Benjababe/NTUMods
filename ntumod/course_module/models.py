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


class Module(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    grading = models.CharField(max_length=20, null=True, blank=True)
    credits = models.FloatField(null=True, blank=True)
    module_prereq = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return f'ID:{self.pk} : {self.code} : {self.name} : {self.desc} : {self.grading} : {self.credits}'


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    module = models.ForeignKey(Module, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.course} : {self.module}'

    class Meta:
        ordering = ['course', 'module']
        verbose_name_plural = 'Course Modules'
        unique_together = ('course', 'module')
