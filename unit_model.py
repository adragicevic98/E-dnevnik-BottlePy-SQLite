import unittest
import adminControl
import bottle
import os
import sys
from NastavnikModel import NastavnikModel


if __name__ == "__main__":

    sys.path.append(os.path.abspath("../"))

import adminModel

class TestUcenikModel(unittest.TestCase):

    def setUp(self):
        self.dr=adminModel.SQLRazredModel("unit_baza2.db")
        self.db = adminModel.SQLUcenikModel("unit_baza2.db")
     
    def tearDown(self):
       del(self.db)
       del(self.dr)
       os.remove("unit_baza2.db")

      
    def test_ucenik_select_empty(self):
        self.assertCountEqual(self.db.ucenik_select(), [])
      
    def test_ucenik_select_two_records(self):
        self.db.ucenik_insert("Ante", "Antić",2,"a")
        self.db.ucenik_insert("Iva", "Ivić",3,"b")
        self.assertCountEqual(self.db.ucenik_select(), [(1, 'Ante', 'Antić', 2, 'A', '1u'), (2, 'Iva', 'Ivić', 3, 'B', '2u')])
       
    def test_ucenik_select_two_records_reversed(self):
        self.db.ucenik_insert("Ante", "Antić",2,"a")
        self.db.ucenik_insert("Iva", "Ivić","3","b")
        self.assertCountEqual(self.db.ucenik_select(), [(1, 'Ante', 'Antić', 2, 'A', '1u'), (2, 'Iva', 'Ivić', 3, 'B', '2u')])
    
    def test_ucenik_by_mb_int(self):
        self.db.ucenik_insert("Ante", "Antić",2,"a")
        self.db.ucenik_insert("Iva", "Ivić","3","b")
        self.assertCountEqual(self.db.ucenik_select(mb=1), [(1, 'Ante', 'Antić', 2, 'A', '1u')])
     
    def test_ucenik_by_mb_str(self):
        self.db.ucenik_insert("Ante", "Antić",2,"a")
        self.db.ucenik_insert("Iva", "Ivić","3","b")
        self.assertCountEqual(self.db.ucenik_select(mb="2"), [(2, 'Iva', 'Ivić', 3, 'B', '2u')])
    
    def test_ucenik_2_inserts_1_update(self):
        self.db.ucenik_insert("Ante", "Antić",2,"a")
        self.db.ucenik_insert("Iva", "Ivić","3","b")
        self.db.ucenik_edit(2,"Ivana", "Ivanić",3,"b")
        self.assertCountEqual(self.db.ucenik_select(), [(1, 'Ante', 'Antić', 2, 'A', '1u'), (2, 'Ivana', 'Ivanić', 3, 'B', '2u')])
        
    def test_ucenik_2_inserts_1_delete(self):
        self.db.ucenik_insert("Ante", "Antić",2,"a")
        self.db.ucenik_insert("Iva", "Ivić","3","b")
        self.db.ucenik_delete(1)
        self.assertCountEqual(self.db.ucenik_select(), [(2, 'Iva', 'Ivić', 3, 'B', '2u')])


    
    


class TestRazredModel(unittest.TestCase):

    def setUp(self):
        self.dn=adminModel.SQL_NastavnikModel("unit_baza2.db")
        self.db = adminModel.SQLRazredModel("unit_baza2.db")
    def tearDown(self):
        del(self.db)
        del(self.dn)
        os.remove("unit_baza2.db")
    def test_razred_select_empty(self):
        self.assertCountEqual(self.db.razred_select(), [])

    def test_razred_select_two_records(self):
        self.db.razred_insert(2, "A",1)
        self.db.razred_insert("4", "B")
        self.assertCountEqual(self.db.razred_select(), [(1, 2, 'A',1), (2, 4, 'B',None)])

    def test_razred_select_two_records_reversed(self):
        self.db.razred_insert("2", "A",1)
        self.db.razred_insert(4, "B")
        self.assertCountEqual(self.db.razred_select(), [(1, 2, 'A',1), (2, 4, 'B',None)])

    def test_razred_by_mb_int(self):
        self.db.razred_insert("2", "A",1)
        self.db.razred_insert(4, "B",2)
        self.assertCountEqual(self.db.razred_select(mb=1), [(1, 2, 'A',1)])
    def test_razred_by_mb_str(self):
        self.db.razred_insert("2", "A",1)
        self.db.razred_insert(4, "B",2)
        self.assertCountEqual(self.db.razred_select(mb="2"), [(2, 4, 'B',2)])

    def test_razred_2_inserts_1_update(self):
        self.db.razred_insert("2", "A")
        self.db.razred_insert(4, "B")
        self.dn.insert_nastavnik('Ivan','Matic')
        self.db.razred_update_razrednik(2,1)
        self.assertCountEqual(self.db.razred_select(), [(1, 2, 'A',None), (2, 4, 'B',1)])
        self.assertCountEqual(self.db.razred_bez_razrednika(), [(1, 2, 'A',None)])
        self.assertCountEqual(self.db.razred_sa_razredniom(), [(2, 4, 'B',1,'Matic')])
    
        
    
class TestLoginModel(unittest.TestCase):

    def setUp(self):
        self.db = adminModel.SQL_LoginModel("unit_baza2.db")
    def tearDown(self):
        del(self.db)
        os.remove("unit_baza2.db")

    def test_login_select_empty_almost(self):
        self.assertCountEqual(self.db.login_select(), ({'1a':'123'},{},{}))

    def test_login_select_two_records(self):
        self.db.login_insert("2u")
        self.db.login_insert("3a")
        self.assertCountEqual(self.db.login_select(), ({'1a':'123','3a':'123'},{},{'2u':'123'}))

    def test_login_2_inserts_1_delete(self):
        self.db.login_delete('2u')
        self.assertCountEqual(self.db.login_select(), ({'1a':'123'},{},{}))
        
    def test_login_chek(self):
        self.assertTrue(self.db.login_chek('1a','123'))
        self.assertFalse(self.db.login_chek('2u', '123'))
        
      
class TestNastavnikModel(unittest.TestCase):
    def setUp(self):
        self.db = adminModel.SQL_NastavnikModel("unit_baza2.db")
    def tearDown(self):
        del(self.db)
        os.remove("unit_baza2.db")
    def test_nastavnik_select_empty(self):
        self.assertCountEqual(self.db.select_nastavnik(), [])

    def test_nastvanik_select_two_records(self):
        self.db.insert_nastavnik("Ante", "Antić")
        self.db.insert_nastavnik("Mate", "Matić")
        self.assertCountEqual(self.db.select_nastavnik(), [(1, 'Ante','Antić','1n'), (2, 'Mate', 'Matić','2n')])

    def test_nastavnik_by_mb_int(self):
        self.db.insert_nastavnik("Ante", "Antić")
        self.db.insert_nastavnik("Mate", "Matić")
        self.assertCountEqual(self.db.select_nastavnik(mb=1), [(1, 'Ante','Antić','1n')])
   
    def test_nastavnik_by_mb_str(self):
        self.db.insert_nastavnik("Ante", "Antić")
        self.db.insert_nastavnik("Mate", "Matić")
        self.assertCountEqual(self.db.select_nastavnik(mb="1"), [(1, 'Ante','Antić','1n')])

    def test_nastavnik_2_inserts_1_update(self):
        self.db.insert_nastavnik("Ante", "Antić")
        self.db.insert_nastavnik("Mate", "Matić")
        self.db.nastavnik_edit(1,"Ivo","Ivić")
        self.assertCountEqual(self.db.select_nastavnik(), [(1, 'Ivo','Ivić','1n'), (2, 'Mate', 'Matić','2n')])

    def test_nastavnik_2_inserts_1_delete(self):
        self.db.insert_nastavnik("Ante", "Antić")
        self.db.insert_nastavnik("Mate", "Matić")
        self.db.delete_nastavnik(1)
        self.assertCountEqual(self.db.select_nastavnik(), [(2, 'Mate', 'Matić','2n')])
        
    def test_ucenik_validacija(self):
        self.assertEqual(adminControl.ucenik_validiraj('Ivo','Ivic',2, 'A'),True)
        self.assertEqual(adminControl.ucenik_validiraj("Ivo","Matic","3","b"),True)
        self.assertEqual(adminControl.ucenik_validiraj("","","",""),False)
        self.assertEqual(adminControl.ucenik_validiraj("Ana","Anić","3",""),False)
        self.assertEqual(adminControl.ucenik_validiraj("Ivo","Markić","3",""),False)
        self.assertEqual(adminControl.ucenik_validiraj("","Matic","3","b"),False)
        self.assertEqual(adminControl.ucenik_validiraj("Ivo","","3","b"),False)
        self.assertEqual(adminControl.ucenik_validiraj("Ivo","Matic","9","b"),False)
        self.assertEqual(adminControl.ucenik_validiraj("Ivo","Matic","3","D"),False)
        self.assertEqual(adminControl.ucenik_validiraj("I","Matic","3","A"),False)
        self.assertEqual(adminControl.ucenik_validiraj("Ivo","M","3","A"),False)
        
    def test_nastavnik_validacija(self):
        self.assertEqual(adminControl.nastavnik_validiraj("Ivan","Ivanić"),True)
        self.assertEqual(adminControl.nastavnik_validiraj("Ivan",""),False)
        self.assertEqual(adminControl.nastavnik_validiraj("","Ivanić"),False)
        self.assertEqual(adminControl.nastavnik_validiraj("",""),False)
        self.assertEqual(adminControl.nastavnik_validiraj("2","Ivanić"),False)
        self.assertEqual(adminControl.nastavnik_validiraj("Ivan","5"),False)
        self.assertEqual(adminControl.nastavnik_validiraj("I","Ivanić"),False)
        self.assertEqual(adminControl.nastavnik_validiraj("Iv","Ivanić"),True)
        self.assertEqual(adminControl.nastavnik_validiraj("@","Ivanić"),False)
        

class TestPredmetkModel(unittest.TestCase):
    def setUp(self):
        self.db = adminModel.SQL_PredmetModel("unit_baza2.db")
        self.do = adminModel.SQL_OcjenaModel("unit_baza2.db")
        self.dn = NastavnikModel("unit_baza2.db")
        self.du = adminModel.SQLUcenikModel("unit_baza2.db")
    def tearDown(self):
        del(self.db)
        del(self.do)
        del(self.dn)
        del(self.du)
        os.remove("unit_baza2.db")
    def test_predmet_select_empty(self):
        self.assertCountEqual(self.db.select_predmet(), [])
    def test_predmet_select_two_records(self):
        self.db.insert_predmet("hrvatski",1)
        self.db.insert_predmet("matematika", "2")
        self.assertCountEqual(self.db.select_predmet(), [(1,'hrvatski',1), (2,'matematika', 2)])
    def test_predmet_postoji(self):
        self.db.insert_predmet("hrvatski",1)
        self.db.insert_predmet("matematika", "2")
        self.assertEqual(self.db.predmetPostoji("hrvatski",1),True)
    def test_ocjena_2_inserts_1_delete(self):
        self.du.ucenik_insert("Ante", "Antić",2,"a")
        self.du.ucenik_insert("Iva", "Ivić",3,"b")
        self.dn.insert_ocjena(2,1,1,'1.1.2020','Jure Matic')
        self.dn.insert_ocjena(3,2,2,'2.2.2020.','Jure Matic')
        self.dn.delete_ocjena(2)
        self.assertCountEqual(self.dn.select_ocjena(1,1),([(1, 2, '1.1.2020', 1, 1, 'Jure Matic')], 2.0) )

   
        

if __name__ == "__main__":
    unittest.main()

