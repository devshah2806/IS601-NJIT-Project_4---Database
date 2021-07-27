from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'db_test'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Students Marks Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM marks')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, grades=result)


@app.route('/view/<grade_id>', methods=['GET'])
def record_view(grade_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM marks WHERE id=%s', grade_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', grade=result[0])


@app.route('/edit/<grade_id>', methods=['GET'])
def form_edit_get(grade_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM marks WHERE id=%s', grade_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', grade=result[0])


@app.route('/edit/<grade_id>', methods=['POST'])
def form_update_post(grade_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldLName'), request.form.get('fldFName'), request.form.get('fldSSN'),
                 request.form.get('fldTest1'), request.form.get('fldTest2'), request.form.get('fldTest3'),
                 request.form.get('fldTest4'), request.form.get('fldFinal'), request.form.get('fldGrade'), grade_id)
    sql_update_query = """UPDATE marks t SET t.Last_Name = %s, t.First_Name = %s, t.SSN = %s, t.Test1 = 
    %s, t.Test2 = %s, t.Test3 = %s, t.Test4 = %s, t.Final = %s, t.Grade = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/grades/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Student Form')


@app.route('/grades/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldLName'), request.form.get('fldFName'), request.form.get('fldSSN'),
                 request.form.get('fldTest1'), request.form.get('fldTest2'), request.form.get('fldTest3'),
                 request.form.get('fldTest4'), request.form.get('fldFinal'), request.form.get('fldGrade'))
    sql_insert_query = """INSERT INTO marks(Last_Name,First_Name,SSN,Test1,Test2,Test3,Test4,Final,Grade) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<grade_id>', methods=['POST'])
def form_delete_post(grade_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM marks WHERE id = %s """
    cursor.execute(sql_delete_query, grade_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/grades', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM marks')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grades/<grade_id>', methods=['GET'])
def api_retrieve(grade_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM marks WHERE id=%s', grade_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grades/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/grades/<grade_id>', methods=['PUT'])
def api_edit(grade_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/grades/<grade_id>', methods=['DELETE'])
def api_delete(grade_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)