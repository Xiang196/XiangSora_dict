from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os
import random

app = Flask(__name__)

# 数据库路径（你可以改为绝对路径或相对路径）
DB_PATH = os.path.join('ecdict-sqlite-28', 'stardict.db')

def query_word(word):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 让结果可以用字典方式访问
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM stardict WHERE word = ?", (word.lower(),))
    row = cursor.fetchone()

    conn.close()
    return row

def get_random_word():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 获取一个随机单词，限制为常用词汇（通过collins星级或词频筛选）
    cursor.execute("SELECT word FROM stardict WHERE collins >= 2 OR frq >= 3000 ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    
    conn.close()
    return row['word'] if row else None

@app.route("/", methods=["GET"])
def index():
    word = request.args.get("word", "").strip()
    result = query_word(word) if word else None
    return render_template("index.html", word=word, result=result)

@app.route("/random")
def random_word():
    word = get_random_word()
    if word:
        return redirect(url_for('index', word=word))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
