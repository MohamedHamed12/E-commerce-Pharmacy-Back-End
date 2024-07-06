
# -*- coding: utf-8 -*-

from accounts.filters import *
from accounts.models import *
from accounts.pagination import *
from accounts.permissions import ProfilePermission
from accounts.serializers import *
from accounts.utils import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework import mixins, viewsets

# -*- coding: utf-8 -*-




class EmployeeViewSet(

                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet
):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [ProfilePermission]
    pagination_class=CustomPagination
    filter_backends = [
            DjangoFilterBackend,
            rest_filters.SearchFilter,
            rest_filters.OrderingFilter,
        ]
    filterset_class = EmployeeFilter


    # def create(self, request, *args, **kwargs):
    #     print("hhh")
    #     serializer = DoctorSerializer(data=request.data)
    #     serializer.is_valid(raise_ex ception=True)
    #     doctor=serializer.save()

    #     user=User.objects.create_user(username=serializer.data['national_id'],password=serializer.data['national_id'])
    #     doctor.user=user
    #     doctor.save()

    #     return Response(DoctorSerializer(doctor).data, status=status.HTTP_201_CREATED)
        # return super().create(request, *args, **kwargs)

#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'method', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['soft', 'hard'],
#                 description='Specify the delete method (soft or hard). Default is soft.'
#             )
#         ]
#     )
#     def destroy(self, request, *args, **kwargs):
#         if  request.query_params.get('method')=='hard':
#                 instance = self.get_object()
#                 instance.delete(force_policy=HARD_DELETE)
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return super().destroy(request, *args, **kwargs)

#     # @method_decorator(cache_page(60))
#     def get_deleted(self, request, *args, **kwargs):
#         if not request.user.is_staff:
#             return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

#         paginator = self.pagination_class()
#         deleted_employees = Employee.deleted_objects.all()
#         result_page = paginator.paginate_queryset( deleted_employees, request)
#         serializer = self.get_serializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)


# class DeletedEmployeeView(viewsets.ViewSet):
#     serializer_class = RestoreEmployeeSerializer
#     queryset = Employee.deleted_objects.all()
#     permission_classes = [StaffPermission]
#     def restore(self, request, *args, **kwargs):
#         serializer = RestoreEmployeeSerializer(data={'id':kwargs['pk']})
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         instance = serializer.validated_data['id']
#         instance.undelete()
#         return Response(status=status.HTTP_200_OK)
#     def destroy(self, request, *args, **kwargs):
#         serializer = RestoreEmployeeSerializer(data={'id':kwargs['pk']})
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         instance = serializer.validated_data['id']
#         instance.delete(force_policy=HARD_DELETE)
#         return Response(status=status.HTTP_204_NO_CONTENT)
