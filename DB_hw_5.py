import psycopg2

# createdb -U postgres db_hw5 в терминале
class Clientbase:

    def create_base(self):
        with open('C:\\Users\\Алина\\Desktop\\postgres_pass.txt', 'r') as f:
            passw = f.read()
        conn = psycopg2.connect(database='db_hw5', user='postgres', password=passw)
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS Client(
                id SERIAL PRIMARY KEY,
                name VARCHAR(80) NOT NULL,
                last_name VARCHAR(80) NOT NULL,
                email VARCHAR(80) UNIQUE NOT NULL);
                ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS Phone(
                id SERIAL PRIMARY KEY,
                phone_number VARCHAR(20) UNIQUE NOT NULL,
                client_id INTEGER NOT NULL REFERENCES Client(id));
                ''')
            conn.commit()
            conn.close()
            print('Таблицы базы данных созданы')

    def add_client(self):
        with open('C:\\Users\\Алина\\Desktop\\postgres_pass.txt', 'r') as f:
            passw = f.read()
        conn = psycopg2.connect(database='db_hw5', user='postgres', password=passw)
        name = input('Введите имя клиента: ')
        last_name = input('Введите фамилию клиента: ')
        email = input('Введите почту клиента: ')
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO Client(name, last_name, email) VALUES (%s, %s, %s);
                ''', (name, last_name, email))
        conn.commit()
        conn.close()
        print(f'Клиент {name} {last_name} добавлен в базу')

    def add_phone(self):
        with open('C:\\Users\\Алина\\Desktop\\postgres_pass.txt', 'r') as f:
            passw = f.read()
        conn = psycopg2.connect(database='db_hw5', user='postgres', password=passw)
        number_ = input('Укажите номер телефона в десятизначном формате: ')
        id = input('Укажите id клиента: ')
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO Phone(phone_number, client_id) VALUES (%s, %s);
                ''', (number_, id))
        conn.commit()
        conn.close()
        print(f'Телефон клиента добавлен')

    def update_data(self):
        with open('C:\\Users\\Алина\\Desktop\\postgres_pass.txt', 'r') as f:
            passw = f.read()
        conn = psycopg2.connect(database='db_hw5', user='postgres', password=passw)
        id = int(input('Введите id клиента, данные которого хотите обновить: '))
        name = input('Введите имя клиента: ')
        last_name = input('Введите фамилию клиента: ')
        email = input('Введите почту клиента: ')
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE Client 
                SET (name, last_name, email) = (%s, %s, %s)
                WHERE id = %s;
                ''', (name, last_name, email, id))
        conn.commit()
        conn.close()
        print(f'Данные клиента изменены')

    def delete_phone(self):
        with open('C:\\Users\\Алина\\Desktop\\postgres_pass.txt', 'r') as f:
            passw = f.read()
        conn = psycopg2.connect(database='db_hw5', user='postgres', password=passw)
        phone_delete = input('Укажите номер телефона для удаления: ')
        with conn.cursor() as cur:
            cur.execute('''
                DELETE FROM Phone 
                WHERE phone_number = %s;
                ''', (phone_delete,))
        conn.commit()
        conn.close()
        print(f'телефонный номер удален')

    def delete_client(self):
        with open('C:\\Users\\Алина\\Desktop\\postgres_pass.txt', 'r') as f:
            passw = f.read()
        conn = psycopg2.connect(database='db_hw5', user='postgres', password=passw)
        client_delete = int(input('Укажите id клиента для удаления:'))
        with conn.cursor() as cur:
            cur.execute('''
                DELETE FROM Phone
                WHERE client_id = %s;
                ''', (client_delete,))
            cur.execute('''
                DELETE FROM Client
                WHERE id = %s;
                ''', (client_delete,))
        conn.commit()
        conn.close()
        print(f'Клиент удален из базы')

    def find_client(self):
        with open('C:\\Users\\Алина\\Desktop\\postgres_pass.txt', 'r') as f:
            passw = f.read()
        conn = psycopg2.connect(database='db_hw5', user='postgres', password=passw)
        data_find = input('Укажите имя, фамилию, почту или телефон для поиска: ')
        with conn.cursor() as cur:
            cur.execute('''
                SELECT * 
                FROM Client
                full JOIN Phone on Client.id = Phone.client_id
                WHERE name=%s or last_name=%s or email=%s or phone_number=%s;
                ''', (data_find, data_find, data_find, data_find))
            res = cur.fetchall()
            id_ = res[0][0]
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT phone_number 
                    FROM Client
                    full JOIN Phone on Client.id = Phone.client_id
                    WHERE client_id=%s;
                    ''', (id_,))
                phones = cur.fetchall()
            for i in res:
                print(f'''
Данные клиента:
id клиента: {i[0]}
Имя клиента: {i[1]}
Фамилия клиента: {i[2]}
Почта клиента: {i[3]}''')
            for phone in phones:
                print(f'Телефон клиента: {phone[0]}')
        conn.commit()
        conn.close()


if __name__ == '__main__':
    base = Clientbase()

    command_dict = {
        '1': base.create_base,
        '2': base.add_client,
        '3': base.add_phone,
        '4': base.update_data,
        '5': base.delete_phone,
        '6': base.delete_client,
        '7': base.find_client
    }

    def interface():
        while True:
            command = input('''
        1 - создать базу данных;
        2 - добавить нового клиента;
        3 - добавить новый телефон существующему клиенту;
        4 - изменить данные клиента;
        5 - удалить телефон существующему клиенту;
        6 - удалить существующего клиента;
        7 - найти клиента по данным (имя, фамилия, почта, телефон)

        Укажите желаемое действие: ''')
            for key, func in command_dict.items():
                if key == command:
                    func()
                    pause = input('Продолжить?')

    interface()