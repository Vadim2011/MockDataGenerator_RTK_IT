import os, csv, json
from datetime import datetime

from flask import Flask, render_template, url_for, request, flash, redirect, session, make_response, jsonify, send_file 
import mimetypes
import psycopg2
from io import StringIO, BytesIO



app = Flask(__name__)
app.config['SECRET_KEY'] = '1234asdfasdfasdf'
mimetypes.add_type('application/javascript', '.js')


def get_connect_db():
  conn = psycopg2.connect(host="localhost",
                          database='mdg',
                          user='rtkuser',
                          password='rtkuser')
  return conn
# send_file(
#     path_or_file: 'os.PathLike[t.AnyStr] | str | t.IO[bytes]',
#     mimetype: 'str | None' = None,
#     as_attachment: 'bool' = False,
#     download_name: 'str | None' = None,
#     conditional: 'bool' = True,
#     etag: 'bool | str' = True,
#     last_modified: 'datetime | int | float | None' = None,
#     max_age: 'None | (int | t.Callable[[str | None], int | None])' = None    
# )

@app.route('/index', methods=['GET','POST'])
@app.route('/', methods=['GET','POST'])
def index():
    msg = ''
    if request.method == 'POST':
        if request.get_json() and request.get_json()['format_data'] == 'csv':
            print('Poosst ========== csv')
            print(request.get_json())
            file_path = r'./test/fff.csv'
            # Отправляем файл с принудительной загрузкой (as_attachment=True)
            return send_file(file_path, 
                            mimetype='text/csv',
                            as_attachment=True, 
                            download_name='fff.csv')

        elif request.get_json() and request.get_json()['format_data'] == 'json':
            print('Poosst ========== json')
            print(request.get_json())
            file_path = r'./test/jj.json'
            # Отправляем файл с принудительной загрузкой (as_attachment=True)
            return send_file(file_path, 
                            mimetype='text/json',
                            as_attachment=True, 
                            download_name='jj.json')
        else:
            return render_template('page404.html'), 404

        
    print('GET ==========')
    return render_template('index.html')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html'), 404


@app.route('/childemployer', methods=['GET','POST','PUT', 'DELETE'])
def children():
  conn = get_connect_db()
  cur = conn.cursor()
  table = 'children_employer'

  if request.method == 'POST':
    try:
      item = request.get_json() # получаем данные от клиента {'pk':'v1', 'c2': 'v2',...}

      item_columns = tuple(item.keys()) # преобразуем Ключи к виду ('pk', 'c2', 'c3', ...)
      item_columns = item_columns
      item_columns = (',').join(item_columns) # преобразуем последов. ключей (колонок) 'c2, c3, ...,cn'

      item_values = tuple(item.values()) # преобразуем Значен к виду ('v1', 'v2', 'v3', ...)

      # формируем запрос INSERT INTO table (c1, c2, c3) VALUES (v1, v2, v3);
      sql = f"INSERT INTO {table} (" + item_columns + ") "
      sql =  sql + 'VALUES (' + ('%s,' * len(item_values)).strip(',') + ");"

      cur.execute(sql, item_values)
      conn.commit()
    except:
      return '<b>Ошибка</b> <br> обработки данных', 400
  
  if request.method == 'PUT':
    try:
      item = request.get_json() # получаем данные от клиента {'pk':'v1', 'c2': 'v2',...}
      item_columns = tuple(item.keys()) # преобразуем Ключи к виду ('pk', 'c2', 'c3', ...)
      pk_name = item_columns[-2] + '=%s AND ' # извлекаем pk=%5
      pk_name2 = item_columns[-1] + '=%s;'
      item_columns = item_columns[:-2] # удаляем pk из последов Ключей
      item_columns = ('=%s,').join(item_columns) + '=%s' # преобразуем последов. ключей (колонок) 'c2=%s, c3=%s, ...'

      item_values = tuple(item.values()) # преобразуем Значен к виду ('v1', 'v2', 'v3', ...)
      pk_value = item_values[-2] # извлекаем Знач vpk
      pk_value2 = item_values[-1] # извлекаем Знач vpk
      item_values = item_values[:-2] # удаляем Знач vpk из основной послед

      # формируем запрос UPDATE table SET c1=v1, c2=v2 WHERE id=2;
      sql = f"UPDATE {table} SET " + item_columns  # "UPDATE table SET c2=%s, c3=%s"
      sql = sql + ' WHERE ' + pk_name + pk_name2   # "UPDATE table SET c2=%s, c3=%s WHERE pk=%s;" 

      cur.execute(sql, (*item_values, pk_value, pk_value2)) # "UPDATE table SET c2=%s, c3=%s WHERE pk=%s;", (v2, v3, vpk)
      conn.commit()
    except:
      return '<b>Ошибка</b> <br> обработки данных', 400
  
  if request.method == 'DELETE':
    try:
      item = request.get_json() # получаем данные от клиента {'pk2':'v1', 'pk2': 'v2',...}
      item_columns = tuple(item.keys()) # преобразуем Ключи к виду ('pk1', 'pk2', 'pk3', ...)
      item_columns = ('=%s AND ').join(item_columns) + '=%s;' # преобразуем последов. ключей 'pk1=%s AND c3=%s...'

      item_values = tuple(item.values()) # преобразуем Значен к виду ('v1', 'v2', 'v3', ...)

      # формируем запрос DELETE FROM table WHERE id=1 and k=2;
      sql = f"DELETE FROM {table}"  # "UPDATE table SET c2=%s, c3=%s"
      sql = sql + ' WHERE ' + item_columns            # "UPDATE table SET c2=%s, c3=%s WHERE pk=%s;" 
      cur.execute(sql, item_values) # "DELETE FROM table WHERE pk1=%s AND pk2=%s;", (v1, v2)
      conn.commit()
    except:
      return '<b>Ошибка</b> <br> обработки данных', 400

  cur.execute('SELECT * FROM employer;')
  employers = cur.fetchall()
  cur.execute(f'SELECT * FROM {table};')
  children = cur.fetchall()
  cur.close()
  conn.close()

  return render_template('childemployer.html', children=children, employers=employers)


@app.route('/get-child/<int:path>')  # Возвращает JSON
def childJSON(path=None):
  conn = get_connect_db()
  cur = conn.cursor()

  sql = 'SELECT e.office_number, ch.child_birth_cert_number, ' \
                               ' ch.employer_number, ' \
                               ' ch.child_name, ' \
                               ' EXTRACT(YEAR FROM ch.child_birth_year), ' \
                               ' ch.child_gender ' \
                               'FROM children_employer ch ' \
         'INNER JOIN employer e ON ch.employer_number = e.employer_number AND ' \
         'e.office_number IN (SELECT office_number FROM office o WHERE o.office_number=%s );'

  cur.execute(sql, (path,)) # "UPDATE table SET c2=%s, c3=%s WHERE pk=%s;", (v2, v3, vpk)
  children_emp_office = [('номер отд.','Номер свид. о рожд.','имя ребенка','год рожд. реб.','пол реб.')]
  children_emp_office = children_emp_office + cur.fetchall()

  cur.close()
  conn.close()

  response = make_response(jsonify(children_emp_office), 200)
  return response


@app.route('/chooseoffice')  # Выбор отдела для показа детей
def chooseoffice():
  conn = get_connect_db()
  cur = conn.cursor()
  cur.execute('SELECT * FROM office ORDER BY office_number;')
  offices = cur.fetchall()
  cur.close()
  conn.close()

  return render_template('chooseoffice.html', offices=offices)


@app.route('/listdb')
def listDB():
  conn = get_connect_db()
  cur = conn.cursor()

  table1 = 'office'
  table2 = 'employer'
  table3 = 'children_employer'

  sql = 'SELECT t1.office_number, t1.office_name, t2.employer_number, t2.employer_surname, ' \
        't2.employer_firstname, t2.employer_patronymic, t2.employer_gender, t2.employer_length_work, ' \
        't3.child_birth_cert_number, t3.child_name, t3.child_birth_year, t3.child_gender ' \
        f'FROM {table1} t1 LEFT JOIN {table2} t2 ON ' \
        f't1.office_number=t2.office_number LEFT JOIN {table3} t3 ON ' \
         't2.employer_number=t3.employer_number ORDER BY  t1.office_number, t2.employer_number ;' 

# кол-во детей у родителей
# employer_surname employer_number	employer_surname	employer_firstname	employer_patronymic	employer_gender	employer_length_work	office_number	count	employer_number
  sql_count_ch = 'select  e.employer_number, e.employer_surname, e.employer_firstname, e.employer_patronymic, ' \
                'e.office_number, ch.count_ch from employer e ' \
                'join (select count(*) as count_ch, ce.employer_number from children_employer ce group by ce.employer_number) ' \
                'as ch on e.employer_number = ch.employer_number; '

  sql_office_child = 'select o.office_number,	o.office_name,	ch_in_off from office o ' \
  'join (select sum(am_ch) as ch_in_off,e.office_number  from employer e ' \
  'join (select count(*) as am_ch, ce.employer_number from children_employer ce group by ce.employer_number) as ch ' \
  'on e.employer_number = ch.employer_number group by e.office_number) as total_ch ' \
  'on total_ch.office_number = o.office_number ;'

  cur.execute(sql)
  alldb = cur.fetchall()

  cur.execute(sql_count_ch)
  count_ch = cur.fetchall()

  cur.execute(sql_office_child)
  office_child = cur.fetchall()

  cur.close()
  conn.close()
  return render_template('listdb.html',alldb=alldb, count_ch=count_ch, office_child=office_child)


@app.route('/download/<path>')
def download(path=None):
  table1 = 'office'
  table2 = 'employer'
  table3 = 'children_employer'

  if path not in ["office-count-child", "employers-count-child", "all-db"]:
    return render_template('page404.html'), 404
  
  name_field = []
  
  if path == "office-count-child":
    sql = 'select o.office_number,	o.office_name,	ch_in_off from office o ' \
        'join (select sum(am_ch) as ch_in_off,e.office_number  from employer e ' \
        'join (select count(*) as am_ch, ce.employer_number from children_employer ce group by ce.employer_number) as ch ' \
        'on e.employer_number = ch.employer_number group by e.office_number) as total_ch ' \
        'on total_ch.office_number = o.office_number ;'
    name_field = ["№ отд.",	"Название отд.",	"Количество детей стор."]  
    
  elif path == "employers-count-child":
    sql = 'select  e.employer_number, e.employer_surname, e.employer_firstname, e.employer_patronymic, ' \
        'e.office_number, ch.count_ch from employer e ' \
        'join (select count(*) as count_ch, ce.employer_number from children_employer ce group by ce.employer_number) ' \
        'as ch on e.employer_number = ch.employer_number; '
    name_field = ["№ Табельный номер сотрудника",	"Фамилия сотруд.",	"Имя сотруд.",
                  "Отчество сотруд.",	"Кол-во детей у сотруд.",	"отдел в котором сотруд."]

  else:
    sql = 'SELECT t1.office_number, t1.office_name, t2.employer_number, t2.employer_surname, ' \
        't2.employer_firstname, t2.employer_patronymic, t2.employer_gender, t2.employer_length_work, ' \
        't3.child_birth_cert_number, t3.child_name, t3.child_birth_year, t3.child_gender ' \
        f'FROM {table1} t1 LEFT JOIN {table2} t2 ON ' \
        f't1.office_number=t2.office_number LEFT JOIN {table3} t3 ON ' \
         't2.employer_number=t3.employer_number ORDER BY  t1.office_number, t2.employer_number ;' 
    name_field = [" № отд.",	"Название отд.",	"Таб. номер сотр.",
                  "Фамилия сотр.",	"Имя сотр.",	"оОтчество сотр.",
                  "Пол сотр.",	"Стаж сотр.",	"Номер СР", "Имя", "Год рожд.", "Пол"]


  conn = get_connect_db()
  cur = conn.cursor()
  cur.execute(sql)
  data = cur.fetchall()

  output = StringIO()

  writer = csv.writer(output, delimiter=";")

  writer.writerow(name_field)

  for row in data:
    writer.writerow(row)
  
  output.seek(0)
  output = output.getvalue()
  output = output.encode('cp1251')

  response = make_response(output)
  response.headers["Content-Disposition"] = f"attachment; filename=hroffice_data{datetime.now().strftime('%S%M%H%d%m%Y')}.csv"
  response.headers["Content-type"] = "text/csv"

  cur.close()
  conn.close()
  return  response


if __name__ == "__main__":
  app.run(debug=True)


