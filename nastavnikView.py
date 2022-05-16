from bottle import  template

class NastavnikView():

    @staticmethod
    def nastavnik_naslovna(ime,prezime,username,mb,razredi=[]):
        return  template('nastavnik_html/nastavnik_naslovna',razredi=razredi,ime=ime,prezime=prezime,mb=mb,un=username)

    @staticmethod
    def odabir_predmeta(ime,prezime,username,mbr,razredopis,predmeti=[]):
        return template('nastavnik_html/predmeti_odabir',ime=ime,prezime=prezime,un=username,mbr=mbr,razredopis=razredopis,predmeti=predmeti)

    @staticmethod
    def odabir_ucenika(ime,prezime,username,maticni_razreda,maticni_predmeta,razred_predmet_opis,ucenici=[]):
        return template('nastavnik_html/ucenik_odabir', ime=ime, prezime=prezime, un=username,maticni_razreda=maticni_razreda,maticni_predmeta=maticni_predmeta,rp_o=razred_predmet_opis,ucenici=ucenici)

    @staticmethod
    def ocjene(prosjek,ime,prezime,username,maticni_razreda,maticni_predmeta,informacije,maticni_ucenika,ocjene=[]):
        return template('nastavnik_html/ocjene', ime=ime, prezime=prezime, un=username,maticni_razreda=maticni_razreda,maticni_predmeta=maticni_predmeta,maticni_ucenika=maticni_ucenika,rp_o=informacije,ocjene=ocjene,prosjek=prosjek)

    @staticmethod
    def ocjena_azuriraj(ime,prezime,username,maticni_razreda,maticni_predmeta,maticni_ucenika,mb,informacije):
        return template('nastavnik_html/ocjena_azuriraj', ime=ime, prezime=prezime, un=username,mb=mb, maticni_razreda=maticni_razreda,maticni_predmeta=maticni_predmeta,rp_o=informacije, maticni_ucenika=maticni_ucenika)








