from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from baserow.contrib.database.api.tokens.authentications import TokenAuthentication
import logging


from ..cloudlanguagetools import instance as clt_instance
# this import is required so that celery can discover the task
from ..cloudlanguagetools import tasks

logger = logging.getLogger(__name__)

class CloudLanguageToolsLanguageList(APIView):
    authentication_classes = APIView.authentication_classes + [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return super().get_permissions()

    @extend_schema(
        tags=["cloudlanguagetools language data"],
        operation_id="language_list",
        description=(
            "Retrieve all languages, translation and transliteration options"
        ),
    )
    @method_permission_classes([AllowAny])
    def get(self, request):
        language_data = clt_instance.get_language_list()
        return Response(language_data)


class CloudLanguageToolsTranslationOptions(APIView):
    authentication_classes = APIView.authentication_classes + [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return super().get_permissions()

    @extend_schema(
        tags=["cloudlanguagetools language data"],
        operation_id="translation_options",
        description=(
            "Retrieve all languages, translation and transliteration options"
        ),
    )
    @method_permission_classes([AllowAny])
    def get(self, request):
        language_data = clt_instance.get_translation_options()
        return Response(language_data)


class CloudLanguageToolsTransliterationOptions(APIView):
    authentication_classes = APIView.authentication_classes + [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return super().get_permissions()

    @extend_schema(
        tags=["cloudlanguagetools language data"],
        operation_id="transliteration_options",
        description=(
            "Retrieve all languages, translation and transliteration options"
        ),
    )
    @method_permission_classes([AllowAny])
    def get(self, request):
        language_data = clt_instance.get_transliteration_options()
        return Response(language_data)

class CloudLanguageToolsDictionaryLookupOptions(APIView):
    authentication_classes = APIView.authentication_classes + [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return super().get_permissions()

    @extend_schema(
        tags=["cloudlanguagetools language data"],
        operation_id="dictionary_lookup_options",
        description=(
            "Retrieve all languages, translation and transliteration options"
        ),
    )
    @method_permission_classes([AllowAny])
    def get(self, request):
        language_data = clt_instance.get_dictionary_lookup_options()
        return Response(language_data)        

class CloudLanguageToolsTranslationServices(APIView):
    authentication_classes = APIView.authentication_classes + [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return super().get_permissions()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="source_language",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                description="source language",
            ),
            OpenApiParameter(
                name="target_language",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                description="target language",
            )            
        ],        
        tags=["cloudlanguagetools language data"],
        operation_id="translation_service",
        description=(
            "Obtain available translation services for source/target language combination"
        ),
    )
    @method_permission_classes([AllowAny])
    def get(self, request, source_language, target_language):
        service_list = clt_instance.get_translation_services_source_target_language(source_language, target_language)
        return Response(service_list)