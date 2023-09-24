from django.contrib.auth.models import User
import requests
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, MessageSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Неправильный логин или пароль.'}, status=status.HTTP_400_BAD_REQUEST)


BOT_TOKEN = '6517270295:AAE_AyIpwTKROs5jo48WJKGKIrY3yxHJfuM'

class SendMessageView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            message = serializer.save()
            telegram_chat_id = get_last_message_id()
            message_body = f"{request.user.username}, я получил от тебя сообщение:\n{message.text}"
            print("message body = ", message_body)
            send_message_to_telegram(BOT_TOKEN, telegram_chat_id, message_body)
            return Response({'message': 'Сообщение отправлено успешно'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_last_message_id():
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates")
    data = response.json()

    if data["result"]:
        chat_id = data["result"][0]["message"]["chat"]["id"]
        print("Chat ID:", chat_id)
        return chat_id

def send_message_to_telegram(telegram_token, telegram_chat_id, message):
    print("message in SEND MESSAGE TO TELEGRAM", message)
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    data = {
        'chat_id': telegram_chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    print("RESPONSE ", response)
    if response.status_code != 200:
        print(f'Ошибка отправки сообщения в Telegram: {response.status_code}')





