from rest_framework import serializers

from apps.core import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'username',
            'first_name',
            'last_name',
            'patronymic',
            'fullname',
            'email',
        )


class AuthorizeRequest(serializers.Serializer):
    password = serializers.CharField()
    username = serializers.CharField()


class AuthorizeResponse(serializers.Serializer):
    user = UserSerializer()
    token = serializers.CharField()


class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = models.Project
        fields = (
            'id',
            'name',
            'description',
            'created_by',
            'is_active',
        )


class TaskSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(queryset=models.Project.objects.all(), write_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all(), write_only=True, required=False, allow_null=True
    )
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = models.Task
        fields = (
            'id',
            'title',
            'description',
            'assigned_to',
            'priority',
            'status',
            'due_date',
            'created_by',
            'project_id',
            'assigned_to_id',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'task',
            'author',
            'text',
            'created_at',
        )


class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = models.Attachment
        fields = (
            'id',
            'task',
            'comment',
            'file',
            'uploaded_by',
            'created_at',
        )
