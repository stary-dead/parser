import re

def parse_size_string(size_string):
    # Регулярные выражения для каждой части строки
    format_pattern = r'(?P<format>US|UK)'
    gender_pattern = r'(?P<gender>[MW]?)'  # Пол (M - мужской, W - женский)
    category_pattern = r'(Kids)?'  # Категория (для детей)
    size_pattern = r'(?P<size>\d+(\.\d+)?)'  # Размер
    age_pattern = r'(?P<age>[YCY]?)'  # Возраст (Y - год, C - ребенок)

    # Объединяем регулярные выражения
    pattern = fr'{format_pattern}\s*{gender_pattern}\s*{category_pattern}\s*{size_pattern}\s*{age_pattern}'

    # Инициализируем список для хранения словарей
    parsed_data = []

    # Находим все соответствия регулярному выражению в строке
    matches = re.finditer(pattern, size_string)

    # Проходимся по каждому соответствию и создаем словарь для каждого
    for match in matches:
        data_dict = match.groupdict()

        # Если пол не указан, присваиваем "Unisex"
        if not data_dict['gender']:
            data_dict['gender'] = 'Unisex'

        # Преобразуем размер в числовой тип, если он указан
        if data_dict['size']:
            data_dict['size'] = float(data_dict['size'])
        
        # Если возраст не указан, присваиваем None
        if not data_dict['age']:
            data_dict['age'] = None

        # Добавляем словарь в список
        parsed_data.append(data_dict)

    return parsed_data


while True:
    print("Строка:")
    print(parse_size_string(input()))