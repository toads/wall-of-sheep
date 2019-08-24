from flask import Flask, json, render_template
from sniff_qq.qq import init_db
from sniff_qq.qq import start_sniffer
import sqlite3
app = Flask(__name__)
# init_db()
start_sniffer()
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/qq_data')
def qq_data():
    conn = sqlite3.connect('qq_id.sqlite3')
    result = conn.execute('select ID,COUNT,TIMESTAMP from QQ where COUNT > 5')
    # TODO 把这个愚蠢的设定改掉
    qq_list = list()
    for qq_id,count,qq_timestamp in result:
        print(qq_id, count,qq_timestamp)
        qq_list.append({'qq':qq_id})
    # return json.dumps({"data":[{"qq":"1099147431"}]})
    return json.dumps({"data":qq_list})
    
    
if __name__ == '__main__':
    app.run()
