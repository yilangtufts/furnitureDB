from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask import Flask, jsonify
import psycopg2
import db

app = Flask(__name__)

Bootstrap(app)
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'TEAM054_DB6400'


# assign each form control to a unique variable
class MonthHighestVol(FlaskForm):
    date = DateField("Pick a date to show the report for that month", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')


class HolidayAdd(FlaskForm):
    date = DateField("Pick a date: ", format='%Y-%m-%d', validators=[DataRequired()])
    name = StringField('Enter the holiday name', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('main_menu.html')


@app.route('/holiday', methods=['GET', 'POST'])
def holiday():
    # header, table = db.execute(query)
    query = \
        """
        SELECT distinct holiday_name FROM holiday;
    
        """
    _, holidays = db.execute(query)

    form = HolidayAdd()
    message = ""
    if form.validate_on_submit():
        date = form.date.data
        year = date.year
        month = date.month
        day = date.day
        name = form.name.data
        # check if the selected date is holiday or not:
        query = \
            """
            SELECT * FROM holiday WHERE date = '%d-%d-%d';             
            """
        _, table = db.execute(query % (year, month, day))
        # if no record:
        if len(table) == 0:
            query = \
                """
                INSERT INTO holiday VALUES ('%d/%d/%d', '%s');             
                """
            db.insert(query % (year, month, day, name))
        # if already has a holiday
        else:
            name += table[0][1]
            query = \
                """
                UPDATE holiday SET holiday_name = '%s' WHERE date = '%d/%d/%d';             
                """
            db.update(query % (name, year, month, day))
        return redirect(url_for('holidayShowDate', yr=year, m=month, d=day))
    else:
        message = 'Invalid input.'

    return render_template('holiday.html', posts=holidays, form=form, message=message)

@app.route('/holiday/<selecthol>')
def holidayShowHD(selecthol):
    # header, table = db.execute(query)
    query = \
        """
        SELECT distinct holiday_name FROM holiday;
    
        """
    _, holidays = db.execute(query)
    # header, table = db.execute(query)
    holquery = \
        """
        SELECT *  FROM holiday WHERE holiday_name =  \'%s\';                   
        """
    header, table = db.execute(holquery % selecthol)
    return render_template('holidayShow.html', posts=holidays, table=table, header=header)

@app.route('/holiday/<int:yr>/<int:m>/<int:d>')
def holidayShowDate(yr, m, d):
    # header, table = db.execute(query)
    query = \
        """
        SELECT * FROM holiday WHERE date = '%d-%d-%d';             
        """
    header, table = db.execute(query % (yr, m, d))
    return render_template('holidayShow.html', table=table, header=header)


@app.route('/cityPopSelect')
def cityPopSelect():
    # selectCity
    # added city selection dropdown
    statequery = \
        """
        SELECT distinct city_name FROM city;
    
        """
    _, cities = db.execute(statequery)
    return render_template('cityPopSelect.html', posts=cities)

@app.route('/cityPop/<selectCity>')
def cityPop(selectCity):
    # selectCity
    # added city selection dropdown
    statequery = \
        """
       SELECT distinct city_name FROM city;
    
        """
    _, cities = db.execute(statequery)
    query = \
        """
         SELECT city_name, city_population FROM city
         WHERE city_name =  \'%s\';
        """
    header, table = db.execute(query % selectCity)

    return render_template('cityPop.html', posts=cities, table=table, header=header)

@app.route('/cityPop/update/<City>')
def cityPopUpdate(cityPopNum, State, City):
    #selectCity
    # added city selection dropdown
    statequery = \
    """
   SELECT distinct city_name FROM city;

    """
    _, cities = db.execute(statequery)
    query = \
        """
       UPDATE city
       SET    city_population = \'%a\'
       WHERE  state =\'%s\'
       AND city_name = \'%c\'
        """
    header, table = db.execute(query % (cityPopNum, State, City))

    return render_template('cityPop.html', posts = cities, table=table, header=header)


@app.route('/category_report')
def category_report():
    query = \
        """
        SELECT G.category_name,
            Count(*),
            Min(G.regular_price),
            Avg(G.regular_price),
            Max(G.regular_price)
        FROM   (SELECT T.category_name,
                    P.regular_price
                FROM   (SELECT C.category_name,
                            I.productid
                        FROM   category AS C
                            LEFT JOIN incategory AS I
                                    ON C.category_name = I.category_name) AS T
                    LEFT JOIN product AS P
                            ON T.productid = P.productid) AS G
        GROUP  BY category_name
        ORDER  BY G.category_name ASC;
        """
    header, table = db.execute(query)
    return render_template('category_report.html', table=table, header=header)


@app.route('/sofa')
def couacheSofas():
    query = \
        """
        SELECT Sum(p.regular_price * quantity * 0.75) - Sum(( CASE
                                                            WHEN (
                  d.productid = p.productid
                  AND d.date = t.date ) THEN d.discount_price
                                                            ELSE p.regular_price
                                                          END ) * quantity) AS
           difference,
           p.product_name                                                   AS
           product_name,
           p.productid                                                      AS
           product_ID,
           p.regular_price                                                  AS
           retail_price,
           Sum(t.quantity)                                                  AS
           total_quantity
        FROM   TRANSACTION AS t
            LEFT JOIN product AS p
                    ON t.productid = p.productid
            LEFT JOIN discount AS d
                    ON d.productid = p.productid
            LEFT JOIN incategory AS ic
                    ON ic.category_name = 'Couches'
                        OR ic.category_name = 'Sofas'
        GROUP  BY p.product_name,
                p.productid
        HAVING Sum(p.regular_price * quantity * 0.75) - Sum(( CASE
                                                                WHEN (
                    d.productid = p.productid
                    AND d.date = t.date ) THEN d.discount_price
                                                                ELSE p.regular_price
                                                            END ) * quantity) < -5000
                OR Sum(p.regular_price * quantity * 0.75) - Sum((
                    CASE
                    WHEN ( d.productid =
                            p.productid
                            AND d.date = t.date ) THEN d.discount_price
                    ELSE p.regular_price
                                                                END ) * quantity) >
                5000
        ORDER  BY difference DESC; 
        """
    header, table = db.execute(query)
    return render_template('sofa.html', table=table, header=header)


@app.route('/storeRevSelect')
def storeRevSelect():
    # add selection for states
    statequery = \
        """
        SELECT distinct state FROM city;                         
        """
    _, States = db.execute(statequery)

    # if request.method == 'POST':
    #     selectstate = request.form.get('selectstate')
    #     return render_template('storeRev.html', selectstate)
    return render_template('storeRevSelect.html', posts=States)


@app.route('/storeRev/<selectstate>')
def storeRev(selectstate):
    # add selection for states
    statequery = \
        """
        SELECT distinct state FROM city;                         
        """
    _, States = db.execute(statequery)

    query = \
        """
        SELECT s.store_number,
        address,
        city_name,
        Extract(year FROM t.date) AS Year,
        Sum(quantity * ( CASE
                            WHEN d.discount_price IS NULL THEN regular_price
                            WHEN d.discount_price IS NOT NULL THEN
                            d.discount_price
                            END ))   AS Revenue
        FROM   store AS s
            natural JOIN city
            natural JOIN TRANSACTION AS t
            natural JOIN product AS p
            LEFT OUTER JOIN discount AS d
                            ON t.productid = d.productid
                            AND t.date = d.date
        WHERE  city_name IN (SELECT city_name
                            FROM   city
                            WHERE  state = \'%s\')
        GROUP  BY s.store_number,
                year
        ORDER  BY year,
                revenue DESC;
        """
    header, table = db.execute(query % selectstate)
    return render_template('storeRev.html', posts=States, table=table, header=header)


@app.route('/highestVolSelect', methods=['GET', 'POST'])
def highestVolSelect():
    form = MonthHighestVol()
    message = ""
    if form.validate_on_submit():
        date = form.date.data
        month = date.month
        year = date.year
        return redirect(url_for('highestVol', yr=year, m=month))
    else:
        message = 'Sorry. There is no record for selected month.'
    return render_template('highestVolSelect.html', form=form, message=message)


@app.route('/highestVol/<int:yr>/<int:m>', methods=['GET', 'POST'])
def highestVol(yr, m):
    form = MonthHighestVol()
    message = ""
    if form.validate_on_submit():
        date = form.date.data
        month = date.month
        year = date.year
        return redirect(url_for('highestVol', yr=year, m=month))
    else:
        message = 'Sorry. There is no record for selected month.'

    query = \
        """
        SELECT category_name,
            state,
            volume
        FROM  (SELECT category_name,
                    state,
                    volume,
                    Rank()
                        OVER (
                        partition BY category_name
                        ORDER BY volume DESC ) AS Rank
            FROM   (SELECT category_name,
                            Sum(quantity)AS Volume,
                            state
                    FROM  (SELECT category_name,
                                    quantity,
                                    store_number
                            FROM  (SELECT category_name,
                                            quantity,
                                            store_number,
                                            Extract(year FROM T.date) AS YEAR,
                                            Extract(month FROM T.date)AS month
                                    FROM   incategory AS I
                                            INNER JOIN TRANSACTION AS T
                                                    ON I.productid = T.productid)AS A
                            WHERE  year = %d
                                    AND month = %d)AS C
                            INNER JOIN (SELECT S.store_number,
                                                city_name,
                                                state
                                        FROM   store AS S
                                                INNER JOIN TRANSACTION AS T
                                                        ON
                                                S.store_number = T.store_number)AS
                                        L
                                    ON C.store_number = L.store_number
                    GROUP  BY category_name,
                                state
                    ORDER  BY category_name ASC) a) a
        WHERE  rank = 1 
        """
    header, table = db.execute(query % (yr, m))
    return render_template('highestVol.html', table=table, header=header, form=form, message=message)


@app.route('/restaurant')
def restaurant():
    query = \
        """
        SELECT category,
           CASE
             WHEN store_type IS NULL THEN 'Non-Restaurant'
             ELSE store_type
           end AS Store_Type,
           quantity_sold
        FROM   (SELECT category_name AS Category,
                    CASE
                        WHEN restaurant IS TRUE THEN 'Restaurant'
                    end           AS Store_Type,
                    Sum(quantity) AS Quantity_Sold
                FROM   incategory
                    LEFT JOIN(SELECT restaurant,
                                        store.store_number,
                                        quantity,
                                        productid
                                FROM   store
                                        INNER JOIN transaction
                                                ON store.store_number =
                                                transaction.store_number) a
                            ON incategory.productid = a.productid
                GROUP  BY category_name,
                        restaurant
                ORDER  BY category_name) a; 
        """
    header, table = db.execute(query)
    return render_template('restaurant.html', table=table, header=header)


@app.route('/campaign')
def campaign():
    query = \
        """
        (SELECT b.productid,
                product_name,
                Sum(inside)                AS sold_during_campaign,
                Sum(outside)               AS sold_outside_campaign,
                Sum(inside) - Sum(outside) AS difference
        FROM   (SELECT Max(CASE
                            WHEN camp = 'inside' THEN quantity
                            ELSE 0
                            end) AS inside,
                        Max(CASE
                            WHEN camp = 'outside' THEN quantity
                            ELSE 0
                            end) AS outside,
                        productid,
                        a.date
                FROM   (SELECT CASE
                                WHEN transaction.date BETWEEN
                                    a.start_date AND a.end_date THEN
                                'inside'
                                ELSE 'outside'
                                end              AS camp,
                                productid,
                                transaction.date AS date,
                                quantity
                        FROM   transaction
                                LEFT JOIN (SELECT date,
                                                start_date,
                                                end_date
                                        FROM   belongto
                                INNER JOIN campaign
                                        ON belongto.campaign_description =
                                        campaign.campaign_description) a
                                    ON transaction.date = a.date) AS a
                GROUP  BY productid,
                        camp,
                        a.date) b
                LEFT JOIN product
                    ON b.productid = product.productid
        GROUP  BY b.productid,
                product_name
        ORDER  BY difference DESC
        -- our dummy data can only show top 2 and bottom 2 due to limited number of data
        -- if using our data to run please change the LIMIT from 10 to 2.
        LIMIT  10)
        UNION
        (SELECT b.productid,
                product_name,
                Sum(inside)                AS sold_during_campaign,
                Sum(outside)               AS sold_outside_campaign,
                Sum(inside) - Sum(outside) AS difference
        FROM   (SELECT Max(CASE
                            WHEN camp = 'inside' THEN quantity
                            ELSE 0
                            end) AS inside,
                        Max(CASE
                            WHEN camp = 'outside' THEN quantity
                            ELSE 0
                            end) AS outside,
                        productid,
                        a.date
                FROM   (SELECT CASE
                                WHEN transaction.date BETWEEN
                                    a.start_date AND a.end_date THEN
                                'inside'
                                ELSE 'outside'
                                end              AS camp,
                                productid,
                                transaction.date AS date,
                                quantity
                        FROM   transaction
                                LEFT JOIN (SELECT date,
                                                start_date,
                                                end_date,
                                                campaign.campaign_description
                                        FROM   belongto
                                INNER JOIN campaign
                                        ON belongto.campaign_description =
                                        campaign.campaign_description) a
                                    ON transaction.date = a.date) AS a
                GROUP  BY productid,
                        camp,
                        a.date) b
                LEFT JOIN product
                    ON b.productid = product.productid
        GROUP  BY b.productid,
                product_name
        ORDER  BY difference ASC
        -- our dummy data can only show top 2 and bottom 2 due to limited number of data
        -- if using our data to run please change the LIMIT from 10 to 2.
        LIMIT  10)
        ORDER  BY difference DESC; 
        """
    header, table = db.execute(query)
    return render_template('campaign.html', table=table, header=header)

# check database connection
def check_db_connection():
    try:
        conn = psycopg2.connect(
            database="furnitureDB",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5433"
        )
        conn.close()
        return True
    except Exception as e:
        print("Error connecting to the database:", e)
        return False

@app.route('/check_connection', methods=['GET'])
def check_connection():
    if check_db_connection():
        return "Connected to the database successfully!"
    else:
        return "Failed to connect to the database."

@app.route('/test')
def test():
    query = \
        """
       SELECT * FROM stores;
    
        """
    header, table = db.execute(query)
    return render_template('test.html', table=table, header=header)

if __name__ == "__main__":
    app.run(port=5000, host="127.0.0.1", debug=True)

