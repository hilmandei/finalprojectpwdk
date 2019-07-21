from flask import Flask, send_from_directory, render_template, request, redirect, url_for, flash
import pandas as pd
import joblib
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import random
import os


app = Flask(__name__, static_url_path='')
app.secret_key = 'random string'

df = pd.read_csv('dataclean.csv', index_col=0)
model = joblib.load('modelmobil1')
dfX = pd.read_csv('nilaiX.csv', index_col=0)

premium = df['car'][df['carClass'] == 4].unique()
high = df['car'][df['carClass'] == 3].unique()
normal = df['car'][df['carClass'] == 2].unique()
low = df['car'][df['carClass'] == 1].unique()



@app.route('/')
def welcome():
    listbrand = df['car'].unique()
    listsize = df['sizeCat'].unique()
    listeng = df['engType'].unique()
    drivetype = df['drive2'].unique()
    print(df.columns)

    return render_template('mobil2.html', brand=listbrand, size=listsize, mesin=listeng, drive=drivetype)


@app.route('/predictionresult', methods=['post'])
def hasil():
    try:
        brand = request.form['brand']
        jarak = request.form['jarak']
        tahun = request.form['tahun']
        volume = request.form['volume']
        size = request.form['size']
        drive = request.form['drive']
        mesin = request.form['mesin']
        regis = request.form['regis']

        if brand == "" or jarak == "" or tahun == "" or volume == "" or size == "" or drive == "" \
                or mesin == "" or regis == "":

            return render_template('mobil2.html', b='kosong')

        else:
            if brand in premium:
                carclass = 4
            elif brand in high:
                carclass = 3
            elif brand in normal:
                carclass = 2
            else:
                carclass = 1

            if size == 'big car':
                bigcar = 1
                mediumcar = 0
                smallcar = 0

            elif size == 'medium car':
                bigcar = 0
                mediumcar = 1
                smallcar = 0

            else:
                bigcar = 0
                mediumcar = 0
                smallcar = 1

            if drive == 'full':
                wd4 = 1
                wd2 = 0
            else:
                wd4 = 0
                wd2 = 1

            if mesin == 'Diesel':
                diesel = 1
                gas = 0
                other = 0
                petrol = 0
            elif mesin == 'Gas':
                diesel = 0
                gas = 1
                other = 0
                petrol = 0
            elif mesin == 'Other':
                diesel = 0
                gas = 0
                other = 1
                petrol = 0
            else:
                diesel = 0
                gas = 0
                other = 0
                petrol = 1
            if regis == 'yes':
                yes = 1
                no = 0
            else:
                yes = 0
                no = 1

            print(brand)
            print(jarak)
            print(tahun)
            print(volume)
            print(size)
            print(drive)
            print(mesin)
            print(carclass)
            print(regis)

            data = [float(jarak), float(tahun), float(volume), carclass, bigcar, mediumcar, smallcar, wd2,
                    wd4, diesel, gas, other, petrol, no, yes]
            prediksi = model.predict([data])[0]

            print(data)
            print(prediksi)

            # For Filter Recommendation ======================================================
            harga = df['price']
            dict1 = dict(harga)

            list1 = []
            for i in harga:
                harga = 100 - abs(i - prediksi) / 100
                list1.append(harga)

            i = 0
            for x in dict1.keys():
                dict1[x] = list1[i]
                i += 1

            c = dict(Counter(dict1).most_common())
            b = list(c.keys())[0:5]
            print(df[['model', 'price']].loc[b])

            dfrec = pd.DataFrame(columns=['car', 'model', 'year', 'mileage', 'price'], index=range(1, len(b) + 1))

            index = 0
            for i in b:
                dfrec.iloc[index, 0] = df['car'].loc[i]
                dfrec.iloc[index, 1] = df['model'].loc[i]
                dfrec.iloc[index, 2] = df['year'].loc[i]
                dfrec.iloc[index, 3] = df['mileage'].loc[i]
                dfrec.iloc[index, 4] = df['price'].loc[i]
                index += 1
            print(dfrec)

            return render_template('mobil2.html', a=round(prediksi), b='isi', brand1=brand, year1=tahun,jarak1=jarak, volume1=volume,
                                   size1=size, drive1=drive, mesin1=mesin, regis1=regis, rec=dfrec)

    except:
        return redirect(url_for('error'))


@app.route('/historical', methods=['get'])
def sejarah():
    qty = ['car', 'body2', 'sizeCat', 'drive2',  'engType', 'registration']
    mean = ['car', 'body2', 'sizeCat', 'drive2', 'engType', 'registration']

    return render_template('history.html', qty=qty, mean=mean)


@app.route('/historicalresult', methods=['post'])
def hasilsejarah():
    try:
        qty = request.form['qty']
        mean = request.form['mean']

        if qty == '' or mean == '':
            return render_template('history.html', b='kosong')

        else:
            randomname = random.randint(10000, 9999999)
            listplot = os.listdir('./storagemobil')
            aa = 'qty' + str(len(listplot) + 1) + '_' + str(randomname) + '.jpg'
            bb = 'mean' + str(len(listplot) + 1) + '_' + str(randomname) + '.jpg'

            if qty != '':
                print(qty)
                print(mean)
                # Qty plot Figure -----------------------
                x = df[qty].value_counts().index
                y = df[qty].value_counts()

                plt.clf()
                plt.figure(figsize=(10, 5))
                plt.bar(x, y, width=0.3, label='Quantity')
                plt.xticks(x, rotation='vertical')
                plt.ylabel('Quantity')
                plt.xlabel(f'{qty}')
                plt.legend()
                plt.grid()
                plt.tight_layout()

                plt.savefig('storagemobil/%s' % aa)
            else:
                pass

            if mean != '':
                # Mean Figure Plot -----------------------
                ft = df[mean].value_counts().index

                dictmean = {}
                for i in ft:
                    dictmean[i] = df['price'][df[mean] == i].mean()

                c = dict(Counter(dictmean).most_common())
                x1 = list(c.keys())
                y1 = list(c.values())

                plt.figure(figsize=(10, 5))
                plt.bar(np.arange(len(x1)), y1, width=0.3, color='y', tick_label=x1, label='Average Price', alpha=1)
                plt.xticks(rotation='vertical')
                plt.ylabel('Average Price USD')
                plt.xlabel(f'{mean}')
                plt.legend()
                plt.tight_layout()
                plt.grid()
                plt.savefig('storagemobil/%s' % bb)

            else:
                pass

            return render_template('history.html', b='isi', aa=aa, bb=bb)

    except:
        return redirect(url_for('error'))


@app.route('/plotku/<path:yy>')                                 # nama path untuk diakses dari web
def plotku(yy):
    return send_from_directory('storagemobil', yy)


@app.route('/error')
def error():
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)




