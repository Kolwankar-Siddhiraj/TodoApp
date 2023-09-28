from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from django.core.paginator import Paginator
from datetime import datetime
from taskapp.models import Task
from taskapp.serializer import TaskSerializer


# support functions

def formatDate(sdate=None):

    if sdate == None:
        return sdate

    return datetime.strptime(sdate, "%d-%m-%Y").date()



# views

class TaskView(APIView):

    permission_classes = []
    authentication_classes = []

    @transaction.atomic
    def get(self, request, tid):

        try:
            data = None
            if tid == "all":
                page_number = request.GET.get('page', None)

                task_obj = Task.objects.filter().order_by('-id')
                queryset = task_obj
                if page_number is not None: 
                    paginator = Paginator(task_obj, per_page=10)
                    queryset = paginator.get_page(page_number)

                data = TaskSerializer(queryset, many=True).data

            else:
                task_obj = Task.objects.filter(id=tid).first()
                if task_obj == None:
                    return Response({"success": False, "message": "Task not found !"}, status=status.HTTP_404_NOT_FOUND)

                data = TaskSerializer(task_obj).data

            return Response({"success": True, "message": "Task retrived !", "data": data}, status=status.HTTP_200_OK)

        except Exception as err:
            print("Error occured :: ", err)
            return Response({"success": False, "message": "Something went wrong !"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @transaction.atomic
    def post(self, request, action):

        try:
            rd = request.data
            print("rd :: ", rd)

            msg = "Something went wrong !!!"
            http_status = status.HTTP_400_BAD_REQUEST

            if action not in ["add", "update", "delete"]:
                msg = "Action not allowed !"

            elif action == "add":
                new_task = Task.objects.create(title=rd['title'], description=rd['description'], due_date=formatDate(rd['due_date']))
                data = TaskSerializer(new_task).data
                return Response({"success": True, "message": "New Task Added !", "data": data}, status=status.HTTP_200_OK)


            elif action == "update":
                task_obj = Task.objects.filter(id=rd['id']).first()

                if rd.get('due_date', None) != None:
                    rd['due_date'] = formatDate(rd['due_date'])

                if task_obj is not None:
                    updated_task = TaskSerializer(instance=task_obj, data=rd)
                    if updated_task.is_valid():
                        updated_task.save()
                        return Response({"success": True, "message": "Task Updated !", "data": updated_task.data}, status=status.HTTP_200_OK)
                    else:
                        print("serializer errors :: ", updated_task.errors)
                        msg = "Invalid data !"
                else:
                    msg = "Task not found !"
                    http_status = status.HTTP_404_NOT_FOUND


            elif action == "delete":
                task_obj = Task.objects.filter(id=rd['id']).first()
                if task_obj is not None:
                    task_obj.delete()
                    return Response({"success": True, "message": "Task Deleted !",}, status=status.HTTP_200_OK)

                msg = "Task not found !"
                http_status = status.HTTP_404_NOT_FOUND

            return Response({"success": False, "message": msg}, status=http_status)

        except Exception as err:
            print("Error occured :: ", err)
            return Response({"success": False, "message": "Something went wrong !"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



