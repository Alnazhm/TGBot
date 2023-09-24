# TGBot
1) Регистрация
   method: POST
   http://164.92.94.145:8000/api/register/
   body: {
        "username":"Zhuldyz",
       "first_name": "Zhuldyz",
       "password": "123"
   }
   получаем gottoken и копируем его
2) Должны залогиниться
   В Headers добавляем Authorization и в значение вставляем Token gottoken
   method: POST
   http://164.92.94.145:8000/api/login/
   body: {
        "username":"Zhuldyz",
       "password": "123"
   }
   получаем токен тоже
3) Потом переходим сюда t.me/testzhm_bot и нажимает на Начать
4) В Headers добавляем Authorization и в значение вставляем Token gottoken
   method: POST
   http://164.92.94.145:8000/api/sendmessage/
   body: {
        "text":"Simple text what you want",
   }
   и потом получаем в ответе вот это {
    "message": "Сообщение отправлено успешно"
} и статус 201
5) Идем теперь в бот и там проверяем получили ли сообщение
   
