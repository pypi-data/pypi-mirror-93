from flask import Flask, current_app

from mark_fluent_log import MarkFluentLog

app = Flask(__name__)
app.secret_key = "jskdfjdsgfjewresdkgfjdsgfjdsgfsdjgfhjdsgf"
app.bblog = MarkFluentLog(app, "TEST", "121.36.111.190", "bbapm2021bbapm!!")


@app.route("/")
def one():
    current_app.bblog.info_key("old", "mark")
    current_app.bblog.info_key("old", [1,2,3])
    return "success"


if __name__ == '__main__':
    app.run()
