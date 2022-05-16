from bottle import route, redirect, template,request,static_file,run
from adminModel import SQL_LoginModel
import adminControl, nastavnikControl,ucenikControl

dbl=SQL_LoginModel('baza2.db')

@route('/static/<filepath>')
def server_static(filepath):
    return static_file(filepath, root='./')


@route('/')
def login():
    adminControl.username_global=None
    nastavnikControl.username_global=None
    return template('administracija_html/naslovnica')

@route('/', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    rb=request.forms.get('rb')
    vrsta={'A':0,'N':1,'U':2}
    vr=vrsta[rb]
    ispravan=dbl.login_chek(username,password,vr)
    if ispravan:
        un = username
        if rb=='A':
            adminControl.username_global=username
            return redirect('/izbornikAdmin')
        elif rb=='N':
            nastavnikControl.username_global=username
            return  redirect('nastavnik/'+un)
        else:
            ucenikControl.username_global=username
            return  redirect('/ucenik/'+un)

    else:
        return "<p>Login failed.""</p>"



if __name__=='__main__':
    run(reloader=True,port=8083)
