import numpy as np

class BTUNotSistemi:
    def __init__(self):
        # Yönerge Madde 5(2): Final katkısı %40-%60 arası olmalıdır.
        self.YSNKY = 0.60  # Final %60
        self.YINKY = 0.40  # Vize %40

    def hbp_hesapla(self, vize, final):
        """Madde 5(3): 0.50 ve üzeri yukarı yuvarlanır."""
        hbp_ham = (vize * self.YINKY) + (final * self.YSNKY)
        return int(hbp_ham + 0.5)

    def mutlak_harf_notu(self, hbp, final):
        """Madde 7(3,4) Barajlar ve Tablo 2 Mutlak Sistem."""
        if final < 35 or hbp < 35:
            return "FF"
        
        # Tablo 2: Ham Başarı Puanı Karşılıkları
        if hbp >= 90: return "AA"
        elif hbp >= 80: return "BA"
        elif hbp >= 75: return "BB"
        elif hbp >= 70: return "CB"
        elif hbp >= 65: return "CC"
        elif hbp >= 60: return "DC"
        elif hbp >= 55: return "DD"
        elif hbp >= 35: return "FD"
        return "FF"

    def bagil_harf_notu(self, hbp, final, sinif_hbpler):
        """Madde 7: Bağıl Değerlendirme (T-Skoru) Sistemi."""
        # Madde 7(3,4): Alt limit kontrolleri
        if final < 35 or hbp < 35:
            return "FF"

        # Madde 7(2,5): BDKL (Bağıl Değerlendirmeye Katılma Limiti) 20 puandır.
        gecerli_hbpler = [x for x in sinif_hbpler if x >= 20]
        
        ort = np.mean(gecerli_hbpler)
        std = np.std(gecerli_hbpler)
        
        # Madde 7(6-a): T-Skoru Formülü
        t_skoru = ((hbp - ort) / (std if std > 0 else 1)) * 10 + 60

        # Tablo 3: Sınıf Düzeyi ve T-Skoru Sınırları
        # Örnek: Orta Düzey Sınıf (47.5 < Ort <= 52.5) için sınırlar
        if ort > 80:   sinirlar = [32, 37, 42, 47, 52, 57, 62, 67]
        elif ort > 70: sinirlar = [34, 39, 44, 49, 54, 59, 64, 69]
        elif ort > 62.5: sinirlar = [36, 41, 46, 51, 56, 61, 66, 71]
        elif ort > 57.5: sinirlar = [38, 43, 48, 53, 58, 63, 68, 73]
        elif ort > 52.5: sinirlar = [40, 45, 50, 55, 60, 65, 70, 75]
        elif ort > 47.5: sinirlar = [42, 47, 52, 57, 62, 67, 72, 77]
        elif ort > 42.5: sinirlar = [44, 49, 54, 59, 64, 69, 74, 79]
        else:            sinirlar = [46, 51, 56, 61, 66, 71, 76, 81]

        harfler = ["FF", "FD", "DD", "DC", "CC", "CB", "BB", "BA", "AA"]
        for i, sinir in enumerate(sinirlar):
            if t_skoru < sinir:
                return harfler[i]
        return "AA"

    def sinif_degerlendir(self, ogrenci_listesi):
        """Madde 7(1): 20 öğrenci sınırı kontrolü."""
        hbpler = [self.hbp_hesapla(o['vize'], o['final']) for o in ogrenci_listesi]
        mevcut = len(ogrenci_listesi)
        
        sonuclar = []
        for i, o in enumerate(ogrenci_listesi):
            hbp = hbpler[i]
            if mevcut < 20:
                harf = self.mutlak_harf_notu(hbp, o['final'])
                sistem = "Mutlak (MNS)"
            else:
                harf = self.bagil_harf_notu(hbp, o['final'], hbpler)
                sistem = "Bağıl (BDS)"
            
            sonuclar.append({
                "no": o['no'],
                "hbp": hbp,
                "harf": harf,
                "sistem": sistem
            })
        return sonuclar

# --- TEST VERİSİ ---
obs = BTUNotSistemi()

# Sınıf A: 15 Kişi (Mutlak Sistem Uygulanır)
sinif_a = [{"no": i, "vize": 60, "final": 70} for i in range(1, 16)]

# Sınıf B: 25 Kişi (Bağıl Sistem Uygulanır)
sinif_b = [{"no": i, "vize": np.random.randint(30,90), "final": np.random.randint(30,90)} for i in range(1, 26)]

print("SINIF A (15 Öğrenci) Örneği:")
print(obs.sinif_degerlendir(sinif_a)[0])

print("\nSINIF B (25 Öğrenci) Örneği:")
print(obs.sinif_degerlendir(sinif_b)[0])