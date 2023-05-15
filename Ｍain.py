#写一个Ｈello World的ＡＰＩ
# 1.导入Flask类
from flask import Flask 
# 2.创建Flask实例
app = Flask(__name__)
# 3.定义路由及视图函数
@app.route('/')
def hello_world():
    return 'Hello World!'
# 4.启动程序
if __name__ == '__main__':
    app.run()
    