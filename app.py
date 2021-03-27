#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template,request,send_file
DEVELOPMENT_ENV  = True
import csv
import os
import json 
import io
from werkzeug.utils import secure_filename
app = Flask(__name__)

app_data = {
    "name":         "Convertisseur TEI",
    "description":  "Convertisseur TEI",
    "author":       "ACHOUR & KHAYYA",
    "html_title":   "Convertisseur TEI",
    "project_name": "Convertisseur TEI",
    "keywords":     "flask, webapp, template, basic"
}


@app.route('/')
def index():
    return render_template('index.html', app_data=app_data)


@app.route('/about')
def about():
    return render_template('about.html', app_data=app_data)


@app.route('/service')
def service():
    return render_template('service.html', app_data=app_data)


@app.route('/contact')
def contact():
    return render_template('contact.html', app_data=app_data)

@app.route('/uploadCsv')
def csvToTei():
    return render_template('uploadCsv.html', app_data=app_data)


@app.route('/csvToTei' , methods=['GET','POST'])
def uploadCsv():
    
    csvFile = request.files['csvFile']
    filename = secure_filename(csvFile.filename)
    csvFile.save(os.path.join(filename))
    xmlFile = request.form['Titre']+'.xml'
    csvData = csv.reader(open(csvFile.filename, "r"))
    xmlData = open(xmlFile, 'w',encoding='utf-8')
    xmlData.write('<?xml version="1.0" encoding="UTF-8"?><TEI xmlns="http://www.tei-c.org/ns/1.0" rendition="tei:teisimple">'+"\n"
    +'  '+'<teiHeader>'+"\n"
      +'   '+'<fileDesc>'+"\n"
         +'    '+'<titleStmt>'+"\n"
            +'     '+'<title>'+request.form['Titre']+'</title>'+"\n"
         +'    '+'</titleStmt>'+"\n"
         +'    '+'<publicationStmt>'+"\n"
            +'     '+'<p>Pas des observations</p>'+"\n"
         +'    '+'</publicationStmt>'+"\n"
         +'    '+'<sourceDesc>'+"\n"
            +'     '+'<p>'+request.form['source']+'</p>'+"\n"
         +'    '+'</sourceDesc>'+"\n"
      +'   '+'</fileDesc>'+"\n"
    +'  '+'</teiHeader>'+"\n"
    +'  '+'<text>'+"\n"
      +'   '+'<body>'+"\n"
         +'    '+'<table>'+"\n")

    for row in csvData:
        xmlData.write('     '+'<row>' + "\n")
        for i in range(len(row)):
            xmlData.write('      '+'<' + 'cell ' +'n = "'+str(i+1)+ '">' \
                          + row[i] + '</' + 'cell' +'>' + "\n")
        xmlData.write('     '+'</row>' + "\n")

    xmlData.write('    '+'</table>'+"\n"
      +'   '+'</body>'+"\n"
    +'  '+'</text>'+"\n"
    +'</TEI>')
    xmlData.close()
    return send_file(request.form['Titre']+'.xml', attachment_filename=request.form['Titre']+'.xml', as_attachment=True)


@app.route('/uploadJson')
def uploadJson():
    return render_template('uploadJson.html', app_data=app_data)

@app.route('/arabicPoet')
def arabicPoet():
    return render_template('arabicPoet.html', app_data=app_data)


@app.route('/arabicEx',methods=['GET','POST'])
def arabicEx():
        return send_file('arabic poet example.json' ,as_attachment=True)

@app.route('/usersEx',methods=['GET','POST'])
def usersEx():
        return send_file('utilisateurs.json' ,as_attachment=True)

@app.route('/uploadarabic',methods=['GET','POST'])
def uploadarabic():
        return render_template('uploadarabic.html', app_data=app_data)

@app.route('/arabictoTei' , methods=['GET','POST'])
def arabictoTei() :
    xmlFile = 'file_generated.xml'
    jsonarabic = request.files['arabicpoet']
    filename = secure_filename(jsonarabic.filename)
    jsonarabic.save(os.path.join(filename))
    xmlData = open(xmlFile, 'w',encoding='utf-8')
    with open(filename, encoding='utf8') as json_file: 
        data = json.load(json_file) 
        xmlData.write('<?xml version="1.0" encoding="UTF-8"?><TEI xmlns="http://www.tei-c.org/ns/1.0" rendition="tei:teisimple">'+"\n"
        +'  '+'<teiHeader>'+"\n"
        +'   '+'<fileDesc>'+"\n"
         +'    '+'<titleStmt>'+"\n"
            +'     '+'<title>'+data['data']['title']+'</title>'+"\n"
         +'    '+'</titleStmt>'+"\n"
         +'    '+'<publicationStmt>'+"\n"
            +'     '+'<p>'+str(data['data']['year'])+'</p>'+"\n"
         +'    '+'</publicationStmt>'+"\n"
         +'    '+'<sourceDesc>'+"\n"
            +'     '+'<p>'+data['data']['poet']+'</p>'+"\n"
         +'    '+'</sourceDesc>'+"\n"
        +'   '+'</fileDesc>'+"\n"
        +'  '+'</teiHeader>'+"\n"
        +'  '+'<text>'+"\n"
        +'   '+'<body>'+"\n")
        xmlData.write('     '+'<lg type="stanza">' + "\n")
# Opening JSON file 

    # Print the type of data variable 

        for i in data['content']: 
            
            xmlData.write('      '+'<lg type="couplet">' + "\n")
            xmlData.write('       '+'<' + 'l'+ '>'+i['first']
                        + '</' + 'l' +'>' + "\n")
            xmlData.write('       '+'<' + 'l' + '>'+i['second']
                        + '</' + 'l' +'>' + "\n")
            xmlData.write('      '+'</lg>' + "\n")
        xmlData.write('     '+'</lg>' + "\n")
        xmlData.write('   '+'</body>'+"\n"
        +'  '+'</text>'+"\n"
        +'</TEI>')
    xmlData.close() 
    return send_file('file_generated.xml', attachment_filename=jsonarabic.filename.split('.')[0]+'.xml', as_attachment=True)

@app.route('/uploadUsers')
def uploadUsers():
    return render_template('uploadUsers.html', app_data=app_data)

@app.route('/userstoTei', methods=['GET','POST'])
def userstoTei():
    xmlFile = 'file_generated.xml'
    jsonusers = request.files['users']
    filename = secure_filename(jsonusers.filename)
    jsonusers.save(os.path.join(filename))
    xmlData = open(xmlFile, 'w',encoding='utf-8')
    with open(filename, encoding='utf8') as json_file: 
        data = json.load(json_file) 
        xmlData.write('<?xml version="1.0" encoding="UTF-8"?><TEI xmlns="http://www.tei-c.org/ns/1.0" rendition="tei:teisimple">'+"\n"
        +'  '+'<teiHeader>'+"\n"
        +'   '+'<fileDesc>'+"\n"
         +'    '+'<titleStmt>'+"\n"
            +'     '+'<title>'+request.form['Titre']+'</title>'+"\n"
         +'    '+'</titleStmt>'+"\n"
         +'    '+'<publicationStmt>'+"\n"
            +'     '+'<p>Pas des observations</p>'+"\n"
         +'    '+'</publicationStmt>'+"\n"
         +'    '+'<sourceDesc>'+"\n"
            +'     '+'<p>'+request.form['source']+'</p>'+"\n"
         +'    '+'</sourceDesc>'+"\n"
        +'   '+'</fileDesc>'+"\n"
        +'  '+'</teiHeader>'+"\n"
        +'  '+'<text>'+"\n"
        +'   '+'<body>'+"\n")
        xmlData.write('     '+'<table>' + "\n")
# Opening JSON file 

    # Print the type of data variable 

        for i in data['users']: 
            
            xmlData.write('      '+'<row>' + "\n")
            xmlData.write('       '+'<' + 'cell'+ '>'+str(i['userId'])
                        + '</' + 'cell' +'>' + "\n")
            xmlData.write('       '+'<' + 'cell'+ '>'+i['firstName']
                        + '</' + 'cell' +'>' + "\n")
            xmlData.write('       '+'<' + 'cell'+ '>'+i['lastName']
                        + '</' + 'cell' +'>' + "\n")
            xmlData.write('       '+'<' + 'cell'+ '>'+str(i['phoneNumber'])
                        + '</' + 'cell' +'>' + "\n")
            xmlData.write('       '+'<' + 'cell'+ '>'+i['emailAddress']
                        + '</' + 'cell' +'>' + "\n")
            xmlData.write('      '+'</row>' + "\n")
        xmlData.write('     '+'</table>' + "\n")
        xmlData.write('   '+'</body>'+"\n"
        +'  '+'</text>'+"\n"
        +'</TEI>')
    xmlData.close()
    return send_file('file_generated.xml', attachment_filename=request.form['Titre']+'.xml', as_attachment=True)

@app.route('/graphEx',methods=['GET','POST'])
def graphEx():
        return send_file('graph example.json' ,as_attachment=True)

@app.route('/uploadGraph')
def uploadGraph():
    return render_template('uploadGraph.html', app_data=app_data)

@app.route('/graphtoTei', methods=['GET','POST'])
def graphtoTei():
    xmlFile = 'file_generated.xml'
    jsonarabic = request.files['graph']
    filename = secure_filename(jsonarabic.filename)
    jsonarabic.save(os.path.join(filename))
    xmlData = open(xmlFile, 'w',encoding='utf-8')
    with open(filename, encoding='utf8') as json_file:
        data = json.load(json_file) 
        typee = data['type']
        idd = data['id']
        order = data['order']
        size = data['size']
        label = data['label']
        xmlData.write('<?xml version="1.0" encoding="UTF-8"?><TEI xmlns="http://www.tei-c.org/ns/1.0" rendition="tei:teisimple">'+"\n"
        +'  '+'<teiHeader>'+"\n"
        +'   '+'<fileDesc>'+"\n"
         +'    '+'<titleStmt>'+"\n"
            +'     '+'<title>'+label+'</title>'+"\n"
         +'    '+'</titleStmt>'+"\n"
         +'    '+'<publicationStmt>'+"\n"
            +'     '+'<p>''</p>'+"\n"
         +'    '+'</publicationStmt>'+"\n"
         +'    '+'<sourceDesc>'+"\n"
            +'     '+'<p>'+request.form['source']+'</p>'+"\n"
         +'    '+'</sourceDesc>'+"\n"
        +'   '+'</fileDesc>'+"\n"
        +'  '+'</teiHeader>'+"\n"
        +'  '+'<text>'+"\n"
        +'   '+'<body>'+"\n")
        xmlData.write('     '+'<graph type='+ '"'+typee+'" xml:id='+'"'+idd+'" order='+'"'+order+'" size='+'"'+size+'"'+'>' + "\n")
        xmlData.write('      '+'<label>'+label+'</label>' +"\n")
# Opening JSON file 

    # Print the type of data variable 

        for i in data['node']: 
            
            xmlData.write('      '+'<node xml:id='+'"'+i['id']+'" degree='
            + '"'+i['degree']+'" adj='
            + '"'+i['adj']+'"'+'>' + "\n")
            xmlData.write('      '+'<label>'+i['label']+'</label>' + "\n" )
            xmlData.write('      '+'</node>' + "\n")
        xmlData.write('     '+'</graph>' + "\n")
        xmlData.write('   '+'</body>'+"\n"
        +'  '+'</text>'+"\n"
        +'</TEI>')
    xmlData.close() 
    return send_file('file_generated.xml', attachment_filename=jsonarabic.filename.split('.')[0]+'.xml', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)