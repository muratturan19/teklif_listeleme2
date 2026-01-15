import pdfplumber
import re
import os

class PDFExtractor:
    def __init__(self):
        pass
    
    def pdf_bilgisi_cikart(self, pdf_path):
        """
        PDF dosyasından firma, konu ve tutar bilgilerini çıkarır
        Returns: (firma, konu, tutar) tuple
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                # İlk birkaç sayfayı oku (genellikle bilgiler başta olur)
                for page in pdf.pages[:3]:
                    text += page.extract_text() + "\n"
                
                firma = self._firma_bul(text)
                konu = self._konu_bul(text)
                tutar = self._tutar_bul(text)
                
                return firma, konu, tutar
        except Exception as e:
            print(f"PDF okuma hatası ({pdf_path}): {str(e)}")
            return None, None, None
    
    def _firma_bul(self, text):
        """Firma adını bulmaya çalışır"""
        # Yaygın firma patternleri
        patterns = [
            r'(?:Firma|FİRMA|Müşteri|MÜŞTERİ|Sayın|SAYIN|Sirket|ŞİRKET|Company)\s*[:：]?\s*([A-ZÇĞİÖŞÜa-zçğıöşü\s\.&\-]+?)(?:\n|$|Tel|Mail|Adres)',
            r'(?:TO|To|to)\s*[:：]?\s*([A-ZÇĞİÖŞÜa-zçğıöşü\s\.&\-]+?)(?:\n|$)',
            r'([A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜa-zçğıöşü\s\.&\-]*(?:Ltd|LTD|A\.?Ş\.?|AS|Inc|INC|Corp|CORP)\.?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                firma = match.group(1).strip()
                if len(firma) > 3:  # En az 3 karakter
                    return firma
        
        return "Belirtilmemiş"
    
    def _konu_bul(self, text):
        """Teklif konusunu bulmaya çalışır"""
        patterns = [
            r'(?:Konu|KONU|Subject|SUBJECT|Proje|PROJE|İş|İŞ)\s*[:：]?\s*([^\n]{10,200})',
            r'(?:Teklif|TEKLİF|Proposal|PROPOSAL)\s+(?:Konusu|KONUSU|Subject|SUBJECT)?\s*[:：]?\s*([^\n]{10,200})',
            r'(?:RE|Re|re)\s*[:：]?\s*([^\n]{10,200})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                konu = match.group(1).strip()
                if len(konu) > 5:
                    return konu
        
        return "Belirtilmemiş"
    
    def _tutar_bul(self, text):
        """Teklif tutarını bulmaya çalışır"""
        patterns = [
            r'(?:Toplam|TOPLAM|Total|TOTAL|Genel Toplam|GENEL TOPLAM|Grand Total)\s*[:：]?\s*([0-9.,]+\s*(?:TL|₺|USD|EUR|$|€))',
            r'(?:Tutar|TUTAR|Amount|AMOUNT|Fiyat|FİYAT|Price|PRICE)\s*[:：]?\s*([0-9.,]+\s*(?:TL|₺|USD|EUR|$|€))',
            r'([0-9]{1,3}(?:[.,][0-9]{3})*(?:[.,][0-9]{2})?\s*(?:TL|₺))',
        ]
        
        tutarlar = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                tutar = match.group(1).strip()
                tutarlar.append(tutar)
        
        if tutarlar:
            # En büyük tutarı döndür (genellikle toplam tutar en büyüktür)
            return max(tutarlar, key=lambda x: self._tutar_sayiya_cevir(x))
        
        return "Belirtilmemiş"
    
    def _tutar_sayiya_cevir(self, tutar_str):
        """Tutar string'ini sayıya çevirir (karşılaştırma için)"""
        try:
            # Sadece rakamları ve noktayı al
            sayi_str = re.sub(r'[^\d.,]', '', tutar_str)
            sayi_str = sayi_str.replace(',', '')
            return float(sayi_str)
        except:
            return 0
