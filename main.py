import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from database import Database
from pdf_extractor import PDFExtractor
from folder_scanner import FolderScanner

class TeklifListelemeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teklif Listeleme Uygulaması")
        self.root.geometry("1000x600")
        
        # Modüller
        self.db = Database()
        self.pdf_extractor = PDFExtractor()
        self.folder_scanner = FolderScanner()
        
        self.setup_ui()
        self.tabloyu_guncelle()
    
    def setup_ui(self):
        """Kullanıcı arayüzünü oluşturur"""
        # Üst panel - Butonlar
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        
        tk.Button(top_frame, text="📄 PDF Dosyası Ekle", 
                 command=self.dosya_ekle, width=20, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(top_frame, text="📁 Klasör Tara", 
                 command=self.klasor_tara, width=20, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(top_frame, text="🔄 Tabloyu Yenile", 
                 command=self.tabloyu_guncelle, width=20, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(top_frame, text="🗑️ Veritabanını Temizle", 
                 command=self.veritabanini_temizle, width=20, height=2).pack(side=tk.LEFT, padx=5)
        
        # Bilgi etiketi
        self.info_label = tk.Label(self.root, text="", fg="blue", font=("Arial", 10))
        self.info_label.pack(pady=5)
        
        # Tablo
        table_frame = tk.Frame(self.root, padx=10, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        columns = ("ID", "Dosya Adı", "Firma", "Konu", "Tutar", "Tarih")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                 yscrollcommand=scrollbar_y.set,
                                 xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Kolon başlıkları
        self.tree.heading("ID", text="ID")
        self.tree.heading("Dosya Adı", text="Dosya Adı")
        self.tree.heading("Firma", text="Firma")
        self.tree.heading("Konu", text="Konu")
        self.tree.heading("Tutar", text="Tutar")
        self.tree.heading("Tarih", text="Tarih")
        
        # Kolon genişlikleri
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Dosya Adı", width=200)
        self.tree.column("Firma", width=200)
        self.tree.column("Konu", width=250)
        self.tree.column("Tutar", width=100, anchor=tk.RIGHT)
        self.tree.column("Tarih", width=150, anchor=tk.CENTER)
        
        # Grid yerleşimi
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Durum çubuğu
        self.status_label = tk.Label(self.root, text="Hazır", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def dosya_ekle(self):
        """Tek bir PDF dosyası ekler"""
        dosya_yolu = filedialog.askopenfilename(
            title="PDF Dosyası Seçin",
            filetypes=[("PDF Dosyaları", "*.pdf"), ("Tüm Dosyalar", "*.*")]
        )
        
        if dosya_yolu:
            self.status_label.config(text=f"İşleniyor: {os.path.basename(dosya_yolu)}")
            self.root.update()
            
            dosya_adi = os.path.basename(dosya_yolu)
            
            # Daha önce eklendi mi kontrol et
            if self.db.teklif_varmi(dosya_adi):
                self.info_label.config(text=f"⚠️ Bu dosya zaten veritabanında: {dosya_adi}", fg="orange")
                self.status_label.config(text="Hazır")
                return
            
            # PDF'den bilgi çıkart
            firma, konu, tutar = self.pdf_extractor.pdf_bilgisi_cikart(dosya_yolu)
            
            # Veritabanına ekle
            self.db.teklif_ekle(dosya_adi, firma, konu, tutar)
            
            self.info_label.config(text=f"✓ Dosya eklendi: {dosya_adi}", fg="green")
            self.status_label.config(text="Hazır")
            self.tabloyu_guncelle()
    
    def klasor_tara(self):
        """Klasör seçer ve tarar"""
        klasor_yolu = filedialog.askdirectory(title="Taranacak Klasörü Seçin")
        
        if klasor_yolu:
            self.status_label.config(text="Klasör taranıyor...")
            self.root.update()
            
            # Klasörü tara
            pdf_dosyalari = self.folder_scanner.klasor_tara(klasor_yolu, max_derinlik=2)
            
            if not pdf_dosyalari:
                self.info_label.config(text="⚠️ Klasörde PDF dosyası bulunamadı", fg="orange")
                self.status_label.config(text="Hazır")
                return
            
            # Her PDF'i işle
            eklenen = 0
            atlanan = 0
            
            for pdf_path in pdf_dosyalari:
                dosya_adi = os.path.basename(pdf_path)
                
                self.status_label.config(text=f"İşleniyor: {dosya_adi} ({eklenen + atlanan + 1}/{len(pdf_dosyalari)})")
                self.root.update()
                
                # Daha önce eklendi mi kontrol et
                if self.db.teklif_varmi(dosya_adi):
                    atlanan += 1
                    continue
                
                # PDF'den bilgi çıkart
                firma, konu, tutar = self.pdf_extractor.pdf_bilgisi_cikart(pdf_path)
                
                # Veritabanına ekle
                self.db.teklif_ekle(dosya_adi, firma, konu, tutar)
                eklenen += 1
            
            self.info_label.config(text=f"✓ {eklenen} dosya eklendi, {atlanan} dosya atlandı (zaten mevcut)", fg="green")
            self.status_label.config(text="Hazır")
            self.tabloyu_guncelle()
    
    def tabloyu_guncelle(self):
        """Tabloyu veritabanından günceller"""
        # Mevcut verileri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Yeni verileri ekle
        teklifler = self.db.tum_teklifleri_getir()
        for teklif in teklifler:
            self.tree.insert("", tk.END, values=teklif)
        
        self.status_label.config(text=f"Toplam {len(teklifler)} teklif listeleniyor")
    
    def veritabanini_temizle(self):
        """Veritabanındaki tüm kayıtları siler"""
        cevap = messagebox.askyesno("Onay", "Tüm kayıtlar silinecek. Emin misiniz?")
        if cevap:
            self.db.veritabanini_temizle()
            self.tabloyu_guncelle()
            self.info_label.config(text="✓ Veritabanı temizlendi", fg="green")

def main():
    root = tk.Tk()
    app = TeklifListelemeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
