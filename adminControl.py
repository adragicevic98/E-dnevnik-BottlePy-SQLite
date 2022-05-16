from bottle import route, request,redirect
from  adminView import  AdminView
from adminModel import SQLUcenikModel,SQL_LoginModel,SQLRazredModel,SQL_PredmetModel,SQL_NastavnikModel,SQL_Predmet_Nastavnik,SQL_Razred_Pn,SQL_OcjenaModel

dbu=SQLUcenikModel('baza2.db')
dbr=SQLRazredModel('baza2.db')
dbl=SQL_LoginModel('baza2.db')
dbp=SQL_PredmetModel('baza2.db')
dbn=SQL_NastavnikModel('baza2.db')
dbpn=SQL_Predmet_Nastavnik('baza2.db')
dbr_pn=SQL_Razred_Pn('baza2.db')
dbo=SQL_OcjenaModel('baza2.db')
ai=AdminView()
username_global=None
val_uc={}
val_n={}


def neispravanIdentitet():
    return '<h1> Zabranjen pristup prijavite se: <a href="/">ovdje</a></h1>'

@route('/izbornikAdmin')
def  admin_izbornik():
    if(username_global is None):return neispravanIdentitet()
    return  ai.o_nastavnici_ucenici_predmeti()

 # UCENIK popis
@route('/izbornikAdmin/ucenik')
def admin_izbornik_ucenik():
    if (username_global is None): return neispravanIdentitet()
    ucenici=dbu.ucenik_select()
    return  ai.a_ucenici(ucenici=ucenici)

#Ucenik trazilica
@route ("/izbornikAdmin/ucenik", method="POST")
def admin_trazilica():
    if (username_global is None): return neispravanIdentitet()
    prez=request.forms.get('prezime')
    prez=prez.title()
    return  ai.a_ucenici(ucenici=dbu.ucenik_select(mb=prez))

#Ucenik dodavanje
@route ("/izbornikAdmin/ucenik/add")
def dodavanje_ucenika():
    if (username_global is None): return neispravanIdentitet()
    return ai.dodavanje_ucenika()

#Ucenik add validacija
@route ("/izbornikAdmin/ucenik/valid")
def dodaj_ucenik_validacija():
    if (username_global is None): return neispravanIdentitet()
    return ai.dodavanje_ucenika_validacija(val_uc)

#Ucenik uredjivanje
@route("/izbornikAdmin/ucenik/edit/<mb>")
def uredjivanje_ucenika(mb):
    if (username_global is None): return neispravanIdentitet()
    mb,ime,prezime,razred,odjeljenje,username=dbu.ucenik_select(mb=mb)[0]
    return ai.edit_ucenik(mb,ime,prezime,razred,odjeljenje)

#Ucenik validaciaja edit
@route("/izbornikAdmin/ucenik/valid_edit/<mb>")
def uredjivanje_ucenik_valid(mb):
    if (username_global is None): return neispravanIdentitet()
    mb, ime, prezime, razred, odjeljenje, username = dbu.ucenik_select(mb=mb)[0]
    return ai.valid_edit_ucenik(mb,ime,prezime,razred,odjeljenje,validacija=val_uc)

#Ucenik delete
@route ("/izbornikAdmin/ucenik/delete/<mb>")
def delete_ucenik(mb):
    if (username_global is None): return neispravanIdentitet()
    mb,ime,prezime,razred,odjeljenje,username=dbu.ucenik_select(mb=mb)[0]
    return ai.ucenik_delete(mb=mb,ime=ime,prezime=prezime,razred=razred,odjeljenje=odjeljenje)

#Ucenik submit delete
@route("/delete_ucenik", method="POST")
def submit_delete():
    if (username_global is None): return neispravanIdentitet()
    akcija=request.forms.get('action')
    mb=request.forms.get('maticni')
    if 'Izb' in akcija:
        username=dbu.ucenik_delete(mb=mb)
        dbl.login_delete(username)
        dbo.delete_ocjena(mb)


    redirect('/izbornikAdmin/ucenik')


#Ucenik submit za dodavanje i edit
@route ('/submit_ucenik', method="POST")
def ucenik_prihvacanje():
    if (username_global is None): return neispravanIdentitet()
    ime=request.forms.get('firstname')
    prezime=request.forms.get('lastname')
    razred=request.forms.get('razred')
    odjeljenje=request.forms.get('odjeljenje')
    action=request.forms.get('action')
    mb=request.forms.get('mb')
    ispravan=ucenik_validiraj(ime=ime,prezime=prezime,razred=razred,odjeljenje=odjeljenje)
    if ispravan:
        if action=='Dodaj':
            dbl.login_insert(dbu.ucenik_insert(ime=ime,prezime=prezime,razred=razred,slovo=odjeljenje))
        elif action=='Uredi':
            if(request.forms.get('stara_razina'))!=razred:
                dbo.delete_ocjena(mb)
            dbu.ucenik_edit(ime=ime,prezime=prezime,razred=razred,odjeljenje=odjeljenje,mb=mb)
        redirect("/izbornikAdmin/ucenik")
    else:
        if action=='Dodaj':
            redirect("/izbornikAdmin/ucenik/valid")
        else:
            redirect("izbornikAdmin/ucenik/valid_edit/"+str(mb))

#Ucenik validacija unosa
def ucenik_validiraj(ime=None,prezime=None,razred=None, odjeljenje=None):
    kategorija='abc'
    ispravan=True
    global  val_uc
    validacija={'Ime':'','Prezime':'', 'Razred':'','Odjeljenje': ''}
    if  len(odjeljenje)!=1 or odjeljenje.lower() not in kategorija:
        validacija['Odjeljenje']='Neispravno '+odjeljenje
        ispravan=False
    if  str(razred).isnumeric():
        razred=float(razred)
        if not razred.is_integer():
            validacija['Razred'] = 'Neispravno ' + str(razred)
            ispravan = False
        elif (int(razred)<1 or int(razred)>8):
            validacija['Razred'] = 'Neispravno ' + str(razred)
            ispravan = False
    else:
        validacija['Razred'] = 'Neispravno ' + str(razred)
        ispravan = False
    if not  ime.isalpha() or len(ime) <= 1:
        validacija['Ime']="Neispravno "+ str(ime)
        ispravan=False
    if not  prezime.isalpha() or len(prezime)<=1:
        validacija['Prezime']='Neispravno '+ str(prezime)
        ispravan=False
    val_uc=validacija
    return ispravan


#Predmete triba brisat
"""
@route("/izbornikAdmin/predmet")
def popis_predmeta():
    if (username_global is None): return neispravanIdentitet()
    predmeti=dbp.select_predmet()
    return  ai.lista_predmeta(predmeti)

@route("/izbornikAdmin/predmet/add")
def dodaj_predmet():
    if (username_global is None): return neispravanIdentitet()
    return ai.dodaj_predmet()

@route("/submit_predmet", method="POST")
def submit_predmet():
    if (username_global is None): return neispravanIdentitet()
    naziv=request.forms.get('naziv')
    razina=request.forms.get('razina')
    action=request.forms.get('action')
    mb=request.forms.get('mb')
    if (validacija_predmet(naziv,razina)):
        if action=="Dodaj":
            dbp.insert_predmet(naziv,razina)
        elif action=="Uredi":
            dbp.edit_predmet(mb,naziv,razina)
        redirect("/izbornikAdmin/predmet")
    else:
        if action=='Dodaj':
            redirect("/izbornikAdmin/predmet/valid")
        else:
            redirect("/izbornikAdmin/predmet/valid_edit/"+str(mb))

@route("/izbornikAdmin/predmet/valid")
def predmet_valid_add():
    if (username_global is None): return neispravanIdentitet()
    return ai.dodaj_predmet_validacija()

@route("/izbornikAdmin/predmet/edit/<mb>")
def edit_predmet(mb):
    if (username_global is None): return neispravanIdentitet()
    mb,naziv,razina=dbp.select_predmet(mb)[0]
    return ai.edit_predmet(mb,naziv,razina)

@route("/izbornikAdmin/predmet/valid_edit/<mb>")
def edit_valid_predmet(mb):
    if (username_global is None): return neispravanIdentitet()
    mb, naziv, razina = dbp.select_predmet(mb)[0]
    return  ai.edit_valid_predmet(mb,naziv,razina)

@route ("/izbornikAdmin/predmet/delete/<mb>")
def delete_predmet(mb):
    if (username_global is None): return neispravanIdentitet()
    mb,naziv,razina=dbp.select_predmet(mb=mb)[0]
    return ai.predmet_delete(mb=mb,naziv=naziv,razina=razina)


@route("/delete_predmet", method="POST")
def submit_delete_predmet():
    if (username_global is None): return neispravanIdentitet()
    akcija=request.forms.get('action')
    mb=request.forms.get('maticni')
    if 'Izb' in akcija:
        #brisanje pn tablice kad se brise predmet
        dbp.delete_predmet(mb=mb)
    redirect('/izbornikAdmin/predmet')

"""
def validacija_predmet(naziv, razina):
    if ( dbp.select_predmet(naziv=naziv,razina=razina) != []):
        return False
    valid_predmeti={'Hrvatski':'12345678', 'Engleski':'12345678','Matematika':'12345678' ,'Tjelesni':'12345678','Priroda':'1234','Povijest':'5678','Geografija':'5678' ,'Biologija':'5678','Informatika':'5678','Tehnicki':'5678','Fizika':'78','Kemija':'78'}
    return   razina in valid_predmeti[naziv]
##Predmet
##Brisat do tu

#Nastavnik


 # nastavnik popis
@route('/izbornikAdmin/nastavnik')
def admin_popis_nastavnik():
    if (username_global is None): return neispravanIdentitet()
    nastavnici=dbn.select_nastavnik()
    return  ai.nastavnik_popis(nastavnici=nastavnici)

#nastavnik trazilica
@route ("/izbornikAdmin/nastavnik", method="POST")
def admin_trazilica_nastavnik():
    if (username_global is None): return neispravanIdentitet()
    prez=request.forms.get('prezime')
    prez=prez.title()
    return  ai.nastavnik_popis(nastavnici=dbn.select_nastavnik(mb=prez))

#nastavnik dodavanje
@route ("/izbornikAdmin/nastavnik/add")
def dodavanje_nastavnik():
    if (username_global is None): return neispravanIdentitet()
    return ai.nastavnik_dodaj()

#nastavnik add validacija
@route ("/izbornikAdmin/nastavnik/valid")
def dodaj_nastavnik_validacija():
    if (username_global is None): return neispravanIdentitet()
    return ai.dodavanje_nastavnik_validacija(val_n)

#nastavnik uredjivanje
@route("/izbornikAdmin/nastavnik/edit/<mb>")
def uredjivanje_nastavnik(mb):
    if (username_global is None): return neispravanIdentitet()
    mb,ime,prezime,username=dbn.select_nastavnik(mb=mb)[0]
    return ai.edit_nastavnik(mb,ime,prezime)

#nastavnik validaciaja edit
@route("/izbornikAdmin/nastavnik/valid_edit/<mb>")
def uredjivanje_nastavnik_valid(mb):
    if (username_global is None): return neispravanIdentitet()
    mb, ime, prezime,username = dbn.select_nastavnik(mb=mb)[0]

    return ai.valid_edit_nastavnik(mb,ime,prezime,validacija=val_n)

#nastavnik delete
@route ("/izbornikAdmin/nastavnik/delete/<mb>")
def delete_nastavnik(mb):
    if (username_global is None): return neispravanIdentitet()
    mb,ime,prezime,username=dbn.select_nastavnik(mb=mb)[0]
    return ai.nastavnik_delete(mb=mb,ime=ime,prezime=prezime)

#nastavnik submit delete
@route("/delete_nastavnik", method="POST")
def submit_delete_nastavnik():
    if (username_global is None): return neispravanIdentitet()
    akcija=request.forms.get('action')
    mb=request.forms.get('maticni')
    if 'Izb' in akcija:
        dbl.login_delete(dbn.delete_nastavnik(mb=mb))

        #brisanje pn tablice

    redirect('/izbornikAdmin/nastavnik')


#nastavnik submit za dodavanje i edit
@route ('/submit_nastavnik', method="POST")
def nastavnik_prihvacanje():
    if (username_global is None): return neispravanIdentitet()
    ime=request.forms.get('firstname')
    prezime=request.forms.get('lastname')
    action=request.forms.get('action')
    mb=request.forms.get('mb')
    ispravan=nastavnik_validiraj(ime=ime,prezime=prezime)
    if ispravan:
        if action=='Dodaj':
            dbl.login_insert(dbn.insert_nastavnik(ime=ime,prezime=prezime))

        elif action=='Uredi':
            dbn.nastavnik_edit(ime=ime,prezime=prezime,mb=mb)
        redirect("/izbornikAdmin/nastavnik")
    else:
        if action=='Dodaj':
            redirect("/izbornikAdmin/nastavnik/valid")
        else:
            redirect("izbornikAdmin/nastavnik/valid_edit/"+str(mb))

#nastavnik validacija unosa
def nastavnik_validiraj(ime=None,prezime=None):
    ispravan=True
    global  val_n
    validacija={'Ime':'','Prezime':''}
    if not  ime.isalpha() or len(ime) <= 1:
        validacija['Ime']="Neispravno "+ str(ime)
        ispravan=False
    if not  prezime.isalpha() or len(prezime)<=1:
        validacija['Prezime']='Neispravno '+ str(prezime)
        ispravan=False
    val_n=validacija
    return ispravan



#Kordinacija


def oblikovanje_ucitelja():
     popis=dbpn.popis_ucitelja_Predmet_Nastavnik()
     if(len(popis)==0): return []
     nastavnik_mb=[]
     mbovi=[]
     for i in popis:
         if  i[-1]not in mbovi:
             nastavnik_mb.append((i[0],i[1],i[2],i[3],'1-4',i[5],i[6]))
             mbovi.append(i[-1])
     return  nastavnik_mb
def oblikovanje_profesora():
    popis = dbpn.popis_profesora_Predmet_Nastavnik()
    if (len(popis) == 0): return []
    nastavnik_mb = []
    predmeti = []
    for i in popis:
        if i[4] not in predmeti:
            nastavnik_mb.append((i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
            predmeti.append(i[4])
    return nastavnik_mb
def valid_add_predmet_nastavnik(nastavnik_mb,predmeti_odabir):
    predmeti={'1':['Hrvatski','Matematika','Priroda','Tjelesni','Engleski'],'Hrvatski':[5,6,7,8], 'Matematika':[5,6,7,8], 'Engleski':[5,6,7,8],'Tjelesni':[5,6,7,8],'Geografija':[5,6,7,8],'Povijest':[5,6,7,8],'Biologija':[5,6,7,8],'Informatika':[5,6,7,8],'Tehnicki':[5,6,7,8],'Fizika':[7,8],'Kemija':[7,8]}
    razine=[1,2,3,4]
    if predmeti_odabir=='1':
        predmet=predmeti[predmeti_odabir]
        razine=[1,2,3,4]
        for i in predmet:
            for r in razine:
                if  not dbp.predmetPostoji(i,r):
                    dbp.insert_predmet(i,r)

                mb_predmeta=dbp.get_predmet_mb(i,r)
                if not dbpn.postojiPredmet_Nastavnik(PredmetID=mb_predmeta,NastavnikID=nastavnik_mb):
                    dbpn.insert_Predmet_Nastavnik(nastavnikID=nastavnik_mb,predmetID=mb_predmeta)
    else:
        predmet=predmeti_odabir
        razine=predmeti[predmeti_odabir]
        for r in razine:
            if  not dbp.predmetPostoji(predmet,r):
                dbp.insert_predmet(predmet,r)
            mb_predmeta=dbp.get_predmet_mb(predmet,r)
            if  not dbpn.postojiPredmet_Nastavnik(PredmetID=mb_predmeta,NastavnikID=nastavnik_mb):
                dbpn.insert_Predmet_Nastavnik(predmetID=mb_predmeta,nastavnikID=nastavnik_mb)

@route('/izbornikAdmin/kordinacija')
def kordinacija():
    if (username_global is None): return neispravanIdentitet()
    svi_nastavnici=dbpn.popis_sivh_profesora_za_Predmet_Nastavnik()
    nastavnici_ucitelji=oblikovanje_ucitelja()
    nastavnici_profeosri=oblikovanje_profesora()
    return ai.kordinacija(pn=nastavnici_ucitelji,nastavnici=svi_nastavnici,pp=nastavnici_profeosri)

@route('/add_pn',method='POST')
def dodaj_predmet_nastavnik():
    if (username_global is None): return neispravanIdentitet()
    odabir=request.forms.get('naziv')
    nastavnikID=request.forms.get('nastavnik')
    valid_add_predmet_nastavnik(nastavnikID,odabir)
    redirect('izbornikAdmin/kordinacija')


@route('/del_pu', method='POST')
def izbrisi_pn():
    if (username_global is None): return neispravanIdentitet()
    lista=dbp.get_predmet_mb_do_cetri()
    nastavnik_maticni=request.forms.get('nastavnikID')
    lista_pn_mb=dbpn.select_Predmet_Nastavnik_mb_lista_predmeta(nastavnikID=nastavnik_maticni,lista_predmeta=lista)
    if dbn.jeRazrednik(nastavnik_maticni):
        razred_mb=dbn.get_Razred_mb_od_Razrednik(nastavnik_maticni)[0]
        #ovde mozda bude problem ako nije razrednik onda nisu ni povezani
        for pnID in lista_pn_mb:
            dbr_pn.delete_Razred_PredmetNastavnik(pnID=pnID,razredID=razred_mb)
        dbr.razred_update_razrednik(mbr=razred_mb,razrednikID=None)
    for pn_mb in lista_pn_mb:
        dbpn.delete_Predmet_Nastavnik(mb=pn_mb)
    redirect('izbornikAdmin/kordinacija')


@route('/del_pp', method='POST')
def izbrisi_profesor_Predmet():
    if (username_global is None): return neispravanIdentitet()
    predmet_naziv=request.forms.get('predmet')
    lista_mb_predmeti=dbp.get_predmet_mb_od_cetri(predmet_naziv)
    print(lista_mb_predmeti)
    nastavnik_maticni=request.forms.get('nastavnikID')
    lista_pn_mb=dbpn.select_Predmet_Nastavnik_mb_lista_predmeta(nastavnikID=nastavnik_maticni,lista_predmeta=lista_mb_predmeti)
    if(dbn.jeRazrednik(nastavnik_maticni)):
        razred_mb = dbn.get_Razred_mb_od_Razrednik(nastavnik_maticni)[0]
        razred_razina=dbr.razred_select(razred_mb)
        if razred_razina[0][1]>4:
            # jos ovde sta ako to nije jedini predmet koji predaje
            #brisi ga jedino ako su svi maticni  pnmb prazni
            dbr.razred_update_razrednik(mbr=razred_mb, razrednikID=None)
    for pn_mb in lista_pn_mb:
        dbr_pn.delete_Razred_PredmetNastavnik(pnID=pn_mb)
        dbpn.delete_Predmet_Nastavnik(mb=pn_mb)
    redirect('izbornikAdmin/kordinacija')



@route('/izbornikAdmin/kordinacija/razrednik')
def razrednik():
    if (username_global is None): return neispravanIdentitet()
    razredi1=dbr.razred_bez_razrednika()
    razredi2=dbr.razred_sa_razredniom()
    return ai.razrednik(razredi1=razredi1,razredi2=razredi2)


def get_moguci_nastavnici(razina):
    moguci_razrednici=[]
    mp=[]
    if razina>4: lista=dbpn.popis_profesora_Predmet_Nastavnik()
    else:lista=dbpn.popis_ucitelja_Predmet_Nastavnik()
    if len(lista)==0: return []
    razrednici_duplicati=[(i[-1],i[1], i[2] ) for i in lista if not dbn.jeRazrednik(i[-1])]
    for i in razrednici_duplicati:
        if  i[0] not in mp:
            moguci_razrednici.append(i)
            mp.append(i[0])

    return moguci_razrednici

@route('/razrednik_add',method='POST')
def razrednik_add():
    if (username_global is None): return neispravanIdentitet()
    mb=request.forms.get('razredID1')
    mbr,r,od,rID=dbr.razred_select(mb=mb)[0]
    lista=get_moguci_nastavnici(r)
    lista2=[]
    for i in lista:
        a=(i[0],i[1],i[2],mb)
        lista2.append(a)

    return  ai.razrednik_add(mbr=mb ,r=r,od=od,slobodni=lista2)


@route('/submit_razrednik', method='POST')
def razrednik_submit():
    if (username_global is None): return neispravanIdentitet()
    mbr=request.forms.get('razred')
    rID=request.forms.get('razrednik')
    razred=dbr.razred_select(mb=mbr)[0]
    print(mbr)
    print(rID)
    dbr.razred_update_razrednik(mbr=mbr, razrednikID=rID)
    if razred[1]<5:
        pnID=dbpn.select2_mb_Predmet_Nastavnik(predmetRazina=razred[1],nastavnikID=rID)
        for pn in  pnID:
            dbr_pn.insert_Razred_PredmetNastavnik(razredID=mbr,pnID=pn)

    redirect('izbornikAdmin/kordinacija/razrednik')


@route('/razrednik_delete',method='POST')
def razrednik_ukloni():
    if (username_global is None): return neispravanIdentitet()
    mb=request.forms.get('razredID')
    razred_mb,razina,odjeljenje,razrednik=dbr.razred_select(mb=mb)[0]
    if razina<5:
        dbr_pn.delete_Razred_PredmetNastavnik2(razredID=razred_mb)

    dbr.razred_update_razrednik(razrednikID=None,mbr=mb)
    redirect('izbornikAdmin/kordinacija/razrednik')


@route('/izbornikAdmin/kordinacija/razred_nastava')
def popis_razreda():
    if (username_global is None): return neispravanIdentitet()
    popis=dbr.razred_select()
    return ai.popis_razreda(popis)


@route('/razred_uredi', method='POST')
def razred_postavka():
    if (username_global is None): return neispravanIdentitet()
    razina=request.forms.get('razred')
    rid=request.forms.get('razrednikID')
    mbr=request.forms.get('mbr')
    if int(razina)>4:
        mogucnosti=dbpn.select_popis_nastave_moguce(razina=int(razina))
        uneseni=dbr_pn.select_popis_unesene_nastave(int(razina))
        predmeti_uneseni = [i[3] for i in uneseni]
        mogucnosti2=[]
        for i,j in enumerate(mogucnosti):
            if j[1] not in predmeti_uneseni:
                mogucnosti2.append(mogucnosti[i])
        return  ai.razred_nastava(uneseni=uneseni,mogucnosti=mogucnosti2, razred_maticni=mbr)

    if rid=='None':
        redirect('/izbornikAdmin/kordinacija/razrednik')
    else:
        mbr,r,od,raz=dbr.razred_select(mb=mbr)[0]
        a=razina+' '+od
        popis=dbr_pn.select_popis_predmeta_po_razredu(mbr)
        return ai.popis_rn(popis=popis,a=a,mat=mbr)



@route('/razred_nastava_ukloni', method="POST")
def ukloni_razred_nastava():
    if (username_global is None): return neispravanIdentitet()
    predmetNastavnik_mb=request.forms.get('pn')
    razred_mb=request.forms.get('razred')
    dbr_pn.delete_Razred_PredmetNastavnik(razredID=razred_mb,pnID=predmetNastavnik_mb)
    redirect('/izbornikAdmin/kordinacija/razred_nastava')

@route('/razred_nastava_add', method="POST")
def dodaj_razred_nastava():
    if (username_global is None): return neispravanIdentitet()
    predmetNastavnik_mb=request.forms.get('pn')
    razred_mb=request.forms.get('razred')
    dbr_pn.insert_Razred_PredmetNastavnik(pnID=predmetNastavnik_mb,razredID=razred_mb)
    redirect('/izbornikAdmin/kordinacija/razred_nastava')





































