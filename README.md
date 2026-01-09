# Giss Print Agent

---

Giss Print Agent, web uygulamalarından yerel yazıcılara doğrudan ve sessiz (diyalog penceresi olmadan) çıktı göndermenizi sağlayan basit bir ara katman yazılımıdır.

### Nedir?
Bu araç, bilgisayarınızda arka planda çalışarak tarayıcıdan gelen yazdırma komutlarını alır ve Windows yazıcılarınıza iletir. Özellikle etiket yazdırma veya fatura kesme gibi süreçlerde hızı artırmak için tasarlanmıştır.

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

**Not:** Yazdırma işleminin çalışması için `SumatraPDF.exe` dosyası uygulama ile aynı klasörde bulunmalıdır.

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

**Note:** `SumatraPDF.exe` must be in the same folder as the application for printing to work.

### Future Features (Roadmap)
This project is open for further development. Planned features include:
- **RAW Printing:** Direct command support for Zebra (ZPL) or Receipt printers (ESC/POS).
- **Paper Tray Selection:** Ability to choose which printer tray/drawer to use for the job.
- **HTTPS Support:** Communication over secure connections.
- **Queue Monitoring:** Tracking the status of print jobs.
