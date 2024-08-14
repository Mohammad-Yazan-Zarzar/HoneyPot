from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import mobileFitstTest
app = Flask(__name__)

# Database connection details
db_config = {
    'host': 'your_host',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="honeypot",
    charset="utf8mb4",
    collation="utf8mb4_general_ci"
)

@app.route('/')
def index():
    tests = get_tests()
    return render_template('index.html', tests=tests)

@app.route('/Account_Manager', methods=['GET', 'POST'])

def Account_Manager():
    if request.method == 'POST':
        # username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        typeAccount = request.form['typeAccount']
        save_email(email,password,typeAccount)
        return redirect(url_for('Account_Manager'))
    accounts=get_accounts()
    return render_template('accountManager.html', accounts=accounts)


def get_accounts():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="honeypot",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        cursor = db.cursor()
        sql = "select * from accounts"
        cursor.execute(sql)
        accounts = cursor.fetchall()
        cursor.close()
        db.close()
        return accounts
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []


def get_tests():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="honeypot",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        cursor = db.cursor()
        sql = ("select companyName,countryCode,mobileNumbers.phone,testCounter,brand,testDate,testTime,success,descriptionTest from tests inner join mobileNumbers on tests.phoneId=mobileNumbers.id "
               " inner join company on mobileNumbers.companyId=company.id ORDER BY testDate DESC , testTime Desc  ;")
        cursor.execute(sql)
        tests = cursor.fetchall()
        cursor.close()
        db.close()
        return tests
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

def save_email(email,password,typeAccount):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="honeypot",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        cursor = db.cursor()
        status=True
        sql = "INSERT INTO accounts (email,password,accountType,status) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (email,password,typeAccount,status))
        db.commit()
        cursor.close()
        db.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

@app.route('/run-function',methods=['POST'])
def runHoneypot():
    data = request.get_json()

    print('run HoneyPot',data)

    mobileFitstTest.honeyPot(data['test'])
    return jsonify({'result': 'success'})




if __name__ == '__main__':
    app.run(debug=True)