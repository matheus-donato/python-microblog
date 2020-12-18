import datetime
import locale
from flask import Flask, render_template, request
from pymongo import MongoClient
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def create_app():
    '''
    Quando iniciamos um app, ele pode ser carregado mais de uma vez. Para previnir isso, foi criada essa função que será chamada
    pelo Flask quando ele for executada, e com isso garantimos que ela só será chamada apenas uma vez.
    '''
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://matheus:master57@microblog-application.xztf5.mongodb.net/test")
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():

        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%d-%m-%Y")
            app.db.entries.insert({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"], "%d-%m-%Y").strftime("%d %b")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)
    return app