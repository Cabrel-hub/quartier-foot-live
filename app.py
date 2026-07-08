from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# On stocke tout ici : calendrier + scores
matches = []
id_counter = 1

def get_classement():
    equipes = {}
    for m in matches:
        for eq in [m['equipe1'], m['equipe2']]:
            if eq not in equipes:
                equipes[eq] = {'nom': eq, 'pts': 0, 'joues': 0, 'gagnes': 0, 'nuls': 0, 'perdus': 0, 'buts_pour': 0, 'buts_contre': 0}
        if m['score1']!= '' and m['score2']!= '':
            try:
                s1 = int(m['score1']); s2 = int(m['score2'])
                equipes[m['equipe1']]['joues'] += 1
                equipes[m['equipe2']]['joues'] += 1
                equipes[m['equipe1']]['buts_pour'] += s1
                equipes[m['equipe1']]['buts_contre'] += s2
                equipes[m['equipe2']]['buts_pour'] += s2
                equipes[m['equipe2']]['buts_contre'] += s1
                if s1 > s2:
                    equipes[m['equipe1']]['pts'] += 3
                    equipes[m['equipe1']]['gagnes'] += 1
                    equipes[m['equipe2']]['perdus'] += 1
                elif s2 > s1:
                    equipes[m['equipe2']]['pts'] += 3
                    equipes[m['equipe2']]['gagnes'] += 1
                    equipes[m['equipe1']]['perdus'] += 1
                else:
                    equipes[m['equipe1']]['pts'] += 1
                    equipes[m['equipe2']]['pts'] += 1
                    equipes[m['equipe1']]['nuls'] += 1
                    equipes[m['equipe2']]['nuls'] += 1
            except:
                pass
    classement = sorted(equipes.values(), key=lambda x: x['pts'], reverse=True)
    return classement

@app.route('/')
def index():
    return render_template('index.html', matches=matches, classement=get_classement())

@app.route('/add', methods=['POST'])
def add():
    global id_counter
    match = {
        'id': id_counter,
        'equipe1': request.form.get('equipe1'),
        'equipe2': request.form.get('equipe2'),
        'date': request.form.get('date'),
        'heure': request.form.get('heure'),
        'terrain': request.form.get('terrain'),
        'score1': request.form.get('score1', ''),
        'score2': request.form.get('score2', '')
    }
    matches.append(match)
    id_counter += 1
    return redirect('/')

@app.route('/update/<int:match_id>', methods=['POST'])
def update(match_id):
    for m in matches:
        if m['id'] == match_id:
            m['score1'] = request.form.get('score1')
            m['score2'] = request.form.get('score2')
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)