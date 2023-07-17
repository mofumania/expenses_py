from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
import sqlite3
import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)


@app.route("/")
def index():
    input_link = create_link()
    month = create_month()
    input_detail_link = create_detail_link()
    # 前月の計算
    pr = datetime.datetime.strptime(month, "%Y-%m") - relativedelta(months=1)
    pre_month = pr.strftime("%Y-%m")
    # 翌月の計算
    nm = datetime.datetime.strptime(month, "%Y-%m") + relativedelta(months=1)
    next_month = nm.strftime("%Y-%m")

    db = sqlite3.connect("expenses.db", isolation_level=None)

    sql = "SELECT * FROM fixed_cost"
    fixed_costs = db.execute(sql)
    pricies = []
    for fixed_cost in fixed_costs:
        pricies.append(fixed_cost[1])
    total_price = sum(pricies)
    fixed_costs = db.execute(sql)

    food_sql = f"SELECT price FROM items WHERE date LIKE '{month}%' AND category = '食費'"
    food_costs = db.execute(food_sql)
    food_pricies = []
    for food_cost in food_costs:
        food_pricies.append(food_cost[0])
    total_food_cost = sum(food_pricies)
    food_costs = db.execute(food_sql)

    daily_item_sql = f"SELECT price FROM items WHERE date LIKE '{month}%' AND category = '日用品'"
    daily_item_costs = db.execute(daily_item_sql)
    daily_item_pricies = []
    for daily_item_cost in daily_item_costs:
        daily_item_pricies.append(daily_item_cost[0])
    total_daily_item_cost = sum(daily_item_pricies)
    daily_item_costs = db.execute(daily_item_sql)

    entertainment_sql = f"SELECT price FROM items WHERE date LIKE '{month}%' AND category = '交際費'"
    entertainment_costs = db.execute(entertainment_sql)
    entertainment_pricies = []
    for entertainment_cost in entertainment_costs:
        entertainment_pricies.append(entertainment_cost[0])
    total_entertainment_cost = sum(entertainment_pricies)
    entertainment_costs = db.execute(entertainment_sql)

    other_sql = f"SELECT price FROM items WHERE date LIKE '{month}%' AND category = 'その他'"
    other_costs = db.execute(other_sql)
    other_pricies = []
    for other_cost in other_costs:
        other_pricies.append(other_cost[0])
    total_other_cost = sum(other_pricies)
    other_costs = db.execute(other_sql)

    count_sql = f"SELECT COUNT (date = '{month}') FROM fixed_cost"
    count = db.execute(count_sql).fetchall()[0][0]
    if count == 0:
        link = "/fixed_cost/input"
    else:
        link = "/fixed_cost"
    return render_template(
        "index.html",
        input_link=input_link,
        input_detail_link=input_detail_link,
        month=month,
        pre_month=pre_month,
        next_month=next_month,
        fixed_costs=fixed_costs,
        total_price=total_price,
        food_costs = food_costs,
        total_food_cost = total_food_cost,
        daily_item_costs = daily_item_costs,
        total_daily_item_cost = total_daily_item_cost,
        entertainment_costs = entertainment_costs,
        total_entertainment_cost = total_entertainment_cost,
        other_costs = other_costs,
        total_other_cost = total_other_cost,
        link = link
    )

@app.route("/fixed_cost/input", methods=["GET"])
def get_input_fixed_cost():
    month = create_month()
    return render_template("input_fixed_cost.html",month = month)

@app.route("/fixed_cost", methods=["GET"])
def get_fixed_cost():
    month = create_month()
    db = sqlite3.connect("expenses.db", isolation_level=None)
    sql = "SELECT * FROM fixed_cost"
    fixed_costs = db.execute(sql)
    pricies = []
    for fixed_cost in fixed_costs:
        pricies.append(fixed_cost[1])
    total_price = sum(pricies)
    fixed_costs = db.execute(sql)
    return render_template(
        "fixed_cost.html",
        month = month,
        fixed_costs=fixed_costs,
        total_price=total_price)

@app.route("/fixed_cost/input", methods=["POST"])
def post_input_fixed_cost():
    month = create_month()
    rent = request.form["rent"]
    sql = f"INSERT INTO fixed_cost (name,price,name_ja,date) VALUES (?,?,?,?)"
    electricity = request.form["electricity"]
    gas = request.form["gas"]
    water = request.form["water"]
    wi_fi = request.form["wi-fi"]
    savings = request.form["savings"]
    db = sqlite3.connect("expenses.db", isolation_level=None)
    db.execute(sql,("rent",rent,"家賃",month))
    db.execute(sql,("electricity",electricity,"電気代",month))
    db.execute(sql,("gas",gas,"ガス代",month))
    db.execute(sql,("water",water,"水道代",month))
    db.execute(sql,("wi-fi",wi_fi,"wi-fi",month))
    db.execute(sql,("savings",savings,"貯金",month))
    db.close()
    return redirect(url_for("index"))

@app.route("/fixed_cost", methods=["POST"])
def post_fixed_cost():
    month = create_month()
    rent = request.form["rent"]
    sql_rent = f"UPDATE fixed_cost set price = '{rent}' WHERE name = 'rent'"
    electricity = request.form["electricity"]
    sql_ele = f"UPDATE fixed_cost set price = '{electricity}' WHERE name = 'electricity'"
    gas = request.form["gas"]
    sql_gas = f"UPDATE fixed_cost set price = '{gas}' WHERE name = 'gas'"
    water = request.form["water"]
    sql_water = f"UPDATE fixed_cost set price = '{water}' WHERE name = 'water'"
    wi_fi = request.form["wi-fi"]
    sql_wifi = f"UPDATE fixed_cost set price = '{wi_fi}' WHERE name = 'wi_fi'"
    savings = request.form["savings"]
    sql_sav = f"UPDATE fixed_cost set price = '{savings}' WHERE name = 'savings'"
    db = sqlite3.connect("expenses.db", isolation_level=None)
    db.execute(sql_rent)
    db.execute(sql_ele)
    db.execute(sql_gas)
    db.execute(sql_water)
    db.execute(sql_wifi)
    db.execute(sql_sav)
    db.close()
    return redirect(url_for("index"))


@app.route("/detail/<month>")
def detail(month):
    input_link = create_link()
    # 前月の計算
    pr = datetime.datetime.strptime(month, "%Y-%m") - relativedelta(months=1)
    pre_month = pr.strftime("%Y-%m")
    # 翌月の計算
    nm = datetime.datetime.strptime(month, "%Y-%m") + relativedelta(months=1)
    next_month = nm.strftime("%Y-%m")
    db = sqlite3.connect("expenses.db", isolation_level=None)
    sql = f"SELECT * FROM items WHERE date LIKE '{month}%' ORDER BY date ASC"
    items = db.execute(sql)
    # 特定の日付のデータをすべて取得する
    # 取得したデータを表示させる
    return render_template(
        "detail.html",
        items=items,
        input_link=input_link,
        month=month,
        pre_month=pre_month,
        next_month=next_month,
    )


@app.route("/input/<date>", methods=["GET"])
def get_input(date):
    input_detail_link = create_detail_link()
    db = sqlite3.connect("expenses.db", isolation_level=None)
    sql = f"SELECT id,name,price,category FROM items WHERE date = '{date}'"
    items = db.execute(sql)
    pricies = []
    for item in items:
        pricies.append(item[2])
    total_price = sum(pricies)
    result = db.execute(sql)
    return render_template(
        "input.html",
        result=result,
        total_price=total_price,
        date=date,
        input_detail_link=input_detail_link,
    )


@app.route("/input", methods=["POST"])
def post_input():
    category = request.form["category"]
    name = request.form["item"]
    price = int(request.form["price"])
    date = request.form["date"]
    db = sqlite3.connect("expenses.db", isolation_level=None)
    sql = """INSERT INTO items (name,price,category,date) VALUES (?,?,?,?)"""
    db.execute(sql, (name, price, category, date))
    db.close()
    return redirect(url_for("get_input", date=date))


@app.route("/delete_data", methods=["POST"])
def delete_data():
    id = int(request.form["delete_id"])
    date = request.form["date"]
    db = sqlite3.connect("expenses.db", isolation_level=None)
    sql = f"DELETE FROM items WHERE id= '{id}'"
    db.execute(sql)
    db.commit()
    return redirect(url_for("get_input", date=date))

@app.route("/delete_data_detail", methods=["POST"])
def delete_data_detail():
    id = int(request.form["delete_id"])
    month = request.form["month"]
    db = sqlite3.connect("expenses.db", isolation_level=None)
    sql = f"DELETE FROM items WHERE id= '{id}'"
    db.execute(sql)
    db.commit()
    return redirect(url_for("detail", month = month))

def create_link():
    dt_now = datetime.datetime.now()
    today = dt_now.strftime("%Y-%m-%d")
    return "/input/" + today

def create_month():
    dt_now = datetime.datetime.now()
    this_month = dt_now.strftime("%Y-%m")
    return this_month

def create_detail_link():
    dt_now = datetime.datetime.now()
    this_month = dt_now.strftime("%Y-%m")
    return "/detail/" + this_month


if __name__ == "__main__":
    app.debug = True
    app.run(port=8888)
