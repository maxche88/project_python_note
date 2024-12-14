from encode.encrypt import process_encrypt
from manager import JSONManager
import datetime
import textwrap


def main():

    manager = JSONManager()

    while True:
        print(f"{'-' * 29}Note Manager v.1.0{'-' * 29}")
        print(f'add   -   добавить заметку\nedit  -   редактировать заметку\n'
              f'print -   посмотреть заметку (Просмотреть все, используйте "print all")\n'
              f'del   -   удалить заметку    (Удалить все, используйте "del all")\n'
              f'q     -   выход из блокнота')
        print(f"{'-' * 76}")
        action = input("Введите: ")

        # Создаём заметку
        if action == 'add':
            idn = manager.get_max_idn()
            author = input("Введите имя автора: ")
            title = input("Введите заголовок: ")
            text = input("Введите текст заметки: ")

            data = {
                'Уникальный номер': idn,
                'Автор': author,
                'Заголовок': title,
                'Текст': text,
                'Дата': datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            }
            manager.add_record(data)

        # Чтение с фильтром по дате
        elif action == 'print':
            flag = manager.find_idn()
            while flag:
                col = int(input(f'\nПоиск заметки по дате (пример 12.12.2024): 1\n'
                                f'Поиск заметки в промежутке от и до (пример 12.11.2024 12.12.2024): 2\n'
                                f'Поиск заметки по фрагменту текста: 3\n'
                                f'Назад к начальному меню: 0\n\n'
                                f'Введите номер фильтра который применить к поиску: '))
                if col == 1:
                    date = input("Введите дату для поиска. Формат ввода 12.12.2024: ")
                    res_date = manager.get_filter_value(date=date)
                    if res_date:
                        for entry in res_date:
                            print(f"{'-' * 76}")
                            for key, value in entry.items():
                                if len(str(value)) > 69:
                                    value = key + ": " + value
                                    lines = textwrap.wrap(value, width=69)
                                    for line in lines:
                                        print(line)
                                    continue
                                print(f"{key}: {value}")
                            print(f"{'-' * 76}")
                    else:
                        print(f'{'-' * 76}\nНет записей созданных в эту дату!\n{'-' * 50}')

                elif col == 2:
                    date1, date2 = input("Введите даты от и до (включительно) 12.11.2024 12.12.2024: ").split(" ")
                    res_date_f = manager.get_filter_value(date1=date1, date2=date2)
                    if res_date_f:
                        for entry in res_date_f:
                            print(f"{'-' * 76}")
                            for key, value in entry.items():
                                if len(str(value)) > 69:
                                    value = key + ": " + value
                                    lines = textwrap.wrap(value, width=69)
                                    for line in lines:
                                        print(line)
                                    continue
                                print(f"{key}: {value}")
                            print(f"{'-' * 76}")
                    else:
                        print(f'{'-' * 76}\nНет записей созданных в этот период!\n{'-' * 50}')

                elif col == 3:
                    text = input("Введите текст: ")
                    res_text = manager.get_filter_value(text=text)
                    if res_text:
                        for entry in res_text:
                            print(f"{'-' * 76}")
                            for key, value in entry.items():
                                if len(str(value)) > 69:
                                    value = key + ": " + value
                                    lines = textwrap.wrap(value, width=69)
                                    for line in lines:
                                        print(line)
                                    continue
                                print(f"{key}: {value}")
                            print(f"{'-' * 76}")
                    else:
                        print(f'{'-' * 76}\nНет записей в которых существует данный текст!\n{'-' * 50}')

                elif col == 0:
                    break

                else:
                    print(f'Ввод не корректен\n')
            else:
                print("Блокнот пустой. Для того чтобы прочитать - нужно сначала написать!")

        # Чтение всех записей JSON
        elif action == 'print all':
            if manager.find_idn():
                passw = input("В целях безопастности введите пароль: ")
                if passw != "1234":
                    text = manager.get_record()
                    for j, i in enumerate(text):
                        new_value = process_encrypt(text[i]['Текст'])
                        manager.edit_record(str(i), 'Текст', new_value)
                    print("Пароль не верный. Текст зашифрован!")

                pr = manager.get_all_records()
                for entry_id, entry in pr.items():
                    print(f"{'-' * 76}")
                    for key, value in entry.items():
                        if len(str(value)) > 69:
                            value = key + ": " + value
                            lines = textwrap.wrap(value, width=75)
                            for line in lines:
                                print(line)
                            continue
                        print(f"{key}: {value}")
                    print(f"{'-' * 76}")

            else:
                print("Блокнот пустой. Для того чтобы прочитать - нужно сначала написать!")

        # Редактируем заметку
        elif action == 'edit':
            idn_edit = int(input("Введите уникальный номер записи которую необходимо изменить: "))
            flag = manager.find_idn(idn_edit)
            while flag:
                col = int(input(f'\nАвтор: 1\nЗаголовок: 2\nТекст: 3\nНазад к начальному меню: 0\n\n'
                                f'Введите номер поля которое изменить?: '))
                if col == 1:
                    new_value = input("Введите новое значение: ")
                    manager.edit_record(str(idn_edit), 'Автор', new_value)
                    manager.edit_record(str(idn_edit), 'Дата', datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
                    print("Новая запись успешно добавлена")
                elif col == 2:
                    new_value = input("Введите новое значение: ")
                    manager.edit_record(str(idn_edit), 'Заголовок', new_value)
                    manager.edit_record(str(idn_edit), 'Дата', datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
                    print("Новая запись успешно добавлена")
                elif col == 3:
                    new_value = input("Введите новое значение: ")
                    manager.edit_record(str(idn_edit), 'Текст', new_value)
                    manager.edit_record(str(idn_edit), 'Дата', datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
                    print("Новая запись успешно добавлена")
                elif col == 0:
                    break
                else:
                    print(f'Ввод не корректен\n')
            else:
                print("Записи с таким номером не существует")

        # Удаление записи
        elif action == 'del':
            idn_del = int(input("Введите уникальный номер записи для удаления: "))
            if manager.find_idn(idn_del):
                confirm = input("Вы действительно желаете удалить запись? yes/no: ")
                if confirm == 'yes':
                    manager.delete_record(idn_del)
                    print("Запись успешно удалена")
                elif confirm == 'no':
                    print("Вы отменили удаление")
                else:
                    print("Ввод не корректен")
            else:
                print("Записи с таким номером не существует")

        # Удалить все записи
        elif action == 'del all':
            if manager.find_idn():
                confirm = input("Вы действительно желаете удалить все записи? yes/no: ")
                if confirm == 'yes':
                    manager.clear_data()
                    print("Все записи успешно удалены")
                elif confirm == 'no':
                    print("Вы отменили удаление")
                else:
                    print("Ввод не корректен")
            else:
                print("Блокнот пустой, что бы удалить нужно сначала создать.")

        # Выход
        elif action == 'q':
            print("До новых встреч! Это программа была создана студентом Geek Brains. MaxChe")
            break

        else:
            print("Ввод не корректен")


if __name__ == "__main__":
    main()
