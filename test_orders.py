
# Импорт данных запроса из модуля data, в котором определены заголовки и тело запроса
import data

# Импорт настроек из модуля configuration, который содержит параметры конфигурации, URL сервиса
import configuration

# Импорт модуля sender_stand_request, содержит функции для отправки HTTP-запросов
import sender_stand_request


import sender_stand_request

# Позитивный тест 
def test_get_order_by_track_success():
    # Шаг 1: Выполнить запрос на создание заказа
    response_create = sender_stand_request.post_new_order()
    
    # Шаг 2: Сохранить номер трека заказа из тела ответа
    track_number = response_create.json()["track"]
    print(f"\n[Позитивный] Заказ успешно создан. Новый трек-номер: {track_number}")
    
    # Шаг 3: Выполнить запрос на получение заказа по треку заказа
    response_get = sender_stand_request.get_order_by_track(track_number)
    print(f"[Позитивный] Статус ответа сервера: {response_get.status_code} OK")
    
    # Шаг 4: Проверить, что код ответа равен 200
    assert response_get.status_code == 200


# Негативный тест 1: Запрос заказа по несуществующему треку
def test_get_order_by_non_existent_track_error():
    # Передаем заведомо несуществующий или невалидный трек (например, 0 или отрицательный)
    invalid_track = 0
    print(f"\n[Негативный 1] Отправляем запрос с несуществующим треком: {invalid_track}")
    
    response_get = sender_stand_request.get_order_by_track(invalid_track)
    print(f"[Негативный 1] Статус ответа сервера: {response_get.status_code}")
    
    # Проверяем, что сервер возвращает ошибку 404 (Заказ не найден)
    assert response_get.status_code == 404


# Негативный тест 2: Запрос заказа без передачи параметра трека
def test_get_order_by_empty_track_error():
    # Передаем вместо трека пустое значение (None)
    empty_track = ""
    print(f"\n[Негативный 2] Отправляем запрос с пустым параметром трека")
    
    response_get = sender_stand_request.get_order_by_track(empty_track)
    print(f"[Негативный 2] Статус ответа сервера: {response_get.status_code}")
    
    # Проверяем, что сервер возвращает ошибку 400 (Некорректный запрос / Недостаточно данных)
    assert response_get.status_code == 400

    # Позитивный тест POST: Создание заказа с двумя цветами ("BLACK" и "GREY")
def test_create_order_with_multiple_colors_success():
    # Копируем базовое тело запроса, чтобы не изменить оригинал
    current_body = data.order_body.copy()
    # Меняем значение цвета на два доступных варианта
    current_body["color"] = ["BLACK", "GREY"]
    
    print("\n[POST Позитивный] Отправка запроса с выбором двух цветов")
    response = sender_stand_request.requests.post(
        url=sender_stand_request.configuration.URL_SERVICE + sender_stand_request.configuration.CREATE_ORDER_PATH,
        json=current_body,
        headers=data.headers
    )
    
    print(f"[POST Позитивный] Статус ответа сервера: {response.status_code}")
    # Проверяем, что заказ успешно создается (код 201 Created)
    assert response.status_code == 201
    # Проверяем, что в ответе вернулся номер трека
    assert "track" in response.json()


# Негативный тест POST: Создание заказа без обязательного поля (phone)
def test_create_order_missing_phone_error():
    current_body = data.order_body.copy()
    # Удаляем поле phone из словаря
    current_body.pop("phone")
    
    print("\n[POST Негативный 1] Отправка запроса без телефона (phone)")
    response = sender_stand_request.requests.post(
        url=sender_stand_request.configuration.URL_SERVICE + sender_stand_request.configuration.CREATE_ORDER_PATH,
        json=current_body,
        headers=data.headers
    )
    
    print(f"[POST Негативный 1] Статус ответа сервера: {response.status_code}")
    # Ожидаем ошибку 400 Bad Request из-за нехватки обязательных данных
    assert response.status_code == 400


# Негативный тест POST: Отправка запроса с пустым телом {}
def test_create_order_empty_body_error():
    empty_body = {}
    
    print("\n[POST Негативный 2] Отправка пустого тела запроса {}")
    response = sender_stand_request.requests.post(
        url=sender_stand_request.configuration.URL_SERVICE + sender_stand_request.configuration.CREATE_ORDER_PATH,
        json=empty_body,
        headers=data.headers
    )
    
    print(f"[POST Негативный 2] Статус ответа сервера: {response.status_code}")
    # Ожидаем ошибку 400 Bad Request
    assert response.status_code == 400

    # Позитивный тест POST: Минимальное время аренды и корректная дата
def test_create_order_valid_rent_time_and_date_success():
    current_body = data.order_body.copy()
    current_body["rentTime"] = 1  # 1 день аренды
    current_body["deliveryDate"] = "2026-07-15"  # Корректная будущая дата в формате YYYY-MM-DD
    
    print("\n[POST Поля] Отправка запроса с валидными rentTime=1 и deliveryDate")
    response = sender_stand_request.requests.post(
        url=sender_stand_request.configuration.URL_SERVICE + sender_stand_request.configuration.CREATE_ORDER_PATH,
        json=current_body,
        headers=data.headers
    )
    
    print(f"[POST Поля] Статус ответа сервера: {response.status_code}")
    # Сервер должен вернуть 201 Created (или 200, в зависимости от настроек вашего стенда)
    assert response.status_code in [200, 201]
    assert "track" in response.json()


# Негативный тест POST: Некорректный тип данных во времени аренды (строка вместо числа)
def test_create_order_invalid_rent_time_type_error():
    current_body = data.order_body.copy()
    current_body["rentTime"] = "five_days"  # Передаем строку вместо целого числа
    
    print("\n[POST Поля] Отправка запроса со строкой в rentTime")
    response = sender_stand_request.requests.post(
        url=sender_stand_request.configuration.URL_SERVICE + sender_stand_request.configuration.CREATE_ORDER_PATH,
        json=current_body,
        headers=data.headers
    )
    
    print(f"[POST Поля] Статус ответа сервера: {response.status_code}")
    # Ожидаем ошибку валидации 400 Bad Request
    assert response.status_code == 400


# Негативный тест POST: Некорректный формат даты доставки
def test_create_order_invalid_date_format_error():
    current_body = data.order_body.copy()
    current_body["deliveryDate"] = "15-07-2026"  # Неверный формат DD-MM-YYYY (сервер ждет YYYY-MM-DD)
    
    print("\n[POST Поля] Отправка запроса с неверным форматом даты")
    response = sender_stand_request.requests.post(
        url=sender_stand_request.configuration.URL_SERVICE + sender_stand_request.configuration.CREATE_ORDER_PATH,
        json=current_body,
        headers=data.headers
    )
    
    print(f"[POST Поля] Статус ответа сервера: {response.status_code}")
    # Ожидаем ошибку 400 Bad Request
    assert response.status_code == 400

    # Позитивный тест POST: Граничное значение — аренда на 7 дней
def test_create_order_max_rent_time_success():
    current_body = data.order_body.copy()
    current_body["rentTime"] = 7  # Максимально допустимый срок аренды
    
    print("\n[POST Границы] Отправка запроса с максимальным rentTime=7")
    response = sender_stand_request.requests.post(
        url=sender_stand_request.configuration.URL_SERVICE + sender_stand_request.configuration.CREATE_ORDER_PATH,
        json=current_body,
        headers=data.headers
    )
    
    print(f"[POST Границы] Статус ответа сервера: {response.status_code}")
    # Сервер должен успешно создать заказ
    assert response.status_code in [200, 201]
    assert "track" in response.json()


# Негативный тест POST: Значение за границей — аренда на 8 дней
def test_create_order_over_max_rent_time_error():
    current_body = data.order_body.copy()
    current_body["rentTime"] = 8  # Превышение максимального срока аренды
    
    print("\n[POST Границы] Отправка запроса с недопустимым rentTime=8")
    response = sender_stand_request.requests.post(
        url=sender_stand_request.configuration.URL_SERVICE + sender_stand_request.configuration.CREATE_ORDER_PATH,
        json=current_body,
        headers=data.headers
    )