import sqlite3

class UcenikModel():

    def __init__(self,filename):
        self.conn=sqlite3.Connection(filename)
        self.cur=self.conn.cursor()
        self.filename=filename
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS Ucenik(
              mb integer INTEGER PRIMARY KEY,
              ime text NOT NULL,
              prezime text NOT NULL,
              razredID integer NOT NULL,
              username text NOT NULL,
              FOREIGN KEY (razredID) REFERENCES Razred (mb));
              
           CREATE TABLE IF NOT EXISTS Ocjena (
             mb integer PRIMARY KEY,
             ocjena integer,
             datum DATETIME NOT NULL,
             predmetID integer NOT NULL,
             ucenikID integer NOT NULL,
             nastavnik text NOT NULL,
             FOREIGN KEY (predmetID) REFERENCES Predmet (mb),
             FOREIGN KEY (ucenikID) REFERENCES Ucenik (mb));""")

    def zakljuci_ocjenu(self,ocjena):
        if ocjena<1.5:
            return 1
        elif ocjena<2.5:
            return 2
        elif ocjena<3.5:
            return 3
        elif ocjena<4.5:
            return 4
        else:
            return 5
    def ucenik_select_podaci(self,mb):
            self.cur.execute("""SELECT u.ime, u.prezime, u.mb, u.username, r.razina, r.odjeljenje FROM Ucenik u INNER JOIN Razred r ON u.razredID=r.mb WHERE  u.mb= ?  """,(mb,))
            return self.cur.fetchall()
    def ispis_ocjene_ucenik(self,mb):
        podaci=self.ucenik_select_podaci(mb)[0]
        self.cur.execute(
            """SELECT o.ocjena,o.datum,o.nastavnik,p.naziv FROM Ocjena o INNER JOIN Ucenik u ON u.mb=o.ucenikID  INNER JOIN Predmet p ON p.mb=o.predmetID WHERE u.mb= ?  ORDER BY o.predmetID, o.datum""",
            (mb,))
        ocjene=self.cur.fetchall()
        if(len(ocjene)==0):
            return (podaci,{},{},None)
        ocjene_dict={}
        for i in ocjene:
            if i[3]  not in ocjene_dict:
                ocjene_dict[i[3]]=[i[:-1]]
            else:
                ocjene_dict[i[3]].append(i[:3])
        prosjek_p_p={k: self.prosjek_po_predmetu(k,mb)  for k in ocjene_dict.keys()}
        ukupni_prosjek=round(sum(self.zakljuci_ocjenu(i) for i in prosjek_p_p.values()) /len(prosjek_p_p),2)
        return (podaci,ocjene_dict,prosjek_p_p,ukupni_prosjek)



    def prosjek_po_predmetu(self,kljuc,mb):
        self.cur.execute("""SELECT AVG(ocjena) FROM Ocjena o INNER JOIN Predmet p ON p.mb=o.predmetID where p.naziv=? and o.ucenikID=? ORDER BY datum """,
                         (kljuc, mb))
        prosjek=self.cur.fetchall()
        return round(prosjek[0][0],2)










    
