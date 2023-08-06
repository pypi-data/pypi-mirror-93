from flask import Flask, current_app

from mark_fluent_log import MarkFluentLog

app = Flask(__name__)
# "TEST" 对应不同项目，改成PDC、CTMS、IWRS等，方便搜索
# 测试的也可以在前面加上TEST，变成TEST_PDC、TEST_CTMS、TEST_IWRS
app.bblog = MarkFluentLog(app, "TEST", "121.36.111.190", "bbapm2021bbapm!!")


@app.route("/")
def one():
    current_app.bblog.info("info信息")
    current_app.bblog.error("error信息")
    # 带key的消息，方便调试
    current_app.bblog.info_key("old", [1, 2, 3])
    return "success"


if __name__ == '__main__':
    app.run()
