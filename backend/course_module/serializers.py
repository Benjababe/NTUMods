# Serializer helps us translate json and python data types because front end application
# send json data type and receive json data types it also controls what we receive on
# front end applications and what we should send back to front end as we don't want to
# send all the field from db to user

from rest_framework import serializers
from .models import Module, CourseModule, Course


class ModuleSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField('getCourseName')

    def getCourseName(self, moduleObj):
        pkCourseList = CourseModule.objects.filter(module=moduleObj.code).values_list('course', flat=True)
        moduleNameList = []

        for coursepk in pkCourseList:
            moduleNameList.append(Course.objects.filter(pk=coursepk).values_list('name', flat=True)[0])

        return moduleNameList

    class Meta:
        model = Module
        fields = '__all__'
