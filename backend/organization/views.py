from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from users.serializers import UserFetchSerializer
from users.models import User
from .models import Organization
from .serializers import OrganizationSerializer
from .decorators import (
    is_organization_owner,
    is_particular_organization_owner,
    is_admin,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from project.serializers import ProjectSerializer
from project.models import Project
from config import *


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Viewset for Organization CRUD
    """

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (IsAuthenticated,)

    @is_admin
    def create(self, request, pk=None, *args, **kwargs):
        """
        Create an Organization
        """
        title = request.data.get("title")
        email_domain_name = request.data.get("email_domain_name")
        organization_owner = request.data.get("organization_owner")
        default_transcript_editor = request.data.get("default_transcript_editor")
        default_transcript_reviewer = request.data.get("default_transcript_reviewer")
        default_translation_editor = request.data.get("default_translation_editor")
        default_translation_reviewer = request.data.get("default_translation_reviewer")
        default_transcript_type = request.data.get("default_transcript_type")
        default_translation_type = request.data.get("default_translation_type")

        if title is None or email_domain_name is None or organization_owner is None:
            return Response(
                {
                    "message": "missing param : title or email_domain_name or organization_owner"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            organization_owner = User.objects.get(pk=organization_owner)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if organization_owner.is_superuser == False and organization_owner.role != (
            User.ADMIN and User.ORG_OWNER
        ):
            return Response(
                {"message": "This user can't be the organization owner."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if default_transcript_editor:
            try:
                default_transcript_editor = User.objects.get(
                    pk=default_transcript_editor
                )
            except User.DoesNotExist:
                return Response(
                    {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

        if default_transcript_reviewer:
            try:
                default_transcript_reviewer = User.objects.get(
                    pk=default_transcript_reviewer
                )
            except User.DoesNotExist:
                return Response(
                    {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

        if default_translation_editor:
            try:
                default_translation_editor = User.objects.get(
                    pk=default_translation_editor
                )
            except User.DoesNotExist:
                return Response(
                    {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

        if default_translation_reviewer:
            try:
                default_translation_reviewer = User.objects.get(
                    pk=default_translation_reviewer
                )
            except User.DoesNotExist:
                return Response(
                    {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

        try:
            organization = Organization(
                title=title,
                email_domain_name=email_domain_name,
                organization_owner=organization_owner,
                created_by=request.user,
                default_transcript_editor=default_transcript_editor,
                default_transcript_reviewer=default_transcript_reviewer,
                default_translation_editor=default_translation_editor,
                default_translation_reviewer=default_translation_reviewer,
                default_transcript_type=default_transcript_type,
                default_translation_type=default_translation_type,
            )
            organization.save()
        except:
            return Response(
                {"message": "Organization can't be created"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        organization_owner.organization = organization
        organization_owner.save()

        response = {
            "organization_id": organization.id,
            "message": "Organization is successfully created.",
        }

        return Response(
            response,
            status=status.HTTP_200_OK,
        )

    @is_particular_organization_owner
    def update(self, request, pk=None, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @is_particular_organization_owner
    def partial_update(self, request, pk=None, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        return Response(
            {"message": "Deleting of Organizations is not supported!"},
            status=status.HTTP_403_FORBIDDEN,
        )

    @swagger_auto_schema(
        method="get",
        manual_parameters=[
            openapi.Parameter(
                "role",
                openapi.IN_QUERY,
                description=("A string to get the role type e.g. PROJECT_MANAGER"),
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={200: "Get members of a organization"},
    )
    @action(
        detail=True, methods=["GET"], name="Get Organization users", url_name="users"
    )
    def users(self, request, pk=None):
        try:
            organization = Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            return Response(
                {"message": "Organization not found"}, status=status.HTTP_404_NOT_FOUND
            )
        users = User.objects.filter(organization=organization)
        serializer = UserFetchSerializer(users, many=True)
        if "role" in request.query_params:
            role = request.query_params["role"]
            if role == "PROJECT_MANAGER":
                user_by_roles = users.filter(role="PROJECT_MANAGER")
                serializer = UserFetchSerializer(user_by_roles, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["GET"],
        name="List Projects in Organization",
        url_name="list_projects",
    )
    def list_projects(self, request, pk=None, *args, **kwargs):
        try:
            organization = Organization.objects.get(pk=pk)
            projects = Project.objects.filter(organization_id=organization)

            user = request.user
            if user.role == User.ORG_OWNER or user.is_superuser:
                serializer = ProjectSerializer(projects, many=True)
            else:
                projects_by_roles = []
                for project in projects:
                    if request.user in project.members.all():
                        projects_by_roles.append(project)
                if len(projects_by_roles) > 0:
                    serializer = ProjectSerializer(projects_by_roles, many=True)
                else:
                    return Response(
                        {
                            "message": "This user is not a member of any project in this organization."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(
                {"error": "Project does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": e},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"error": "invalid method"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
