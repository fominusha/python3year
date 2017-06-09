from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem
##from collections import defaultdict, OrderedDict, Counter

m = Mystem()
app = Flask(__name__)

def check_verbs(text):
    ana = m.analyze(text)
    words_number = 0
    verbs_number = 0
    verbs_trans = 0
    verbs_intrans = 0
    verbs_perfect = 0
    verbs_imperfect = 0
    stat = {}
    massiv_verbs = []


    for i in ana:
        if i['text'].strip() and 'analysis' in i and i['analysis']:
            words_number += 1
            v = i['analysis'][0]['gr'].split('=')[0].split(',')[0]
            verb = i['analysis'][0]['gr']
            if v.startswith('V'):
                verbs_number += 1
                massiv_verbs.append(i['analysis'][0]['lex'])
            if ',сов' in verb:
                verbs_trans += 1
            if 'несов' in verb:
                verbs_intrans += 1
            if 'пе=' in verb:
                verbs_perfect += 1
            if 'нп=' in verb:
                verbs_imperfect += 1

    freq_stat = {}
    for y in massiv_verbs:
        if y in freq_stat:
            freq_stat[y] += 1
        else:
            freq_stat[y] = 1
    freqs_stat = sorted(freq_stat.items(), key=lambda x: x[1], reverse=True)
    
    verbs_number_ps = verbs_number / words_number

    stat['Общее количество слов'] = verbs_number
    stat['Доля глаголов'] = verbs_number_ps
    stat['Глаголов совершенного вида'] = verbs_trans
    stat['Глаголов несовершенного вида'] = verbs_intrans
    stat['Переходных глаголов'] = verbs_perfect
    stat['Непереходных глаголов'] = verbs_imperfect
    results1 = 'Общее количество глаголов: {}, доля глаголов: {}, глаголов совершенного вида: {}, глаголов несовершенного вида: {}, переходных глаголов: {}, непереходных глаголов: {} '.format(verbs_number, verbs_number_ps, verbs_trans, verbs_intrans, verbs_perfect, verbs_imperfect), freqs_stat

    return results1, stat

@app.route('/', methods=['get', 'post'])
def index():
    if request.form:
        text = request.form['text']
        results1, stat = check_verbs(text)
        return render_template('index_page.html', input=text, text=results1, data=stat)
    return render_template('index_page.html', data={})


if __name__ == '__main__':
    app.run(debug=True)
    

            
