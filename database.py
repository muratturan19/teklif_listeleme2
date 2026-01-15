import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path='teklif_veritabani.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Veritabanını başlatır ve tabloyu oluşturur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teklifler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dosya_adi TEXT NOT NULL,
                firma TEXT,
                konu TEXT,
                tutar TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def teklif_ekle(self, dosya_adi, firma, konu, tutar):
        """Veritabanına yeni teklif ekler"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO teklifler (dosya_adi, firma, konu, tutar)
            VALUES (?, ?, ?, ?)
        ''', (dosya_adi, firma, konu, tutar))
        conn.commit()
        conn.close()
    
    def tum_teklifleri_getir(self):
        """Tüm teklifleri getirir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, dosya_adi, firma, konu, tutar, tarih FROM teklifler ORDER BY tarih DESC')
        teklifler = cursor.fetchall()
        conn.close()
        return teklifler
    
    def teklif_varmi(self, dosya_adi):
        """Bu dosya daha önce eklenmiş mi kontrol eder"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM teklifler WHERE dosya_adi = ?', (dosya_adi,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    def veritabanini_temizle(self):
        """Tüm kayıtları siler"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM teklifler')
        conn.commit()
        conn.close()
