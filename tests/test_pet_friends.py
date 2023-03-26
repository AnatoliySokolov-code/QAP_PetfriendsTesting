from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Матроскин', animal_type='кошара',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Милогазка", "кошечка", "1", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Патти', animal_type='анимэ', age=10):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_without_photo(name='Большеглазка', animal_type='кошечка', age='2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert 'id' in result


def test_add_pet_photo(pet_photo='images/cat1.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert 'pet_photo' in result


def test_add_new_pet_with_some_data_missing(name='', animal_type='', age='7'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    if status != 200:
        raise Exception("Заполните обязательные поля.")
    else:
        assert result["animal_type"] == animal_type

    # Баг: животное должно добавляться только в случае заполнения всех обязательных полей


def test_get_api_key_for_invalid_user(email="qwerty@ya.ru", password="qwerty"):
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert "key" not in result


def test_get_api_key_without_credentials(email="", password=""):
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert "key" not in result


def test_add_pet_photo_in_jpeg(pet_photo='images/dog_photo.jpeg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert 'pet_photo' in result


def test_add_pet_photo_in_png(pet_photo='images/pet_photo.png'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert 'pet_photo' in result


def test_add_new_pet_with_invalid_age(name='Страшила', animal_type='пёс', age='222', pet_photo="images\dog_photo.jpeg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert 'id' in result

    # Баг: значение возраста недопустимо, питомец не должен быть добавлен

def test_add_new_pet_with_invalid_animal_type(name='Sunny', animal_type='трамвай', age='65000000'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert 'id' in result

    # Баг: значение вида животного недопустимо, питомец не должен быть добавлен


def test_add_new_pet_with_too_long_name(name="Страшила"*10, animal_type="собака", age="2"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    # Баг: значение имени недопустимо, питомец не должен быть добавлен


def test_delete_any_pet_successful():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    pet_id = pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, pets = pf.get_list_of_pets(auth_key, "")
    assert status == 200
    assert pet_id not in pets.values()
    # Баг: удаление питомца, которого нет в собственном списке питомцев, должно быть недоступно


def test_update_any_pet_info(name="Матроскин", animal_type="мультяшный персонаж", age="2"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    status, result = pf.update_pet_info(auth_key, pets["pets"][0]["id"], name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    # Баг: изменение данных питомца, которого нет в собственном списке питомцев, должно быть недоступно
