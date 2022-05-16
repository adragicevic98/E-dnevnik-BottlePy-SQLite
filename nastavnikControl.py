from bottle import  route, request,redirect
from NastavnikModel import  NastavnikModel
from nastavnikView import NastavnikView
from datetime import date

nastavnik=NastavnikModel('baza2.db')
ni=NastavnikView()
username_global=None
mb=None
ime=None
prezime=None
def neispravanIdentitet():
    return '<h1> Zabranjen pristup prijavite se: <a href="/">ovdje</a></h1>'

def podaci_nastavnik():
    global ime
    global prezime
    global  mb
    global  username_global
    return (ime, prezime, username_global)

@route('/nastavnik/<un>')
def nastavnik_naslovna(un):
   global username_global
   if (username_global is None): return neispravanIdentitet()
   global mb
   global ime
   global prezime
   mb, ime, prezime, username_global=nastavnik.select_nastavnik(un)
   razredi=nastavnik.select_razredi(mb)
   return ni.nastavnik_naslovna(ime, prezime, username_global, mb, razredi)

@route('/')
def odjava():
    global mb
    global username_global
    global ime
    global prezime
    mb=None
    username_global=None
    ime=None
    prezime=None
    redirect('/')

@route('/razred_odabir',method='POST')
def odabir_razreda():
    if (username_global is None): return neispravanIdentitet()
    razina=request.forms.get('razred')
    mbr=request.forms.get('mb')
    odjeljenje=request.forms.get('odjeljenje')
    if int(razina)>4:
        redirect('/nastavnik/razred/visi/'+str(mbr))
    else:
        redirect('/nastavnik/razred/nizi/'+str(mbr))

@route('/nastavnik/razred/nizi/<mbr>')
def popis_predmeta(mbr):
    if (username_global is None): return neispravanIdentitet()
    predmeti=nastavnik.select_predmeti_nizi(mbr)
    razredopis=nastavnik.dohvati_razred(mbr)
    return ni.odabir_predmeta(ime=ime, prezime=prezime, username=username_global, mbr=mbr, razredopis=razredopis, predmeti=predmeti)

@route('/nastavnik/razred/visi/<mbr>')
def popis_predmeta(mbr):
    if (username_global is None): return neispravanIdentitet()
    global mb
    predmeti=nastavnik.select_predmeti_visi(mbr,mb)
    razredopis = nastavnik.dohvati_razred(mbr)
    return ni.odabir_predmeta(ime=ime, prezime=prezime, username=username_global, mbr=mbr, razredopis=razredopis, predmeti=predmeti)

@route('/predmet_odabir',method="POST")
def predmet_odabran():
    if (username_global is None): return neispravanIdentitet()
    mb_predmet=request.forms.get('mbpredmet')
    mb_razred=request.forms.get('mbrazred')
    redirect('/nastavnik/odabir_ucenika/'+mb_razred+'/'+mb_predmet)

@route('/nastavnik/odabir_ucenika/<maticni_razred>/<maticni_predmet>')
def popis_ucenika(maticni_razred,maticni_predmet):
    if (username_global is None): return neispravanIdentitet()
    ucenici=nastavnik.select_ucenik(maticni_razred=maticni_razred)
    razred_predmet_opis=(nastavnik.dohvati_razred(maticni_razred),nastavnik.dohvati_predmet(maticni_predmet))
    return ni.odabir_ucenika(ime=ime, prezime=prezime, username=username_global, maticni_razreda=maticni_razred, maticni_predmeta=maticni_predmet, razred_predmet_opis=razred_predmet_opis, ucenici=ucenici)


@route('/ucenik_odabir',method='POST')
def prikaz_ocjena():
    if (username_global is None): return neispravanIdentitet()
    maticni_ucenik=request.forms.get('maticni_ucenik')
    maticni_predmet = request.forms.get('maticni_predmet')
    maticni_razred = request.forms.get('maticni_razred')
    redirect('/nastavnik/popis_ocjena/'+maticni_razred+'/'+maticni_predmet+'/'+maticni_ucenik)

@route('/nastavnik/popis_ocjena/<maticni_razred>/<maticni_predmet>/<maticni_ucenik>')
def popis_ocjena(maticni_razred,maticni_predmet,maticni_ucenik):
    if (username_global is None): return neispravanIdentitet()
    informacije=(nastavnik.dohvati_razred(maticni_razred),nastavnik.dohvati_predmet(maticni_predmet),nastavnik.dohvati_ucenik(maticni_ucenik))
    ocjene,prosjek=nastavnik.select_ocjena(maticni_predmet,maticni_ucenik)
    ime,prezime,username=podaci_nastavnik()
    return ni.ocjene(prosjek=prosjek,ime=ime,prezime=prezime,username=username,maticni_razreda=maticni_razred,maticni_predmeta=maticni_predmet,informacije=informacije,maticni_ucenika=maticni_ucenik,ocjene=ocjene)


@route('/ocjena_add', method='POST')
def dodaj_ocjenu():
    if (username_global is None): return neispravanIdentitet()
    mb_ucenik=request.forms.get('maticni_ucenik')
    mb_razred=request.forms.get('maticni_razred')
    mb_predmet=request.forms.get('maticni_predmet')
    ocjena=int(request.forms.get('ocjena'))
    datum=request.forms.get('datum')
    nastavnik_podaci=request.forms.get('ime_nastavnik')+' '+request.forms.get('prezime_nastavnik')
    #g m d
    g,m,d=datum.split('-')
    datum2=date(int(g),int(m),int(d))
    nastavnik.insert_ocjena(ocjena=int(ocjena),mb_ucenik=int(mb_ucenik),mb_predmet=int(mb_predmet),datum=datum2,nastavnik=nastavnik_podaci)
    redirect('/nastavnik/popis_ocjena/'+str(mb_razred)+'/'+str(mb_predmet)+'/'+str(mb_ucenik))


@route('/ocjena_brisi_azur',method='POST')
def brisi_ocjenu():
    if (username_global is None): return neispravanIdentitet()
    maticni_ocjena=request.forms.get('mb_ocjena')
    razred=request.forms.get('razred')
    predmet=request.forms.get('predmet')
    ucenik=request.forms.get('ucenik')
    akcija=request.forms.get('akcija')
    if akcija=='Izbrisi':
        nastavnik.delete_ocjena(maticni_ocjena)
        redirect('/nastavnik/popis_ocjena/'+str(razred)+'/'+str(predmet)+'/'+str(ucenik))
    else:
        redirect('/ocjena_azuriraj/'+str(razred)+'/'+str(predmet)+'/'+str(ucenik)+'/'+str(maticni_ocjena))

@route('/ocjena_azuriraj/<maticni_razred>/<maticni_predmet>/<maticni_ucenik>/<maticni_ocjena>')
def ocjena_azuriraj(maticni_razred,maticni_predmet,maticni_ucenik,maticni_ocjena):
    if (username_global is None): return neispravanIdentitet()
    ime, prezime, username = podaci_nastavnik()
    ocjena,datum=nastavnik.dohvati_ocjena(maticni_ocjena)
    informacije=(nastavnik.dohvati_ucenik(maticni_ucenik),ocjena,nastavnik.dohvati_predmet(maticni_predmet),datum)
    return ni.ocjena_azuriraj( ime=ime, prezime=prezime, username=username, maticni_razreda=maticni_razred,maticni_predmeta=maticni_predmet,mb=maticni_ocjena ,informacije=informacije, maticni_ucenika=maticni_ucenik)


@route('/submit_ocjena',method="POST")
def ocjena_submit():
    if (username_global is None): return neispravanIdentitet()
    mb_ucenik=request.forms.get('maticni_ucenik')
    mb_razred=request.forms.get('maticni_razred')
    mb_predmet=request.forms.get('maticni_predmet')

    mb_ocjena=request.forms.get('maticni_ocjena')
    ocjena=int(request.forms.get('ocjena'))
    datum=request.forms.get('datum')
    g,m,d=datum.split('-')
    datum2=date(int(g),int(m),int(d))
    nastavnik_podaci = request.forms.get('ime_nastavnik') + ' ' + request.forms.get('prezime_nastavnik')
    nastavnik.ocjena_update(mb_ocjena=mb_ocjena,ocjena=ocjena,datum=datum2,nastavnik=nastavnik_podaci)

    redirect('/nastavnik/popis_ocjena/' + str(mb_razred) + '/' + str(mb_predmet) + '/' + str(mb_ucenik))










































