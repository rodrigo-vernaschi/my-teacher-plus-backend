from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)

from teacher.models import Professor, Aula
from teacher.serializers import(
    ProfessorSerializer,
    CadastrarAulaSerializer,
    AulaSerializer
)

class ProfessorAPIView(APIView):
    def get(self, request, format=None):
        # buscar todos os professores no banco de dados
        professores = Professor.objects.all()
        # serializa todos os professores usando o "many=True"
        serializer = ProfessorSerializer(professores, many=True)
        # retorna a resposta com os dados e o status de sucesso 
        return Response(serializer.data, status=HTTP_200_OK)


class CadastrarAulaAPIView(APIView):
    def post(self, request, id, format=None):
        # buscar professor ou mostrar erro 404
        professor = get_object_or_404(Professor, id=id)
        serializer = CadastrarAulaSerializer(data=request.data)
        if serializer.is_valid():
            aula = Aula(
                nome=serializer.validated_data.get('nome'),
                email=serializer.validated_data.get('email'),
                professor = professor
            )
            aula.save()
            aula_serializer = AulaSerializer(aula, many=False)
            return Response(aula_serializer.data, status=HTTP_201_CREATED)
        return Response(
            {
                "message": "Houveram erros de validação",
                "errors": serializer.errors
            },
            status=HTTP_400_BAD_REQUEST
            )