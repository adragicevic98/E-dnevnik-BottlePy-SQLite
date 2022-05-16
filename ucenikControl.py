from bottle import route, request, redirect
from UcenikModel import UcenikModel
from ucenikView import  UcenikView


dbu=UcenikModel('baza2.db')
#dbo=SQL_OcjenaModel('baza2.db')
username_global=None
un=None
ui=UcenikView()
def neispravanIdentitet():
    return '<h1> Zabranjen pristup prijavite se: <a href="/">ovdje</a></h1>'
# OCJENE popis
@route('/ucenik/<username>')
def ucenik_izbornik_ocjene(username):
    global username_global
    if (username_global is None): return neispravanIdentitet()
    maticni_ucenika=int(username[:-1])
    podaci,ocjene_rijecnik,prosjek_po_predmetu,ukupan_prosjek=dbu.ispis_ocjene_ucenik(maticni_ucenika)
    return ui.o_osobni_ocjene(podaci=podaci,ocjene=ocjene_rijecnik,prosjek_p_p=prosjek_po_predmetu,ukupan_prosjek=ukupan_prosjek)



