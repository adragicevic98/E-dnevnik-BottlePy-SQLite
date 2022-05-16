from bottle import  template

class UcenikView():
    
    @staticmethod
    def o_osobni_ocjene(podaci,ocjene,prosjek_p_p,ukupan_prosjek):
        return template('ucenik_html/Ucenik_naslovna',podaci=podaci,ocjene=ocjene,prosjek_p_p=prosjek_p_p,ukupan_prosjek=ukupan_prosjek)
