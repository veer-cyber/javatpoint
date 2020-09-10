from flask import Flask, render_template,request
import requests
import bs4
import pdfcrowd
import sys
import os
from pikepdf import Pdf
from glob import glob
app = Flask(__name__)


@app.route('/')
def enterUrl():
    return render_template('index.html')

@app.route('/user/login', methods=['POST'])
def pdfConverter():
    url = request.form['url']
    endurl = request.form['end']
    print(endurl)
    end = endurl.replace("https://www.javatpoint.com/","")
    print(end)
    print(url)
    print("Check")
    try:
        client = pdfcrowd.HtmlToPdfClient('demo', 'ce544b6ea52a5621fb9d55f8b542d14d')
        client.convertUrlToFile(url, 'static/pdf/1.pdf')
        print("1")
        counter = 2
        noti = True
        while(noti == True):
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.text, "lxml")
            data = soup.select(".next", href=True)
            nextpoint = data[0]['href']
            print(nextpoint)
            url = "https://www.javatpoint.com/" + nextpoint
            if nextpoint != end:
                try:
                    client.convertUrlToFile(url,'static/pdf/' + f'{counter}.pdf')
                    print(counter)
                    counter += 1
                except pdfcrowd.Error as why:
                    sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))
                    raise
            else:
                noti = False

        filepath_list = os.listdir('static/pdf/')
        pdf = Pdf.new()
        for file in filepath_list:
            if file.endswith('.pdf'):
                print(file)
                src = Pdf.open('static/pdf/'+file)
                print("@#$")
                pdf.pages.extend(src.pages)
        src = Pdf.open('static\\final_pdf\\blank.pdf')
        pdf.pages.extend(src.pages)
        pdf.save('static/final_pdf/merged.pdf')

        for file in filepath_list:
            if file.endswith('.pdf'):
                os.remove('static/pdf/'+file)
    except Exception as e:
        print(e)

    return render_template('download.html')
if __name__ == '__main__':
    app.run()
