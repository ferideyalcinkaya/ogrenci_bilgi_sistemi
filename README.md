# ogrenci_bilgi_sistemi
🎓 BTÜ Öğrenci Bilgi Sistemi (OBS) Not Hesaplama Projesi
Bu proje, Bursa Teknik Üniversitesi Ölçme ve Değerlendirme Esasları Yönergesi hükümlerini dijital ortama aktaran, tam işlevli bir web uygulamasıdır. 
Sistem, öğretim üyelerinin Excel üzerinden toplu not girişi yapmasına ve öğrencilerin kişiselleştirilmiş sonuçlarını görüntülemesine olanak tanır.

📑 Mevzuat Uyumluluğu (Algoritmik Altyapı)
Sistem, yönetmelikteki karmaşık hesaplama yöntemlerini otomatik olarak uygular:

HBP Hesaplama (Madde 5): Ara sınavın %40'ı ile final/bütünleme sınavının %60'ı toplanır; sonuçlar 0.50 kuralına göre en yakın tam sayıya yuvarlanır.

Baraj Puanları (Madde 7/3-4): Ham Başarı Puanı (HBP) veya sınav notu (Final/Büt) 35'in altında olan öğrenciler doğrudan FF notu ile değerlendirilir.

Değerlendirme Sistemleri (Madde 7/1):

MNS (Mutlak): Öğrenci sayısı 20'nin altında olan gruplarda uygulanır.

BDS (Bağıl): 20 ve üzeri mevcuda sahip sınıflarda T-Skoru ve çan eğrisi analizi ile harf notu belirlenir.

Bütünleme Esasları (Madde 9/4): Bütünleme sınavı finalin yerini alır; bütünleme grubu kendi istatistiksel dağılımı içinde değerlendirilir.

💻 Kullanılan Teknolojiler
Backend: Python 3, Flask (RESTful API)

Frontend: React.js, Tailwind CSS (Modern & Duyarlı UI)

Veri Yönetimi: SQLite (Veri Kalıcılığı) ve Pandas (Excel Veri İşleme)

🚀 Öne Çıkan Fonksiyonlar
Excel Entegrasyonu: .xlsx dosyalarından toplu öğrenci verisi ve not aktarımı.

Sınıf İzolasyonu: Sınıf A ve Sınıf B verilerinin istatistiksel olarak birbirini etkilememesi için tasarlanmış bağımsız hesaplama modülleri.

Rol Tabanlı Erişim: Hoca ve öğrenci için özelleştirilmiş giriş ve işlem panelleri.


🛠️ Kurulum
Bağımlılıkları Yükle:pip install flask flask-cors pandas openpyxl numpy
npm install


Sistemi Başlat:

Backend: python app.py

Frontend: npm start

👥 Giriş Bilgileri:
Rol       E-posta            Şifre
Hoca,    ali.hoca@btu.edu.tr,Btu55095!
Öğrenci, ahmet.ogr@btu.edu.tr,Btu11225!
