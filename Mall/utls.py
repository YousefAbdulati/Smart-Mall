from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema

schema_view = get_schema_view(
   openapi.Info(
      title="Smart Mall APIs",
      default_version='v1',
      description="APIs for Smart Mall App ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="test.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   generator_class=BothHttpAndHttpsSchemaGenerator,

)