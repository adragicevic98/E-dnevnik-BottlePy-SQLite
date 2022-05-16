import sqlite3


def pr(lista_id):
    for i in range(0, len(lista_id)):
        if (i + 1) not in lista_id:
            return i + 1
    return len(lista_id) + 1
class SQLUcenikModel():
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
              FOREIGN KEY (razredID) REFERENCES Razred (mb));""")


    def ucenik_select(self,mb=None):
        if mb is not None:
            mb=str(mb)
        if (mb is None):
            self.cur.execute("""SELECT u.mb, u.ime, u.prezime, r.razina, r.odjeljenje, u.username FROM Ucenik u INNER JOIN Razred r ON r.mb=u.RazredID ORDER BY PREZIME """)
        else:
            if (mb.isnumeric()):
                self.cur.execute("""SELECT u.mb, u.ime, u.prezime, r.razina, r.odjeljenje, u.username FROM Ucenik u INNER JOIN Razred r ON r.mb=u.RazredID WHERE u.mb=? ORDER BY PREZIME """,(mb,))
            else:
                self.cur.execute(
                    """SELECT u.mb, u.ime, u.prezime, r.razina, r.odjeljenje, u.username FROM Ucenik u INNER JOIN Razred r ON r.mb=u.RazredID WHERE u.prezime LIKE ? ORDER BY PREZIME """,('%' + mb + '%',))

        return  self.cur.fetchall()
    def ucenik_insert(self, ime, prezime,razred,slovo):
            self.cur.execute("""SELECT mb FROM Ucenik""")
            id=self.cur.fetchall()
            ime,prezime,razred,slovo=self.titlovanje_imena(ime,prezime,razred,slovo)
            id=[int(i[0]) for i in id]
            mb=self.provjeri_razmak(id)
            un=str(mb)+'u'
            r = SQLRazredModel(self.filename)
            razredID=r.get_razred_mb(razred,slovo)
            self.cur.execute("""
                INSERT INTO Ucenik
                (mb, ime, prezime, razredID, username)
                VALUES (?, ?, ?, ?, ?)""", (mb, ime, prezime,razredID,un))
            self.conn.commit()
            return  un

    def ucenik_delete(self, mb):
        red=self.ucenik_select(mb)
        self.cur.execute("""SELECT username From Ucenik WHERE mb=?""",(mb,))
        un=self.cur.fetchall()[0][0]
        self.cur.execute("""
            DELETE FROM Ucenik
            WHERE mb = ?""", (mb, ))
        self.conn.commit()
        return un
    def provjeri_razmak(self, lista_id):
        for i in range(0,len(lista_id)):
            if  (i+1)not in lista_id:
                return i+1
        return  len(lista_id)+1
    def titlovanje_imena(self, ime, prezime,razred,slovo):
         return (ime.title(),prezime.title(),int(razred),slovo.upper())
    def ucenik_edit(self,mb,ime,prezime,razred,odjeljenje):
        ime,prezime,razred,odjeljenje=self.titlovanje_imena(ime,prezime,razred,odjeljenje)
        r=SQLRazredModel(self.filename)
        ID=r.get_razred_mb(razred,odjeljenje)
        self.cur.execute("""UPDATE Ucenik SET
                            ime = ?, prezime = ?, razredID = ? WHERE mb = ? """,(ime,prezime,ID,mb))
        self.conn.commit()
class SQLRazredModel():
    def __init__(self, filename):
        self.conn = sqlite3.Connection(filename)
        self.cur = self.conn.cursor()
        self.filename=filename
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS Razred (
            mb integer PRIMARY KEY,
            razina int NOT NULL,
            odjeljenje text NOT NULL,
            razrednikID integer,
            FOREIGN KEY (razrednikID) REFERENCES Nastavnik (mb))""")

    def razred_select(self, mb=None, razina=None, odjeljenje=None, razrednikID=None):
        sql = "SELECT * FROM Razred  "
        sql_where, sql_and = False, False
        cond = []
        for field, op, val in [("mb", "=", mb), ("razina", "=", razina), ("odjeljenje", "=", odjeljenje), ('razrednikID', '=', razrednikID),]:
            if val is not None:
                if not sql_where:
                    sql_where = True
                    sql += "WHERE "
                if sql_and:
                    sql += "AND "
                sql += "{} {} ? ".format(field, op)
                sql_and = True
                cond.append(val)

        sql += "ORDER BY razina;"
        self.cur.execute(sql, tuple(cond))
        return self.cur.fetchall()
    def razred_bez_razrednika(self):
        self.cur.execute("""SELECT * FROM Razred WHERE razrednikID IS NULL ORDER BY razina""" )
        return  self.cur.fetchall()
    def razred_sa_razredniom(self):
        self.cur.execute("""SELECT r.mb, r.razina, r.odjeljenje, r.razrednikID, n.Prezime FROM Razred r  INNER JOIN  Nastavnik n ON r.razrednikID=n.mb WHERE r.razrednikID IS NOT NULL  ORDER BY razina""" )
        return  self.cur.fetchall()

    def razred_insert(self,razina,odjeljenje, razrednikID=None):
        self.cur.execute("""SELECT * FROM Razred  ORDER BY mb""")
        a=self.cur.fetchall()
        a=[i[0] for i in a]
        self.uc = SQLUcenikModel(self.filename)
        mb=self.uc.provjeri_razmak(a)
        self.cur.execute("""
            INSERT INTO Razred
            (mb, razina, odjeljenje, razrednikID)
            VALUES (?, ?, ?, ?)""", (mb,razina,odjeljenje,razrednikID))
        self.conn.commit()
    def get_razred_mb(self,razina,odjeljenje):
        self.cur.execute("""SELECT mb FROM Razred  WHERE razina = ? AND odjeljenje = ?""",(razina,odjeljenje))
        a=self.cur.fetchall()
        if len(a)!=0:
            return  a[0][0]
        else:
            self.razred_insert(razina=razina,odjeljenje=odjeljenje)
            return self.get_razred_mb(razina,odjeljenje)

    def razred_update_razrednik(self,mbr,razrednikID=None):
        if razrednikID is not None:
            self.cur.execute("""UPDATE Razred SET
                             razrednikID = ? WHERE mb = ? """, (razrednikID, mbr))
            self.conn.commit()
        else:
            self.cur.execute("""UPDATE Razred SET
                             razrednikID = NULL WHERE mb = ? """, (mbr, ))
            self.conn.commit()
        print(self.razred_select(mb=mbr))
class SQL_LoginModel():
    def __init__(self, filename):
        self.conn = sqlite3.Connection(filename)
        self.cur = self.conn.cursor()
        self.cur.executescript("""            
            CREATE TABLE IF NOT EXISTS Login(
            username text PRIMARY KEY NOT NULL,
            password text NOT NULL,
            FOREIGN KEY (username) REFERENCES Ucenik (username));""")

        self.cur.execute("""SELECT username FROM Login WHERE username= ?""",('1a',))
        a=self.cur.fetchall()
        if (len(a)==0):
            self.cur.execute("""
                INSERT INTO Login
                (username, password)
                VALUES (?,?)""", ('1a', '123'))
            self.conn.commit()

    def login_select(self):
        self.cur.execute("""SELECT * FROM Login""")
        a=self.cur.fetchall()


        rijecnik_a = {k: v for k, v in a if k[-1] == 'a'}
        rijecnik_n={k:v for k,v in a if k[-1]=='n'}
        rijecnik_u = {k: v for k, v in a if k[-1] == 'u'}
        return  (rijecnik_a,rijecnik_n,rijecnik_u)

    def login_chek(self,username,pasword,vrsta=0):
        rijecnik=self.login_select()[vrsta]
        if username in rijecnik:
            return rijecnik[username]==pasword
        else: return  False





    def login_delete(self, username):
        self.cur.execute("""
            DELETE FROM Login
            WHERE username = ?""", (username, ))
        self.conn.commit()




    def login_insert(self,un):
        self.cur.execute("""
            INSERT INTO Login
            (username, password)
            VALUES (?,?)""", (un, '123'))
        self.conn.commit()
class SQL_NastavnikModel():
    def __init__(self,filename):
        self.conn=sqlite3.Connection(filename)
        self.cur=self.conn.cursor()
        self.filename=filename
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS Nastavnik (
            mb integer PRIMARY KEY,
            ime text NOT NULL,
            prezime text NOT NULL,
            username text NOT NULL);""")

    def select_nastavnik(self,mb=None):
        if mb is not None:
            mb=str(mb)
        if mb is None:
            self.cur.execute("""SELECT * FROM Nastavnik""")
        elif (mb.isnumeric()):
            self.cur.execute("""SELECT * FROM Nastavnik WHERE mb=?""",(mb,))
        else: self.cur.execute("""SELECT * FROM Nastavnik WHERE prezime LIKE ? ORDER BY prezime""",('%'+mb+'%',))
        return  self.cur.fetchall()

    def insert_nastavnik(self,  ime, prezime):
        #vraca username password je svima 123
        self.cur.execute("""SELECT mb FROM Nastavnik""")
        id = self.cur.fetchall()
        ime, prezime = ime.title(),prezime.title()
        id = [int(i[0]) for i in id]
        mb = pr(id)
        un = str(mb) + 'n'
        self.cur.execute("""
            INSERT INTO Nastavnik
            (mb, ime, prezime, username)
            VALUES (?, ?, ?, ?)""", (mb, ime, prezime, un))
        self.conn.commit()
        return un


    def delete_nastavnik(self, mb):
        red=self.select_nastavnik(str(mb))
        self.cur.execute("""SELECT username From Nastavnik WHERE mb=?""",(mb,))
        un=self.cur.fetchall()[0][0]
        self.cur.execute("""
            DELETE FROM Nastavnik
            WHERE mb = ?""", (mb, ))
        self.conn.commit()
        return un

    def nastavnik_edit(self,mb,ime,prezime):
        ime,prezimee=ime.title(),prezime.title()
        self.cur.execute("""UPDATE Nastavnik SET
                            ime = ?, prezime = ? WHERE mb = ? """,(ime,prezime,mb))
        self.conn.commit()
    def jeRazrednik(self,mb):
        self.cur.execute("""SELECT mb FROM Razred WHERE razrednikID = ? """,(mb,))
        return len(self.cur.fetchall())==1
    def get_Razred_mb_od_Razrednik(self,mb):
        self.cur.execute("""SELECT mb FROM Razred WHERE razrednikID = ? """,(mb,))
        r=self.cur.fetchall()
        if(len(r)!=0):
            return r[0]
        else: return None
class SQL_PredmetModel():

    def __init__(self,filename):
        self.conn=sqlite3.Connection(filename)
        self.cur=self.conn.cursor()
        self.filename=filename
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS Predmet (
            mb integer PRIMARY KEY,
            naziv text NOT NULL,
            razina integer NOT NULL );""")

    def select_predmet(self,mb=None,naziv=None,razina=None):
        sql = "SELECT * FROM Predmet "
        sql_where, sql_and = False, False
        cond = []
        for field, op, val in [("mb","=",mb),("naziv", "=", naziv), ("razina", "=", razina)]:
            if val is not None:
                if not sql_where:
                    sql_where = True
                    sql += "WHERE "
                if sql_and:
                    sql += "AND "
                sql += "{} {} ? ".format(field, op)
                sql_and = True
                cond.append(val)
        sql+="ORDER BY naziv, razina"
        self.cur.execute(sql, tuple(cond))

        return self.cur.fetchall()

    def get_predmet_mb(self,naziv,razina):
        self.cur.execute("""SELECT mb FROM Predmet WHERE naziv= ? and razina = ?""",(naziv,razina))
        a=self.cur.fetchall()
        if len(a)==0:
            return  None
        else: return  a[0][0]

    def get_predmet_mb_do_cetri(self):
        self.cur.execute("""SELECT mb FROM Predmet WHERE razina<=4""")
        a=self.cur.fetchall()
        if len(a)==0:
            return  []
        else: return  [i[0] for i in a]

    def get_predmet_mb_od_cetri(self,predmet):
        self.cur.execute("""SELECT mb FROM Predmet WHERE razina>4 and naziv =?""",(predmet,))
        a=self.cur.fetchall()
        if len(a)==0:
            return  None
        else: return  [i[0] for i in a]


    def insert_predmet(self,naziv,razina):
        self.cur.execute("""SELECT mb FROM Predmet ORDER BY mb""")
        id=[i[0] for i in self.cur.fetchall()]
        mb=pr(id)
        self.cur.execute("""
            INSERT INTO Predmet
            (mb, naziv, razina)
            VALUES (?, ?, ?)""", (mb, naziv, razina))
        self.conn.commit()

    def predmetPostoji(self,naziv,razina):
        a=self.select_predmet(naziv=naziv,razina=razina)
        if len(a)==0:
            return False
        else: return True


    def delete_predmet(self,mb):
        self.cur.execute("""
            DELETE FROM Predmet
            WHERE mb = ?""", (mb, ))
        self.conn.commit()
    def edit_predmet(self,mb,naziv, razina):
        self.cur.execute("""UPDATE Predmet SET
                            naziv = ?, razina = ? WHERE mb = ? """, (naziv, razina, mb))
        self.conn.commit()
class SQL_Predmet_Nastavnik():
    def __init__(self,filename):
        self.conn=sqlite3.Connection(filename)
        self.cur=self.conn.cursor()
        self.filename=filename
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS Predmet_Nastavnik (
            mb integer PRIMARY KEY,
            predmetID integer NOT NULL,
            nastavnikID integer NOT NULL,
            FOREIGN KEY (predmetID) REFERENCES Predmet (mb),
            FOREIGN KEY (nastavnikID) REFERENCES Nastavnik (mb));""")
        #PRIMARY KEY (mb,predmetID,nastavnikID)
    def select_mb_Predmet_Nastavnik(self):
        self.cur.execute("""SELECT mb FROM Predmet_Nastavnik""")
        a=self.cur.fetchall()
        if (len(a)!=0):
            return [i[0] for i in a]
        else: return []
    def select2_mb_Predmet_Nastavnik(self,predmetRazina=None, nastavnikID=None):
        self.cur.execute("""SELECT pn.mb FROM Predmet_Nastavnik pn INNER JOIN  Predmet p ON p.mb=pn.predmetID WHERE p.razina=? and nastavnikID =?""",(predmetRazina,nastavnikID))
        a=self.cur.fetchall()
        if (len(a)!=0):
            return [i[0] for i in a]
        else: return []
    def insert_Predmet_Nastavnik(self,predmetID,nastavnikID):
        mb=pr(self.select_mb_Predmet_Nastavnik())
        self.cur.execute("""
            INSERT INTO Predmet_Nastavnik
            (mb, predmetID, nastavnikID)
            VALUES (?, ?, ?)""", (mb, predmetID,nastavnikID))
        self.conn.commit()
    def  delete_Predmet_Nastavnik(self,mb):
        self.cur.execute("""
            DELETE FROM Predmet_Nastavnik
            WHERE mb = ?""", (mb, ))
        self.conn.commit()
    def popis_ucitelja_Predmet_Nastavnik(self):
        self.cur.execute("""SELECT pn.mb, n.ime, n.prezime, p.razina, p.naziv, p.mb,n.mb FROM Predmet_Nastavnik pn INNER JOIN Nastavnik n ON n.mb=pn.nastavnikID INNER JOIN Predmet p on p.mb=pn.predmetID WHERE p.razina<5""")
        return self.cur.fetchall()
    def popis_profesora_Predmet_Nastavnik(self):
        self.cur.execute("""SELECT pn.mb, n.ime, n.prezime, p.razina, p.naziv, p.mb, n.mb FROM Predmet_Nastavnik pn INNER JOIN Nastavnik n ON n.mb=pn.nastavnikID INNER JOIN Predmet p on p.mb=pn.predmetID WHERE p.razina>5""")
        return self.cur.fetchall()
    def popis_sivh_profesora_za_Predmet_Nastavnik(self):
        self.cur.execute("""SELECT n.mb, n.ime, n.prezime, n.username FROM Nastavnik n""")
        return  self.cur.fetchall()
    def postojiPredmet_Nastavnik(self,PredmetID,NastavnikID):
        self.cur.execute("""Select mb FROM Predmet_Nastavnik WHERE  predmetID = ?  and nastavnikID = ?""",(PredmetID,NastavnikID))
        a=self.cur.fetchall()
        return len(a)!=0
    def select_Predmet_Nastavnik_mb_lista_predmeta(self, nastavnikID=None, lista_predmeta=[]):
        if lista_predmeta is None:
            lista_predmeta = []
        lista=[]
        for i in lista_predmeta:
            self.cur.execute("""SELECT mb FROM Predmet_Nastavnik WHERE predmetID= ? and nastavnikID = ?""", (i,nastavnikID))
            a=self.cur.fetchall()
            if len(a)!=0:
                lista.append(a[0])
        lista=[i[0] for i in lista]
        return lista
    def select_popis_nastave_moguce(self,razina):
        self.cur.execute(
            """SELECT pn.mb, p.naziv, p.razina, n.prezime,n.ime, n.mb  FROM Nastavnik n INNER JOIN Predmet p ON p.mb=pn.predmetID INNER JOIN Predmet_nastavnik pn ON pn.nastavnikID=n.mb WHERE p.razina= ? ORDER BY p.naziv """,(razina,))
        return  self.cur.fetchall()
class SQL_Razred_Pn():
    def __init__(self, filename):
        self.conn = sqlite3.Connection(filename)
        self.cur = self.conn.cursor()
        self.filename = filename
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS Razred_pn (
            razredID integer NOT NULL,
            pnID integer NOT NULL,
            PRIMARY KEY (razredID, pnID),
            FOREIGN KEY (razredID) REFERENCES Razred (mb),
            FOREIGN KEY (pnID) REFERENCES Predmet_nastavnik (mb));""")


    def delete_Razred_PredmetNastavnik(self,pnID,razredID=None):
        if razredID is not None:
            self.cur.execute("""
                DELETE FROM Razred_pn
                WHERE pnID = ? and razredID= ?""", (pnID,razredID))
            self.conn.commit()
        else:
            self.cur.execute("""
                DELETE FROM Razred_pn
                WHERE pnID = ? """, (pnID,))
            self.conn.commit()
    def select_Razred_PredmetNastavnik(self,pnID):
        lista=[]
        self.cur.execute("""SELECT * FROM Razredn_pn WHERE pnID= ? """,(pnID,))
    def insert_Razred_PredmetNastavnik(self,pnID,razredID):

        self.cur.execute("""
            INSERT INTO Razred_pn
            (pnID, razredID)
            VALUES (?, ?)""", (pnID, razredID))
        self.conn.commit()


    def delete_Razred_PredmetNastavnik2(self,razredID):
        self.cur.execute("""
            DELETE FROM Razred_pn
            WHERE razredID= ?""", ( razredID,))
        self.conn.commit()

    def select_popis_predmeta_po_razredu(self,razredID):
        self.cur.execute(
            """SELECT  n.mb, n.ime, n.prezime, p.naziv, p.razina,r.odjeljenje, r.mb, pnn.pnID FROM Razred_pn pnn INNER JOIN Predmet_nastavnik pn ON pnn.pnID=pn.mb INNER JOIN Predmet p ON pn.predmetID=p.mb INNER JOIN Razred r ON r.mb=pnn.razredID INNER JOIN Nastavnik n ON n.mb=pn.nastavnikID WHERE r.mb= ? ORDER BY p.naziv""",(razredID,))
        return self.cur.fetchall()

    def select_predmet_razred(self,razredID):
        self.cur.execute(
            """SELECT  * FROM  Razred_pn WHERE razredID= ?""",(razredID,))
        return self.cur.fetchall()

    def select_popis_unesene_nastave(self,razina):
        self.cur.execute(
            """SELECT  n.mb, n.ime, n.prezime, p.naziv, p.razina,r.odjeljenje, r.mb, pnn.pnID FROM Razred_pn pnn INNER JOIN Predmet_nastavnik pn ON pnn.pnID=pn.mb INNER JOIN Predmet p ON pn.predmetID=p.mb INNER JOIN Razred r ON r.mb=pnn.razredID INNER JOIN Nastavnik n ON n.mb=pn.nastavnikID WHERE p.razina= ?  ORDER BY p.naziv""",(razina,))
        return self.cur.fetchall()
class SQL_OcjenaModel():

    def __init__(self,filename):
        self.conn=sqlite3.Connection(filename)
        self.cur=self.conn.cursor()
        self.filename=filename
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

    def delete_ocjena(self,mb):
        self.cur.execute("""
            DELETE FROM Ocjena
            WHERE ucenikID= ?""", ( mb,))
        self.conn.commit()















































































