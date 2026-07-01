🌐 English Description
This is a Computer Vision application built with Python, OpenCV, and MediaPipe. It allows users to control and switch between real-time camera filters (Grayscale, Invert, and Sepia) without any physical contact, simply by moving their hands closer together or further apart.

# 🖐️ Hand Gesture Controlled Camera Filters (El Hareketleri ile Canlı Kamera Filtreleri)

Bu proje; bilgisayar kamerası (webcam) karşısında iki elinizi birbirine yaklaştırıp uzaklaştırarak canlı video akışındaki filtreleri gerçek zamanlı olarak değiştirmenizi sağlayan bir **Bilgisayarlı Görü (Computer Vision)** uygulamasıdır.

Yapay zeka tabanlı el izleme teknolojisi sayesinde herhangi bir fiziksel butona dokunmadan, sadece el hareketlerinizle görüntüyü manipüle edebilirsiniz.

---

## ✨ Özellikler

* **Çift El Takibi:** MediaPipe Hands teknolojisi ile iki elin eklem noktalarını anlık olarak asenkron izleme.
* **Dinamik Mesafe Ölçümü:** İki elin merkez noktaları (orta parmak kökleri) arasındaki Öklid mesafesini hesaplama.
* **Gerçek Zamanlı Filtre Uygulamaları:**
    * **Normal Mod:** Eller algılanmadığında veya varsayılan durumda orijinal görüntü.
    * **Siyah-Beyaz (Grayscale):** Eller birbirine çok yakınken ($< 180$ piksel).
    * **Ters/Negatif (Invert):** Eller orta mesafedeyken ($180 - 350$ piksel arası).
    * **Sepya (Nostaljik Ton):** Eller birbirinden uzakken ($> 350$ piksel).
* **Görsel Geribildirim:** Ekran üzerinde aktif filtre adını, anlık piksel mesafesini ve eller arasındaki bağlantı çizgisini dinamik olarak gösterme.

---

## 🛠️ Kullanılan Teknolojiler

* **Python 3.x**
* **OpenCV (opencv-python):** Kamera yönetimi, görüntü işleme ve matris manipülasyonu.
* **MediaPipe:** Google tarafından geliştirilen, cihaz üzerinde yüksek performansla çalışan el ve eklem takibi yapay zeka modeli.
* **NumPy:** Sepya filtresi gibi renk matrisi çarpımlarında hızlı matematiksel hesaplamalar için.

---

## 🚀 Kurulum ve Çalıştırma

### 1. Gereksinimlerin Yüklenmesi

Projeyi bilgisayarınızda çalıştırmak için öncelikle gerekli kütüphaneleri terminaliniz üzerinden yükleyin:

pip install opencv-python mediapipe numpy


2. Projenin Çalıştırılması
Kodu içeren Python dosyasını ( camera.py) çalıştırın:
python camera.py


3. Kullanım Talimatları
Program başladıktan sonra web kameranız aktif hale gelecektir.

Filtre geçişlerini tetiklemek için iki elinizi de kameraya gösterin.

Ellerinizi birbirine yaklaştırarak veya uzaklaştırarak filtreler arasındaki canlı geçişi izleyin.

Uygulamadan çıkmak için klavyeden q tuşuna basmanız yeterlidir.


🧠 Çalışma Mantığı
Kameradan alınan her bir kare (frame), MediaPipe modeline gönderilmeden önce yatay olarak çevrilir (aynalama etkisi engellenir).

hands.process() fonksiyonu ile eller tespit edilir ve her el için 21 referans noktası çıkarılır.

Elin en stabil noktası olan 9 numaralı eklem (orta parmak kökü) merkez kabul edilerek iki el arasındaki mesafe şu formülle hesaplanır:


$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$


Hesaplanan piksel mesafesine göre ilgili OpenCV filtre fonksiyonu (renk dönüşümü, bit düzeyinde tersini alma veya kernel matris çarpımı) tetiklenir.
