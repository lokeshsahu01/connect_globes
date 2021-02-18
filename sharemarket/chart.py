from flask import Flask, render_template, request
import csv
import operator
import pandas as pd

app = Flask(__name__)


def Sort(sub_li, index):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    sub_li.sort(key=lambda x: x[index], reverse=True)
    return sub_li


@app.route('/', methods=['GET', 'POST'])
def chart_view():
    csv_writer = list(csv.reader(open('output1.csv', 'r')))
    sector = {}
    head_index = []
    x = []
    for index, i in enumerate(csv_writer[0]):
        if 'Net' in i and i not in x:
            head_index.append(index)
            x.append(i)
    for i in csv_writer[3:-1]:
        data = []
        for index, j in enumerate(i):
            if index in head_index:
                data.append(int(j.replace(',', '')))
        sector[i[1]] = data
    night_fourthx = []
    night_fourth_data = []
    night_fourth = None
    if request.method == "POST":
        night_fourth = request.form.get('night_fourth')
        index = csv_writer[0].index(night_fourth)
        d = []
        for u in csv_writer[3:-1]:
            s = []
            for w in u:
                s.append(int(w) if w.isdigit() or '-' in w else w)
            d.append(s)
        sorted_data = Sort(d, index)

        for k in sorted_data:
            night_fourthx.append(k[1])
            night_fourth_data.append(int(k[index]))
    return render_template('graph.html', sector=sector, x=x, night_fourthx=night_fourthx, night_fourth_data=night_fourth_data, night_fourth=night_fourth)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
