# Teklif Listeleme Uygulaması

Bu uygulama, PDF teklif dosyalarını tarayıp içlerindeki önemli bilgileri (firma, konu, tutar) çıkararak bir veritabanında listeler.

## Özellikler

- PDF dosyalarından otomatik bilgi çıkarma (firma, konu, tutar)
- Tekil dosya ekleme veya klasör tarama (2 seviye derinliğe kadar)
- SQLite veritabanı ile veri saklama
- Tkinter ile basit ve kullanıcı dostu arayüz
- Özet tablo görünümü

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

Uygulamayı başlatın:
```bash
python main.py
```

### Arayüz Özellikleri

- **📄 PDF Dosyası Ekle**: Tek bir PDF dosyası seçip veritabanına ekler
- **📁 Klasör Tara**: Bir klasörü seçip içindeki tüm PDF'leri tarar (2 seviye alt klasöre kadar)
- **🔄 Tabloyu Yenile**: Veritabanındaki güncel verileri tabloya yükler
- **🗑️ Veritabanını Temizle**: Tüm kayıtları siler

### Çıkarılan Bilgiler

Uygulama, PDF dosyalarından şu bilgileri otomatik olarak çıkarmaya çalışır:
- **Firma**: Teklifin verildiği firma/müşteri adı
- **Konu**: Teklifin konusu/başlığı
- **Tutar**: Teklif tutarı (TL, USD, EUR formatlarında)

## Veritabanı

Veriler `teklif_veritabani.db` SQLite dosyasında saklanır. Aşağıdaki alanları içerir:
- ID
- Dosya Adı
- Firma
- Konu
- Tutar
- Tarih (eklenme tarihi)