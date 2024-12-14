import json


class JSONManager:
    def __init__(self, filename='data.json'):
        self.filename = filename
        self.data = {}
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            # Если файл не существует, создаем пустой словарь
            self.data = {}

# Сохранить данные в JSON-файл.
    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

# Добавить новую запись в JSON-файл.
    def add_record(self, record):
        idn = record['Уникальный номер']  # Используем существующее поле idn как ключ
        self.data[idn] = record
        self.save_data()

    # Редактировать существующую запись в JSON-файле.
    def edit_record(self, idn, key, new_value):
        if idn in self.data:
            self.data[idn][key] = new_value
            self.save_data()

    # Удалить запись по id
    def delete_record(self, idn_value):
        data_copy = list(self.data.items())
        for key, value in data_copy:
            if value.get('Уникальный номер') == idn_value:
                del self.data[key]
        self.save_data()

    # Находит максимальное уникальное значение для счёта и создания нового уникального номера
    def get_max_idn(self):
        current_idn = [int(i['Уникальный номер']) for i in self.data.values()]
        if not current_idn:
            return 1
        else:
            max_id = max(current_idn)
            return max_id + 1

    # Возвращает boolean ответ в зависимости нашла или нет уникальное число среди всех записей
    def find_idn(self, idn=None):
        find_idn = [int(i['Уникальный номер']) for i in self.data.values()]
        if idn is None:
            return bool(find_idn)
        return idn in find_idn

    # Поиск записей с применением фильтров
    def get_filter_value(self, date=None, date1=None, date2=None, text=None):
        result = []

        if date:
            for record_id, record in self.data.items():
                record_date = record['Дата'][:10]

                if record_date == date:
                    result.append(record)

        elif date1 and date2:
            for record_id, record in self.data.items():
                record_date = record['Дата'][:10]

                if date1 <= record_date <= date2:
                    result.append(record)

        elif text:
            for record_id, record in self.data.items():
                if any(text.lower() in str(value).lower() for value in record.values()):
                    result.append(record)

        if len(result) > 0:
            return result
        else:
            return False

    # Получить запись по ключу
    def get_record(self):
        return self.data

    # Получить все записи
    def get_all_records(self):
        return self.data

    # Очистить все данные
    def clear_data(self):
        self.data = {}
        self.save_data()




