import os, csv, json, random, string
from datetime import datetime

from flask import Flask, render_template, url_for, request, flash, redirect, session, make_response, jsonify, send_file 
import mimetypes
import psycopg2
from io import StringIO, BytesIO
from transliterate import translit


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234asdfasdfasdf'
mimetypes.add_type('application/javascript', '.js')


# ---------------------------------------------
# SELECT * FROM user_connections WHERE id_user = 
# (SELECT id FROM users_ WHERE name = 'test_1');

# ---------------------------------------------
# SELECT * FROM cities ORDER BY RANDOM() LIMIT 5;
# SELECT * FROM street ORDER BY RANDOM() LIMIT 5;

# ---------------------------------------------
# SELECT * FROM first_name ORDER BY RANDOM() LIMIT 5;
# SELECT * FROM surname ORDER BY RANDOM() LIMIT 5;
# SELECT * FROM patronymic ORDER BY RANDOM() LIMIT 5;


def get_connect_db():
    with open('password.txt') as f:
        password = f.read()

    conn = psycopg2.connect(host="localhost",
                            database='mdg_db',
                            user='mdg',
                            password=password)
    return conn


# запос к БД
def get_data_from_db(table, count):
  conn = get_connect_db()
  cur = conn.cursor()
  cur.execute(f'SELECT name FROM {table} ORDER BY RANDOM() LIMIT {count};')
  data = cur.fetchall()
  cur.close()
  conn.close()

  return data


def generate_emale_random(alphabet='aasdfqwer', domain=['mail.ru', 'gmail.com', 'yandex.ru', 'vk.com','rambler.ru'], lenght_min=4, lenght_max=12):
    """
        documentation     
        generate_emale_random(alphabet='aasdfqwer', domain=['mail.ru', 'gmail.com', 'yandex.ru', 'vk.com','rambler.ru'], lenght_min=4, lenght_max=12)
    """

    alphabet = string.ascii_lowercase
    username = "".join(random.choice(alphabet) for _ in range(random.randint(lenght_min, lenght_max)))
    domain = random.choice(domain)
    return f"{username}@{domain}"


def generate_emale_name(first_name, surname,domain=['mail.ru', 'gmail.com', 'yandex.ru', 'vk.com','rambler.ru']):
    """
        documentation     
        generate_emale_name(first_name, surname,domain=['mail.ru', 'gmail.com', 'yandex.ru', 'vk.com','rambler.ru'])
    """

    f_name = translit(first_name.lower(), "ru", reversed=True)
    surname = translit(surname.lower(), "ru", reversed=True)

    # Убираем лишние пробелы и спецсимволы
    f_name = "".join(e for e in f_name if e.isalnum())
    surname = "".join(e for e in surname if e.isalnum())

    f_name = f_name[:random.randint(1, len(f_name))]
    domain = random.choice(domain)

    return  f"{f_name}.{surname}@{domain}"


def generate_phone_random():
    """
      documentation     
      generate_phone_random()
    """

    phone_number = '8 9' + str(random.randint(0, 9)) + str(random.randint(0, 9))
    phone_number = phone_number + ' ' + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
    phone_number = phone_number + ' ' + str(random.randint(0, 9)) + str(random.randint(0, 9))
    phone_number = phone_number + ' ' + str(random.randint(0, 9)) + str(random.randint(0, 9))
    return phone_number


def create_json_data(params, format):
    """
    documentation     
    reate_json_data(params, format)
    """

    count_item = int(params['count_item'])
    if not count_item:
        return ['error']

    print(params)
    surnames = None
    first_names = None
    result_data = []
    if params['surname'] == 'on':
        # surnames_db = get_data_from_db('surname', count_item)
        # print(surnames_db)

        surnames = ['surname'] + ['Aaaaa'] * count_item
        result_data.append(surnames)
    if params['first_name'] == 'on':
        # first_name_db = get_data_from_db('first_name', count_item)
        # print(first_name_db)

        first_names = ['first_name'] + ['Bbbb'] * count_item
        result_data.append(first_names)
    if params['patronymic'] == 'on':
        # patronymic_db = get_data_from_db('patronymic', count_item)
        # print(patronymic_db)

        patronymics = ['patronymic'] + ['Ccccc'] * count_item
        result_data.append(patronymics)
    if params['email']['email'] == 'on':
        if params['email']['email_method'] == 'email-gen':
            email_list = []
            for _ in range(count_item):
                email_list.append(generate_emale_random())
        elif params['email']['email_method'] == 'email-name' and surnames and first_names:
            email_list = []
            for fn, sn in zip(first_names,surnames):
                email_list.append(generate_emale_name(fn, sn))            
            pass
        else:
            email_list = ['aaa@mail.ru'] * count_item
            pass
        email_list = ['email'] + email_list
        result_data.append(email_list)
    if params['phone']['phone'] == 'on':
        if params['phone']['phone_method'] == 'phone-gen':
            phone_list = []
            for _ in range(count_item):
                phone_list.append(generate_phone_random())
        else:
            phone_list = ['8 900 100 22 33'] * count_item
        phones = ['phone'] + phone_list
        result_data.append(phones)
    if params['address']['address'] == 'on':
        addresses_list  = ['Россия'] * count_item
        if params['address']['address_city']:
            # cities_db = get_data_from_db('cities', count_item)
            # print(patronymic_db)
            addresses_list = [i + ', Cccity' for i in addresses_list]

        if params['address']['address_street']:
            # street_db = get_data_from_db('street', count_item)
            # print(street_db)

            addresses_list = [i + ', Ssstreet' for i in addresses_list]

        if params['address']['address_house']:
            addresses_list = [i + f', {random.randint(1, 300)}' for i in addresses_list]

        if params['address']['address_apartment']:
            addresses_list = [i + f', {random.randint(1, 100)}' for i in addresses_list]

            # 'address_city': True, 'address_street': True, 'address_house': True, 'address_apartment': True}
        addresses = ['addresses'] + addresses_list
        result_data.append(addresses)
    
    if format == 'csv':
        data = list(zip(*result_data))
        buffer = StringIO()
        writer = csv.writer(buffer, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerows(data)
        
        buffer.seek(0)
        bytes_buffer = BytesIO(buffer.getvalue().encode("utf-8"))
        return bytes_buffer
    else:
        _data = list(zip(*result_data))
        _data[0] = _data[0] + ('id',)

        data = []
        for n,i in enumerate(_data[1:]):
            data.append(dict(zip(_data[0],i + (n,))))
        
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        bytes_buffer = BytesIO()
        bytes_buffer.write(json_data.encode('utf-8'))
        bytes_buffer.seek(0)
        return bytes_buffer
    pass



@app.route('/index', methods=['GET','POST'])
@app.route('/', methods=['GET','POST'])
def index():
    msg = ''
    if request.method == 'POST':
        params = request.get_json()
        if params and params['format_data'] == 'csv':
            file_csv =  create_json_data(params, 'csv') # r'./test/fff.csv'

            return send_file(file_csv, 
                            mimetype='text/csv',
                            as_attachment=True, 
                            download_name='result.csv')

        elif params and params['format_data'] == 'json':
            file_json = create_json_data(params, 'json') 

            return send_file(file_json, 
                            mimetype='text/json',
                            as_attachment=True, 
                            download_name='result.json')
        else:
            return render_template('page404.html'), 404

        
    print('GET ==========')
    return render_template('index.html')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html'), 404





if __name__ == "__main__":
  app.run(debug=True)

