import sqlite3

def pr(lista_id):
    for i in range(0, len(lista_id)):
        if (i + 1) not in lista_id:
            return i + 1
    return len(lista_id) + 1


class NastavnikModel():
    def __init__(self,filename):
        self.conn = sqlite3.Connection(filename)
        self.cur = self.conn.cursor()
        self.filename = filename
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS Ocjena (
            mb integer PRIMARY KEY,
            ocjena integer,
            datum DATETIME NOT NULL,
            predmetID integer NOT NULL,
            ucenikID integer NOT NULL,
            nastavnik text NOT NULL,
            FOREIGN KEY (predmetID) REFERENCES Predmet (mb),
            FOREIGN KEY (ucenikID) REFERENCES Ucenik (mb));""")

    def select_razredi(self,mb):
        self.cur.execute(
            """SELECT DISTINCT r.mb, r.razina, r.odjeljenje  FROM Razred r INNER JOIN Razred_pn rpn ON r.mb=rpn.razredID INNER JOIN Predmet_Nastavnik pn ON pn.mb=rpn.pnID WHERE pn.nastavnikID= ? ORDER BY r.razina""",(mb,))
        return self.cur.fetchall()
    def select_nastavnik(self,un):
        self.cur.execute(
            """SELECT * FROM Nastavnik where username= ?""",(un,))
        return self.cur.fetchall()[0]

    def select_predmeti_nizi(self,mb):
        #pripazi postoji li predmet
        self.cur.execute(
            """SELECT p.mb, p.naziv, p.razina  FROM Razred r INNER JOIN Razred_pn rpn ON r.mb=rpn.razredID INNER JOIN Predmet_Nastavnik pn ON pn.mb=rpn.pnID INNER JOIN Predmet p ON p.mb=pn.predmetID WHERE r.mb= ? ORDER BY p.naziv""",(mb,))
        return self.cur.fetchall()

    def select_predmeti_visi(self,mb_razred,mb_nastavnik):
        #pripazi postoji li predmet
        print(mb_nastavnik)
        self.cur.execute(
            """SELECT p.mb, p.naziv, p.razina  FROM Razred r INNER JOIN Razred_pn rpn ON r.mb=rpn.razredID INNER JOIN Predmet_Nastavnik pn ON pn.mb=rpn.pnID INNER JOIN Predmet p ON p.mb=pn.predmetID WHERE r.mb= ? and pn.NastavnikID= ? ORDER BY p.naziv""",(mb_razred,mb_nastavnik))
        return self.cur.fetchall()

    def select_ucenik(self,maticni_razred):
        self.cur.execute(
            """SELECT *  FROM Ucenik where razredID= ? """,(maticni_razred,))
        return self.cur.fetchall()

    def dohvati_razred(self,maticni_razred):
       self.cur.execute( """SELECT razina, odjeljenje  FROM Razred where mb= ? """, (maticni_razred,))
       a,b=self.cur.fetchall()[0]
       return str(a)+' '+b

    def dohvati_predmet(self,maticni_predmet):
        self.cur.execute("""SELECT naziv   FROM Predmet where mb= ? """, (maticni_predmet,))
        return  self.cur.fetchall()[0][0]

    def dohvati_ucenik(self,maticni_ucenik):
        self.cur.execute("""SELECT ime,prezime   FROM Ucenik where mb= ? """, (maticni_ucenik,))
        a,b=self.cur.fetchall()[0]
        return  a+' '+b

    def dohvati_ocjena(self,mb):
        self.cur.execute("""SELECT ocjena,datum   FROM Ocjena where mb= ? """, (mb,))
        a,b=self.cur.fetchall()[0]
        return  (a,b)




    def insert_ocjena(self,ocjena,mb_ucenik,mb_predmet,datum,nastavnik):
        self.cur.execute("""SELECT mb FROM Ocjena""")
        id = self.cur.fetchall()
        id=[int(i[0])for i in id]
        mb=pr(id)
        self.cur.execute("""
             INSERT INTO Ocjena
             (mb, ocjena, datum,predmetID,ucenikID,nastavnik)
               VALUES (?, ?, ?, ?, ?, ?)""", (mb, ocjena, datum,mb_predmet,mb_ucenik,nastavnik))
        self.conn.commit()

    def select_ocjena(self,predmetID,ucenikID):
        self.cur.execute("""SELECT * FROM Ocjena where predmetID=? and ucenikID=? ORDER BY datum """,(predmetID,ucenikID))
        ocjene= self.cur.fetchall()
        self.cur.execute("""SELECT AVG(ocjena) FROM Ocjena where predmetID=? and ucenikID=? ORDER BY datum """,
                         (predmetID, ucenikID))
        prosjek=self.cur.fetchall()
        if len(prosjek)!=0:
            return (ocjene,prosjek[0][0])
        return (ocjene,"")

    def delete_ocjena(self,mb):
        self.cur.execute("""
            DELETE FROM Ocjena
            WHERE mb= ?""", ( mb,))
        self.conn.commit()

    def ocjena_update(self,mb_ocjena,ocjena,datum,nastavnik):
        self.cur.execute("""UPDATE Ocjena SET
                            ocjena = ?, datum = ?, nastavnik = ? WHERE mb = ? """,(ocjena,datum,nastavnik,mb_ocjena))
        self.conn.commit()
















