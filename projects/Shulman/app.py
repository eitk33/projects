import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, current_app
from flask_session import Session
#shulmanek47
#shul.man.ek@gmail.com
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

import time

from helpers import apology, login_required, mailpara

from flask_mail import Mail, Message

zzz
app = Flask(__name__)
mailpara()
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
mail = Mail(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///shulman.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Creating index route





# Creating login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM people WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["gab"] = 0
        if db.execute("SELECT g_id FROM gabaim WHERE g_id = ?", session["user_id"]):
            session["gab"] = 1
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



# Creating logout route

@app.route("/logout")

def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



# Creating register route

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form.get("username")
        email = request.form.get("Mail")
        rws = db.execute("SELECT * FROM people WHERE username = ?", request.form.get("username"))
        if not request.form.get("username") or not request.form.get("password"):
            return apology("need usname n' pass", 400)
        if len(rws) != 0:
             return apology("username already taken", 400)
        elif  request.form.get("password") !=request.form.get("confirmation"):
             return apology("passwords are not the same", 400)
        if not email:
            return apology("Invalid mail address", 400)
        elif mail_check(email) == 1:
            return apology("Invalid mail address", 400)
        else:
            passw = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO people (username, hash, mail) values (?,?,?) ", name, passw, email)
            rows = db.execute("SELECT * FROM people WHERE username = ?", request.form.get("username"))
            session["user_id"] = rows[0]["id"]
            id = session["user_id"]
            db.execute("INSERT INTO pref (us_id) values (?) ", id)
            kehila = db.execute("SELECT k_name FROM kehilot ")
            return render_template("preference.html", kehila = kehila)

    else:
        return render_template("register.html")

def mail_check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return 0
    else:
        return 1


# Creating inital preference route

@app.route("/preference", methods=["GET", "POST"])
@login_required
def preference():

    if request.method == "POST":
        id = session.get("user_id")
        db.execute("DELETE FROM pref WHERE us_id = ?", id)
        db.execute("INSERT INTO pref (us_id) values (?) ", id)
        db.execute("DELETE FROM gabaim WHERE g_id = ?", id)
        kehila = request.form.get("Kehila")
        kehila = kehila.strip()
        if request.form.get("new"):
            kehila = request.form.get("new")
            kehila = kehila.strip()
            db.execute("INSERT INTO kehilot (k_name) VALUES (?)", kehila)
        keh = db.execute("SELECT id FROM kehilot WHERE k_name = ?", kehila)
        keh = keh[0]['id']
        ba = 0
        gabay = 0
        if request.form.get('ba'):
            ba = 1
        if request.form.get('gabay'):
            gabay = 2
            db.execute("UPDATE kehilot set gab = ?", id)
            db.execute("INSERT INTO gabaim (g_id, keh_id) VALUES (?,?)", id, keh)
        role = gabay + ba

        db.execute("INSERT INTO ans (us_id, keh_id) VALUES (?,?)", id, keh,)
        db.execute("INSERT INTO arvi (us_id, keh_id) VALUES (?,?)", id, keh,)
        db.execute("INSERT INTO mincha (us_id, keh_id) VALUES (?,?)", id, keh,)
        db.execute("INSERT INTO shabaton (us_id, keh_id) VALUES (?,?)", id, keh,)
        pom = 0
        confs = 0

        if request.form.get('mincha'):
            pom = 1
        if request.form.get('shabat_c'):
            confs = 1


        db.execute("UPDATE pref SET kehila = ?, not_s = ?, conf_m = ?, role = ? WHERE us_id =?"
        ,keh, pom, confs, role, id)
        session.clear()
        return redirect("/")
    else:
        kehila = db.execute("SELECT k_name FROM kehilot ")
        return render_template("preference.html", kehila = kehila)


@app.route("/gabay", methods=["GET", "POST"])
@login_required
def gabay():
    if request.method == "POST":

        id = session.get("user_id")
        keh = db.execute("SELECT id FROM kehilot WHERE gab = ?", id)
        keh = keh[0]['id']



        message = "This is a poll: \n"
        con_mess = "we have a Minyan!\n"
        tot_message = "From Shul-man: \n"

        if request.form.get("minpoll"):
            db.execute("UPDATE ans SET anso_min = 0 WHERE keh_id = ?", keh)
            db.execute("UPDATE mincha SET att = 0 WHERE keh_id = ?", keh)
            message = message + message_add_time_poll("Minchae", request.form.get("mintime"))
            db.execute("UPDATE gabaim SET note_min = 1 WHERE g_id = ?", id)

        if request.form.get("arvpoll"):
            db.execute("UPDATE ans SET anso_arv = 0 WHERE keh_id = ?", keh)
            db.execute("UPDATE arvi SET att = 0 WHERE keh_id = ?", keh)
            message = message + message_add_time_poll("Arvit", request.form.get("arvtime"))
            db.execute("UPDATE gabaim SET note_arv = 1 WHERE g_id = ?", id)
        if request.form.get("shabat"):
            db.execute("UPDATE ans SET anso_shab = 0 WHERE keh_id = ?", keh)
            db.execute("UPDATE shabaton SET att = 0 WHERE keh_id = ?", keh)
            message = message + message_add_shabat("Shabat")
            db.execute("UPDATE gabaim SET note_shab = 1 WHERE g_id = ?", id)
        if request.form.get("mincha_con"):
            con_mess = con_mess + conf_message_time("Minchae", request.form.get("mintimecon"))
        if request.form.get("arv_con"):
            con_mess = con_mess + conf_message_time("Arvit", request.form.get("arvtimecon"))
        if request.form.get("shab_con"):
            con_mess = con_mess + conf_message_shabat("Shabat")
        url = "https://eitk33-code50-97097035-x545xq9qg26rvx-5000.githubpreview.dev/poll"
        message = (f"{message} will you join us? please enter {url} to confirm\n\n\n")

        if request.form.get("minpoll") or request.form.get("arvpoll") or request.form.get("shabpoll"):
            tot_message = tot_message + message
        if request.form.get("mincha_con") or request.form.get("arv_con") or request.form.get("shab_con"):
            tot_message = tot_message + con_mess

        # Send email
        mail_list_poll = 0
        mail_list_poll = db.execute("SELECT mail FROM people WHERE id IN(SELECT us_id FROM pref WHERE not_s = 1 and kehila = (SELECT keh_id FROM gabaim WHERE g_id = ? ))", id)
        mail_list_poll = alt(mail_list_poll)

        mail_list_conf = 0
        mail_list_conf = db.execute("SELECT mail FROM people WHERE id IN (SELECT us_id FROM pref WHERE conf_m = 1 and kehila = (SELECT keh_id FROM gabaim WHERE g_id = ?))", id)
        mail_list_conf = alt(mail_list_conf)

        mail_list_all = 0

        s_poll = set(mail_list_poll)
        s_conf = set(mail_list_conf)
        mail_list_all = set(s_conf).intersection(s_poll)
        mails_poll = list(s_poll.difference(mail_list_all))
        mails_conf = list(s_conf.difference(mail_list_all))
        mail_list_all = list(mail_list_all)

        for i in range(len(mails_poll)):
            message_send = Message(recipients=[mails_poll[i]], body=message)
            mail.send(message_send)
        for i in range(len(mails_conf)):
            message_send = Message(body = con_mess, recipients=[mails_conf[i]])
            mail.send(message_send)
        for i in range(len(mail_list_all)):
            message_send = Message(body = tot_message, recipients= [mail_list_all[i]])
            mail.send(message_send)

        return redirect("/")
    else:
        return render_template("gabay.html")
def alt(list_of):
    for i in range(len(list_of)):
        list_of[i] = list_of[i]['mail']
    return list_of

def message_add_time_poll(dave, time):
    msg = (f"{dave} will take place at: {time}\n")
    return msg

def message_add_shabat(dave):
    msg = (f"{dave} \n")
    return msg

def conf_message_time(dave, time):
    msg = (f"{dave} will take place at: {time}\n")
    return msg

def conf_message_shabat(dave):
    msg = (f"on {dave}\n")
    return msg

@app.route("/poll", methods=["GET", "POST"])
@login_required
def poll():
    id = session.get("user_id")

    if request.method == "POST":
        min_at = 0
        arv_at = 0
        shab_at = 0

        keh = db.execute("SELECT kehila FROM pref WHERE us_id = ?", id)
        keh = keh[0]['kehila']

        if request.form.get("Mincha"):
            min_at = 1
            db.execute("UPDATE mincha SET att = 1 WHERE us_id = ?", id)
            db.execute("UPDATE ans SET anso_min = 1 WHERE us_id = ?", id)
        if request.form.get("Arvit"):
            arv_at = 1
            db.execute("UPDATE arvi SET att = 1 WHERE us_id = ?", id)
            db.execute("UPDATE ans SET anso_arv = 1 WHERE us_id = ?", id)
        if request.form.get("Shabat"):
            shab_at = 1
            db.execute("UPDATE shabaton SET att = 1 WHERE us_id = ?", id)
            db.execute("UPDATE ans SET anso_shab = 1 WHERE us_id = ?", id)

        return redirect ("/")
    else:
        poll_render = 0
        id = session.get("user_id")
        gab_id = db.execute ("SELECT g_id FROM gabaim WHERE keh_id = (SELECT kehila from pref WHERE us_id = ?)", id)
        gab_id = gab_id[0]['g_id']


        poll_val = db.execute("SELECT note_min, note_arv, note_shab FROM gabaim WHERE g_id = ?", gab_id)
        poll_render = []
        if poll_val[0]['note_min'] == 1:
            new = {'name' : 'Mincha'}
            poll_render.append(new)
        if poll_val[0]['note_arv'] == 1:
            new = {'name' : 'Arvit'}
            poll_render.append(new)
        if poll_val[0]['note_shab'] == 1:
            new = {'name' : 'Shabat'}
            poll_render.append(new)


        if check_ans('anso_min') == 0:
            poll_del(poll_render, "Mincha")
        if check_ans("anso_arv") == 0:
            poll_del(poll_render, "Arvit")
        if check_ans("anso_shab") == 0:
            poll_del(poll_render, "Shabat")
        return render_template("poll.html", poll_render = poll_render)

def check_ans(x):
    id = session.get("user_id")
    check_ans = db.execute("SELECT * FROM ans WHERE us_id = ?", id)
    if check_ans[0][x] > 0:
        return 0
    return 1

def poll_del(y , z):
    for i in range(len(y)):
        if y[i]['name'] == z:
            del y[i]
            break
    return

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    id = session.get("user_id")
    prefill = {}
    prefill["keh"] = 0
    keh = db.execute("SELECT kehila FROM pref WHERE us_id = ?", id)
    if keh[0]['kehila']:
        prefill["keh"] = 1
        keh = db.execute("SELECT kehila FROM pref WHERE us_id = ?", id)
        keh = keh[0]['kehila']
        li_min = db.execute("SELECT username FROM people WHERE id IN (SELECT us_id FROM mincha WHERE att = 1 AND keh_id = ?)", keh)
        li_arv = db.execute("SELECT username FROM people WHERE id IN (SELECT us_id FROM arvi WHERE att = 1 AND keh_id = ?)", keh)
        li_shab = db.execute("SELECT username FROM people WHERE id IN (SELECT us_id FROM shabaton WHERE att = 1 AND keh_id = ?)", keh)
        return render_template("index.html", li_min = li_min, li_arv = li_arv, li_shab = li_shab, prefill = prefill)
    else:
        message = "Please make sure to fill your preferences in oreder to conect to Kehila"
        return render_template("index.html", message = message, prefill = prefill)

@app.route("/deregister", methods=[ "POST"])
@login_required
def deregister():
    # Forget registrant
    id = session.get("user_id")
    prefill = {}
    prefill["keh"] = 0
    keh = db.execute("SELECT kehila FROM pref WHERE us_id = ?", id)
    if keh[0]['kehila']:
        prefill["keh"] = 1
    keh = db.execute("SELECT kehila FROM pref WHERE us_id = ?", id)
    keh = keh[0]['kehila']

    idm = request.form.get("idm")
    ida = request.form.get("ida")
    ids = request.form.get("ids")
    if idm:
        db.execute("UPDATE mincha SET att = 0 WHERE us_id = ?", id )
        db.execute("UPDATE ans SET anso_min = 0 WHERE us_id = ?", id )
    if ida:
        db.execute("UPDATE arvi SET att = 0 WHERE us_id = ?", id )
        db.execute("UPDATE ans SET anso_arv = 0 WHERE us_id = ?", id )
    if ids:
        db.execute("UPDATE shabaton SET att = 0 WHERE us_id = ?", id )
        db.execute("UPDATE ans SET anso_shab = 0 WHERE us_id = ?", id )
    li_min = db.execute("SELECT username FROM people WHERE id IN (SELECT us_id FROM mincha WHERE att = 1 AND keh_id = ?)", keh)
    li_arv = db.execute("SELECT username FROM people WHERE id IN (SELECT us_id FROM arvi WHERE att = 1 AND keh_id = ?)", keh)
    li_shab = db.execute("SELECT username FROM people WHERE id IN (SELECT us_id FROM shabaton WHERE att = 1 AND keh_id = ?)", keh)
    return render_template("index.html", li_min = li_min, li_arv = li_arv, li_shab = li_shab, prefill = prefill)