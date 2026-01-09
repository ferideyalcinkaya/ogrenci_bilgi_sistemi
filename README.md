# ogrenci_bilgi_sistemi
🎓 BTÜ OBS Not Hesaplama & Yönetim Sistemi

Bu proje, Bursa Teknik Üniversitesi Ölçme ve Değerlendirme Esasları Yönergesi hükümlerine yüksek oranda uyumlu olarak geliştirilmiş, web tabanlı bir Not Yönetim Sistemi simülasyonudur.
Sistem; hoca ve öğrenci rollerini ayırarak, Excel'den toplu veri girişi ve otomatik harf notu hesaplama işlemlerini gerçekleştirmektedir.

🚀 Öne Çıkan Özellikler

Yönetmelik Uyumlu Hesaplama: 

Madde 5: Ara sınavın %40, final/bütünleme sınavının %60 etkisi ve 0.50 yuvarlama kuralı.


Madde 7(1): Öğrenci sayısı 20 altındaki sınıflarda Mutlak Not Sistemi (MNS), 20 ve üzerindeki sınıflarda Bağıl Değerlendirme Sistemi (BDS/Çan).


Madde 7(3-4): Ham Başarı Puanı (HBP) veya Final/Büt notu 35 altında olan öğrenciler için doğrudan FF barajı.


Madde 7(5): BDKL (20 puan) altı öğrencilerin bağıl değerlendirme istatistiklerine dahil edilmemesi.


Madde 9(4): Bütünleme sınavına girenlerin final notunun iptal edilip, büt notuyla ayrı bir grupta değerlendirilmesi.

Toplu Veri Girişi: 
Excel (.xlsx) dosyalarından öğrenci listesi ve notların otomatik içeri aktarılması.

Dinamik Arayüz: Not değişikliklerinde tüm sınıfın harf notlarının (BDS dahil) anında yeniden hesaplanması.

Rol Tabanlı Erişim: Hoca için tam yönetim paneli, öğrenci için kişisel not görüntüleme ekranı.
🛠️ Kurulum ve Çalıştırma1. Backend (Python/Flask)Bash# Gerekli kütüphaneleri kurun
pip install flask flask-cors pandas openpyxl numpy

# Uygulamayı başlatın
python app.py
2. Frontend (React) 

# Bağımlılıkları yükleyin
npm install

# Uygulamayı başlatın
npm start
🔑 Test Giriş BilgileriRol
E-posta Şifre Hoca için: ali.hoca@btu.edu.tr Btu55095!  
E-posta Şifre Öğrenci için:ahmet.ogr@btu.edu.tr  Btu11225!
Excel Dosya Yapısı Excel üzerinden toplu not yüklemek için dosyanızın ilk satırı şu başlıklardan oluşmalıdır:
Öğrenci No, Ad Soyad, Vize, Final, Büt
📝 Lisans:
Bu proje eğitim amaçlı geliştirilmiştir ve MIT Lisansı ile korunmaktadır.
