import os

class FolderScanner:
    def __init__(self):
        self.pdf_files = []
    
    def klasor_tara(self, klasor_yolu, max_derinlik=2):
        """
        Belirtilen klasörü tarar ve PDF dosyalarını bulur
        max_derinlik: Kaç seviye alt klasöre inileceği (varsayılan 2)
        """
        self.pdf_files = []
        self._recursive_scan(klasor_yolu, 0, max_derinlik)
        return self.pdf_files
    
    def _recursive_scan(self, klasor_yolu, current_derinlik, max_derinlik):
        """Özyinelemeli olarak klasörleri tarar"""
        if not os.path.exists(klasor_yolu):
            return
        
        if current_derinlik > max_derinlik:
            return
        
        try:
            for item in os.listdir(klasor_yolu):
                item_path = os.path.join(klasor_yolu, item)
                
                if os.path.isfile(item_path):
                    if item.lower().endswith('.pdf'):
                        self.pdf_files.append(item_path)
                elif os.path.isdir(item_path):
                    self._recursive_scan(item_path, current_derinlik + 1, max_derinlik)
        except PermissionError:
            print(f"Erişim izni yok: {klasor_yolu}")
        except Exception as e:
            print(f"Klasör tarama hatası: {str(e)}")
