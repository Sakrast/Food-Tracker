from flask import Flask, render_template, g, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect(r'C:\Users\anubh\Desktop\Flask Course\Food Tracker\database.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



@app.route('/', methods = ["POST", "GET"])
def home():
    db = get_db()
    if request.method == "POST":
        if 'date-btn' in request.form:
            date = request.form['date']
            dt = datetime.strptime(date, '%Y-%m-%d')
            database_date = datetime.strftime(dt, '%Y%m%d')
            print(database_date)
            db.execute('insert into log_date (entry_date) values(?)', [database_date])
            db.commit()

        elif 'food-btn' in request.form:
            name = (request.form['food-name'])
            fat = int(request.form['fat'])
            carbs = int(request.form['carbs'])
            protein = int(request.form['protein'])
            calories = protein * 4 + carbs * 4 + fat * 9
            db.execute(
                """ 
                insert into food (name, fat, protein, carbs, calories) 
                values (?, ?, ?, ?, ?)
                """,
                [name, fat, protein, carbs, calories]
            )
            db.commit()

            cur = db.execute('select name, protein, carbs, fat, calories from food')
            results = cur.fetchall()
            return render_template('foods.html', results = results)

    
    cur = db.execute(
        """ 
        select log_date.entry_date, 
        sum(food.protein) as protein, sum(food.carbs) as carbs, sum(food.fat) as fat, sum(food.calories) as calories 
        from log_date 
        left join food_date on food_date.log_date_id = log_date.id
        left join food on food.id = food_date.food_id
        group by log_date.id order by log_date.entry_date desc
        """
    )
    results = cur.fetchall()
    print(results)
    date_results_all = []

    for i in results:
        single_date = {}
        single_date['entry_date'] = i['entry_date']
        single_date['protein'] = i['protein']
        single_date['carbs'] = i['carbs']
        single_date['fat'] = i['fat']
        single_date['calories'] = i['calories']

        d = datetime.strptime(str(i['entry_date']), '%Y%m%d')
        single_date['readable_date'] = datetime.strftime(d, "%B %d, %Y")
        date_results_all.append(single_date)            

    return render_template('home.html', results = date_results_all)


@app.route('/food-details')
def foodDetails():
    db = get_db()
    cur = db.execute('select name, protein, carbs, fat, calories from food')
    results = cur.fetchall()
    return render_template('foods.html', results = results)


@app.route('/view/<date>', methods = ["GET", "POST"])
def view(date):

    db = get_db()
    cur = db.execute("select id, entry_date from log_date where entry_date = ?", [date])
    date_result = cur.fetchone()
    if request.method == "POST":
        db.execute('insert into food_date (food_id, log_date_id) values (?, ?)', [request.form['food-selected'], date_result['id']])
        db.commit()

    d = datetime.strptime(str(date_result['entry_date']), '%Y%m%d')
    readable_date = datetime.strftime(d, '%B %d, %Y')

    food_cur = db.execute('select id, name from food')
    food_results = food_cur.fetchall()

    log_cur = db.execute(
        """ 
        select food.name, food.protein, food.carbs, food.fat, food.calories from log_date
        join food_date on food_date.log_date_id = log_date.id
        join food on food.id = food_date.food_id
        where log_date.entry_date = ?
        """,
        [date]
    )
    log_results = log_cur.fetchall()


    totals = {}
    totals['protein'] = 0
    totals['carbs'] = 0
    totals['fat'] = 0
    totals['calories'] = 0

    for food in log_results:
        totals['protein'] += food['protein']
        totals['carbs'] += food['carbs']
        totals['fat'] += food['fat']
        totals['calories'] += food['calories']

    return render_template('view.html', entry_date=date_result['entry_date'], readable_date = readable_date, \
                           food_results=food_results, log_results=log_results, totals = totals)
    

if __name__ == "__main__":
    app.run(debug=True)