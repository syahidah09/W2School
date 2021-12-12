from rest_framework import serializers

from ewallet.models import Student

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('student_id', 'name', 'card_id')