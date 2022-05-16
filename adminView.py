from bottle import  template
class AdminView():

    #UCENIK
    @staticmethod
    def o_nastavnici_ucenici_predmeti():
        return  template('administracija_html/Admin_naslovna')
    #popis ucenika
    @staticmethod
    def a_ucenici(ucenici=[]):
        return  template('administracija_html/Ucenici_admin', title="Popis ucenika", ucenici=ucenici)
    @staticmethod
    def dodavanje_ucenika():
        return template('administracija_html/ucenik_dodaj')
    @staticmethod
    def dodavanje_ucenika_validacija(valid):
            return  template('administracija_html/dodavanje_ucenika_validacija',validacija=valid)
    @staticmethod
    def edit_ucenik(mb,ime,prezime,razred,odjeljenje):
        return template('administracija_html/ucenik_edit',mb=mb,ime=ime,prezime=prezime,razred=razred,odjeljenje=odjeljenje)
    @staticmethod
    def valid_edit_ucenik(mb,ime,prezime,razred,odjeljenje,validacija):
        return template('administracija_html/valid_edit_ucenik', mb=mb, ime=ime, prezime=prezime, razred=razred, odjeljenje=odjeljenje,validacija=validacija)
    @staticmethod
    def ucenik_delete(mb,ime,prezime,razred,odjeljenje):
        return template('administracija_html/ucenik_delete', mb=mb, ime=ime, prezime=prezime, razred=razred, odjeljenje=odjeljenje)

    #PREDMET
    """
    @staticmethod
    def lista_predmeta(predmeti=[]):
        return  template('administracija_html/predmeti_lista',title='Lista predmeta',predmeti=predmeti)

    @staticmethod
    def dodaj_predmet():
        return  template('administracija_html/dodaj_predmet', title='Dodaj predmet')

    @staticmethod
    def dodaj_predmet_validacija():
        return  template('administracija_html/dodaj_predmet_valid',title='Neispravan unos')
    @staticmethod
    def edit_predmet(mb,naziv,razina):
        return  template('administracija_html/edit_predmet',title='Uredi predmet',mb=mb,naziv=naziv,razina=razina)

    @staticmethod
    def edit_valid_predmet(mb,naziv,razina):
        return  template('administracija_html/edit_valid_predmet.html',title='Uredi predmet validacija',mb=mb,naziv=naziv,razina=razina)

    @staticmethod
    def predmet_delete(mb,naziv, razina):
        return template('predmet_delete', mb=mb, naziv=naziv,razina=razina)
    """
    #Nastavnici
    @staticmethod
    def nastavnik_popis(nastavnici=[]):
        return template('administracija_html/popis_nastavnika', title='Popis nastavnici',nastavnici=nastavnici)

    @staticmethod
    def nastavnik_dodaj():
        return template('administracija_html/add_nastavnik', title='Dodavanje nastavnika')

    @staticmethod
    def dodavanje_nastavnik_validacija(val):
        return template('administracija_html/add_nastavnik_valid', title='Validacija nastavnika',validacija=val)

    @staticmethod
    def edit_nastavnik(mb,ime,prezime):
        return template('administracija_html/edit_nastavnik', title='Uredi nastavnika',mb=mb,ime=ime,prezime=prezime)

    @staticmethod
    def valid_edit_nastavnik(mb, ime, prezime, validacija):
        return template('administracija_html/edit_nastavnik_valid', title='Uredi nastavnika validacija', mb=mb, ime=ime, prezime=prezime,validacija=validacija)

    @staticmethod
    def nastavnik_delete(mb,ime,prezime):
        return template('administracija_html/nastavnik_delete',title='Brisanje nastavnika', mb=mb, ime=ime, prezime=prezime)

    @staticmethod
    def kordinacija(pn=[], nastavnici=[],pp=[]):
        return  template('administracija_html/kordinacija',title='Predmet-nastavnik',pn=pn,nastavnici=nastavnici,pp=pp)

    @staticmethod
    def razrednik(razredi1=[],razredi2=[]):
        return template('administracija_html/razrednik',title="Odabir razrednika", razredi1=razredi1,razredi2=razredi2)

    @staticmethod
    def razrednik_add(slobodni=[], mbr=None,r=None,od=None):
        return template('administracija_html/razrednik_add',title='Dodaj razrednika',mbr=mbr,r=r,od=od, slobodni=slobodni)


    @staticmethod
    def popis_razreda(razred=[]):
        return  template('administracija_html/popis_razreda',title='Popis razreda',razred=razred)

    @staticmethod
    def razred_nastava(uneseni=[], mogucnosti=[],razred_maticni=None):
        return  template('administracija_html/razred_nastava',title='Razred nastava povezivanje',uneseni=uneseni, mogucnosti=mogucnosti,razred_maticni=razred_maticni)

    @staticmethod
    def popis_rn(popis=[],a=None, mat=None):
        return  template('administracija_html/popis_predmeta_razred',title="Popis predmeta",popis=popis,a=a,maticni_razreda=mat)











