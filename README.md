# Giss Print Agent

---

Giss Print Agent, web uygulamalarından yerel yazıcılara doğrudan ve sessiz (diyalog penceresi olmadan) çıktı göndermenizi sağlayan basit bir ara katman yazılımıdır.

### Nedir?
Bu araç, bilgisayarınızda arka planda çalışarak tarayıcıdan gelen yazdırma komutlarını alır ve Windows yazıcılarınıza iletir. Özellikle etiket yazdırma veya fatura kesme gibi süreçlerde hızı artırmak için tasarlanmıştır.

### Gereksinimler
- **İşletim Sistemi:** Windows 10 / 11
- **Python:** 3.8 veya üzeri (Sadece geliştirme ve derleme için)
- **Bağımlılık:** SumatraPDF (Portable sürüm)

### Nasıl Kullanılır?
1.  `config.json` dosyasından portu ve güvenlik anahtarını (api_key) ayarlayın.
2.  `GissPrintAgent.exe` dosyasını çalıştırın.
3.  Aşağıdaki örnekteki gibi bir istek gönderin:

```javascript
fetch('http://localhost:5000/print', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-Api-Key': 'giss_secret_token'
    },
    body: JSON.stringify({
        printer_name: 'Yazici_Adi',
        pdf_data: 'Base64_PDF_Verisi'
    })
});
```

### Derleme ve Dağıtım
1.  **Exe Oluşturma:** Windows bir makinede `build.bat` dosyasını çalıştırın. Bu işlem `dist` klasörü içinde `GissPrintAgent.exe` dosyasını oluşturacaktır.
2.  **Kullanıcıya Kurulum:**
    - Bir klasör oluşturun (örn: `C:\GissPrintAgent`).
    - `dist/GissPrintAgent.exe` dosyasını bu klasöre kopyalayın.
    - İndirdiğiniz `SumatraPDF.exe` dosyasını da aynı klasöre koyun.
    - `config.json` dosyasını da yanlarına ekleyerek ayarlarınızı yapın.
3.  **Çalıştırma:** `GissPrintAgent.exe` dosyasını çalıştırdığınızda servis hazır hale gelecektir.

**Önemli:** Yazdırma işleminin çalışması için `SumatraPDF.exe` dosyası uygulama ile aynı klasörde bulunmalıdır.
- [SumatraPDF Portable İndir](https://www.sumatrapdfreader.org/download-free-pdf-viewer)

### Gelecek Özellikler (Yol Haritası)
Bu proje geliştirmeye açıktır. İleride eklenmesi planlanan bazı özellikler:
- **RAW Yazdırma:** Zebra (ZPL) veya Fiş yazıcıları (ESC/POS) için doğrudan komut desteği.
- **Kağıt Kaynağı Seçimi:** Yazıcının hangi tepsisinden (çekmecesinden) kağıt alacağının seçilebilmesi.
- **HTTPS Desteği:** Güvenli bağlantı üzerinden iletişim.
- **Kuyruk İzleme:** Yazdırma işlerinin durumunu takip etme.

---

Giss Print Agent is a simple middleware that allows web applications to send silent print jobs directly to local printers without user interaction.

### What is it?
It runs in the background on your computer, receiving print commands from the browser and forwarding them to Windows printers. It is designed to speed up processes like label or invoice printing.

### Requirements
- **Operating System:** Windows 10 / 11
- **Python:** 3.8 or higher (Only for development and building)
- **Dependency:** SumatraPDF (Portable version)

### How to Use?
1.  Configure the port and security key (api_key) in `config.json`.
2.  Run `GissPrintAgent.exe`.
3.  Send a request as shown in the example below:

```javascript
fetch('http://localhost:5000/print', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-Api-Key': 'giss_secret_token'
    },
    body: JSON.stringify({
        printer_name: 'Printer_Name',
        pdf_data: 'Base64_PDF_Data'
    })
});
```

### Building and Distribution
1.  **Create Exe:** Run `build.bat` on a Windows machine. This will generate `GissPrintAgent.exe` inside the `dist` folder.
2.  **User Installation:**
    - Create a folder (e.g., `C:\GissPrintAgent`).
    - Copy `dist/GissPrintAgent.exe` to this folder.
    - Place the downloaded `SumatraPDF.exe` in the same folder.
    - Add `config.json` to the same folder and adjust your settings.
3.  **Run:** Execute `GissPrintAgent.exe` to start the service.

**Note:** `SumatraPDF.exe` must be in the same folder as the application for printing to work.
- [Download SumatraPDF Portable](https://www.sumatrapdfreader.org/download-free-pdf-viewer)

### Future Features (Roadmap)
This project is open for further development. Planned features include:
- **RAW Printing:** Direct command support for Zebra (ZPL) or Receipt printers (ESC/POS).
- **Paper Tray Selection:** Ability to choose which printer tray/drawer to use for the job.
- **HTTPS Support:** Communication over secure connections.
- **Queue Monitoring:** Tracking the status of print jobs.
