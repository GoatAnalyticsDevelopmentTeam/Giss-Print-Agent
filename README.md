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
2.  `GissPrintAgent.exe` dosyasını çalıştırın. Uygulama sağ altta (system tray) simge durumunda çalışacaktır.
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
1.  **Exe Oluşturma:** Windows bir makinede `build.bat` dosyasını çalıştırın. Bu işlem bağımlılıkları otomatik kuracak ve `dist` klasörü içinde `GissPrintAgent.exe` dosyasını oluşturacaktır.
2.  **Paketleme:** Müşterinize göndermek için bir klasör oluşturun ve içine şu 3 dosyayı koyun:
    - `GissPrintAgent.exe` (dist klasöründen)
    - `SumatraPDF.exe` (ana dizinden)
    - `config.json` (ana dizinden)
3.  **Dağıtım:** Bu klasörü ZIP haline getirerek müşterinize iletebilirsiniz. Müşteriniz ZIP'i çıkartıp `GissPrintAgent.exe`'yi çalıştırması yeterlidir.

### Otomatik Başlatma (Windows)
Uygulamanın bilgisayar açıldığında otomatik çalışması için:
1.  `GissPrintAgent.exe` dosyasına sağ tıklayıp **Kısayol oluştur** deyin.
2.  `Windows + R` tuşlarına basıp `shell:startup` yazın ve Enter'a basın.
3.  Oluşturduğunuz kısayolu açılan **Başlangıç** klasörünün içine kopyalayın.

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
2.  Run `GissPrintAgent.exe`. The application will run in the system tray (bottom right).
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
1.  **Create Exe:** Run `build.bat` on a Windows machine. This will automatically install dependencies and generate `GissPrintAgent.exe` inside the `dist` folder.
2.  **Packaging:** Create a folder for your client and include these 3 files:
    - `GissPrintAgent.exe` (from the dist folder)
    - `SumatraPDF.exe` (from the root directory)
    - `config.json` (from the root directory)
3.  **Distribution:** ZIP this folder and send it to your client. The client just needs to extract the ZIP and run `GissPrintAgent.exe`.

### Auto-start (Windows)
To make the application start automatically when the computer boots:
1.  Right-click `GissPrintAgent.exe` and select **Create shortcut**.
2.  Press `Windows + R`, type `shell:startup`, and press Enter.
3.  Copy the shortcut you created into the **Startup** folder that opens.

**Note:** `SumatraPDF.exe` must be in the same folder as the application for printing to work.
- [Download SumatraPDF Portable](https://www.sumatrapdfreader.org/download-free-pdf-viewer)

### Future Features (Roadmap)
This project is open for further development. Planned features include:
- **RAW Printing:** Direct command support for Zebra (ZPL) or Receipt printers (ESC/POS).
- **Paper Tray Selection:** Ability to choose which printer tray/drawer to use for the job.
- **HTTPS Support:** Communication over secure connections.
- **Queue Monitoring:** Tracking the status of print jobs.
