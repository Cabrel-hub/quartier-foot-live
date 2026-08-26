from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB = 'quartier.db'

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipe1 TEXT, equipe2 TEXT,
        score1 INTEGER, score2 INTEGER,
        date TEXT,
                heure TEXT)''')
    conn.commit()
    conn.close()

def get_all_matches():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    m = conn.execute('SELECT * FROM matches ORDER BY id DESC').fetchall()
    conn.close()
    return m

def get_classement():
    matches = get_all_matches()
    classement = {}
    for m in matches:
        if m['score1'] is None: continue
        for eq in [m['equipe1'], m['equipe2']]:
            if eq not in classement: classement[eq] = {'J':0,'G':0,'N':0,'P':0,'BP':0,'BC':0,'Pts':0}
        s1,s2 = int(m['score1']), int(m['score2'])
        classement[m['equipe1']]['J']+=1; classement[m['equipe1']]['BP']+=s1; classement[m['equipe1']]['BC']+=s2
        classement[m['equipe2']]['J']+=1; classement[m['equipe2']]['BP']+=s2; classement[m['equipe2']]['BC']+=s1
        if s1>s2: classement[m['equipe1']]['G']+=1; classement[m['equipe1']]['Pts']+=3; classement[m['equipe2']]['P']+=1
        elif s2>s1: classement[m['equipe2']]['G']+=1; classement[m['equipe2']]['Pts']+=3; classement[m['equipe1']]['P']+=1
        else: classement[m['equipe1']]['N']+=1; classement[m['equipe1']]['Pts']+=1; classement[m['equipe2']]['N']+=1; classement[m['equipe2']]['Pts']+=1
    return sorted(classement.items(), key=lambda x: (x[1]['Pts'], x[1]['BP']-x[1]['BC']), reverse=True)

@app.route('/')
def index():
    init_db()
    return render_template('index.html', matches=get_all_matches(), classement=get_classement())

@app.route('/add', methods=['POST'])
def add():
    conn = sqlite3.connect(DB)
    conn.execute('INSERT INTO matches (equipe1, equipe2, score1, score2, date, heure) VALUES (?,?,?,?,?,?)',
                 (request.form.get('equipe1'), request.form.get('equipe2'), request.form.get('score1'), request.form.get('score2'), request.form.get('date'), request.form.get('heure')))
    conn.commit(); conn.close()
    return redirect('/')

@app.route('/update/<int:match_id>', methods=['POST'])
def update(match_id):
    conn = sqlite3.connect(DB)
    conn.execute('UPDATE matches SET score1=?, score2=? WHERE id=?', (request.form.get('score1'), request.form.get('score2'), match_id))
    conn.commit(); conn.close()
    return redirect('/')

@app.route('/reset')
def reset():
    if os.path.exists(DB): os.remove(DB)
    init_db()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)