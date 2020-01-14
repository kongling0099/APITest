# 定义一个测试脚本
from logzero import logger
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World I am here， test1'


if __name__ == '__main__':
    app.run()

