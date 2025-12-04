def read_csv(path):
    """Читает CSV-файл, возвращает список словарей с данными."""
    records = []
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # первая строка — заголовки
    header = lines[0].strip().split(",")

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        # корректная обработка строк с кавычками
        row = parse_csv_line(line)
        if len(row) != len(header):
            continue

        record = {header[i]: row[i] for i in range(len(header))}
        records.append(record)

    return records


def parse_csv_line(line):
    """
    Собственный парсер CSV без библиотек.
    Поддерживает кавычки и запятые внутри кавычек.
    """
    result = []
    current = ""
    in_quotes = False

    i = 0
    while i < len(line):
        char = line[i]

        if char == '"':
            # двойные кавычки внутри кавычек
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                current += '"'
                i += 1
            else:
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            result.append(current)
            current = ""
        else:
            current += char

        i += 1

    result.append(current)
    return result


def gender_description(sex):
    """Возвращает текст описания пола и форму глагола."""
    if sex.lower() == "female":
        return "женского пола", "совершила"
    return "мужского пола", "совершил"


def device_description(device):
    """Возвращает человекопонятное описание устройства."""
    mapping = {
        "mobile": "мобильного",
        "desktop": "настольного",
        "tablet": "планшетного",
        "laptop": "портативного"
    }
    lower = device.lower()
    return mapping.get(lower, device)


def build_description(item):
    """Формирует человекочитаемое описание записи."""

    fio = item.get("name", "Неизвестно")
    device = device_description(item.get("device_type", ""))
    browser = item.get("browser", "Неизвестно")
    sex = item.get("sex", "")
    age = item.get("age", "?")
    bill = item.get("bill", "?")
    region = item.get("region", "Неизвестно")

    sex_text, verb = gender_description(sex)

    return (
        f"Пользователь {fio} {sex_text}, {age} лет {verb} покупку на "
        f"{bill} у.е. с {device} браузера {browser}. "
        f"Регион, из которого совершалась покупка: {region}."
    )


def write_output(path, descriptions):
    """Записывает все результаты в TXT."""
    with open(path, "w", encoding="utf-8") as file:
        for text in descriptions:
            file.write(text + "\n\n")


def process_clients(csv_path, output_path):
    """Главная функция."""
    records = read_csv(csv_path)

    descriptions = []
    for item in records:
        descriptions.append(build_description(item))

    write_output(output_path, descriptions)


# -------------------------
# Точка входа
# -------------------------
if __name__ == "__main__":
    process_clients("web_clients_correct.csv", "descriptions.txt")
    print("Файл descriptions.txt успешно создан!")
