# Discord Sender

Discord Sender, Discord webhook'larına hızlı mesaj göndermenizi sağlayan minimal bir Windows masaüstü uygulamasıdır.

## Özellikler

- **Global Hotkey (Ctrl+K)**: Mesaj gönderme penceresini anında açar
- **Pano Gönderme (Ctrl+Alt+K)**: Panodaki içeriği direkt Discord'a gönderir
- **Hızlı Mesaj Gönderme**: Mesaj yazıp Enter ile gönder
- **ESC ile Kapatma**: Pencereyi ESC tuşuyla kapat
- **Minimal Dark UI**: Discord temalı, şık arayüz
- **System Tray**: Sistem tepsisinde çalışır, arka planda durur
- **Bildirimler**: Başlangıçta kısayol tuşlarını hatırlatan bildirim

## Kurulum

### Gereksinimler

- Python 3.11 veya üzeri
- Windows 10/11

### Adımlar

1. Repoyu klonlayın:
```bash
git clone https://github.com/YakupEmreYerli/DiscordSender.git
cd DiscordSender
```

2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

3. Yapılandırma dosyasını oluşturun:
```bash
copy config.example.json config.json
```

4. `config.json` dosyasını düzenleyip Discord webhook URL'nizi ekleyin:
```json
{
  "webhook_url": "YOUR_DISCORD_WEBHOOK_URL_HERE",
  "hotkey": "ctrl+k",
  "hotkey_clipboard": "ctrl+alt+k"
}
```

5. Uygulamayı çalıştırın:
```bash
python discord_sender.py
```

## Executable Oluşturma

Tek başına çalışan bir `.exe` dosyası oluşturmak için:

```bash
pip install pyinstaller
pyinstaller DiscordSender.spec --clean
```

Exe dosyası `dist/DiscordSender.exe` konumunda oluşturulacaktır.

## Kullanım

1. Uygulamayı başlatın - Sistem tepsisinde bir ikon görünecek
2. Mesaj göndermek için:
   - `Ctrl+K` tuşlarına basın
   - Mesajınızı yazın
   - `Enter` tuşuna basın
3. Panodan göndermek için:
   - Metni kopyalayın (Ctrl+C)
   - `Ctrl+Alt+K` tuşlarına basın
4. Çıkmak için:
   - Sistem tepsisindeki ikona sağ tıklayın
   - "Çıkış" seçeneğini seçin

## Yapılandırma

Tüm ayarlar `config.json` dosyasında bulunur.

### Webhook URL

Discord webhook URL'nizi almak için:
1. Discord sunucunuzda bir kanala gidin
2. Kanal ayarları > Entegrasyonlar > Webhook'lar
3. Yeni webhook oluşturun veya mevcut birini kullanın
4. Webhook URL'sini kopyalayıp `config.json` dosyasına yapıştırın

### Hotkey Özelleştirme

`config.json` dosyasında istediğiniz kısayol tuşlarını belirleyebilirsiniz:

```json
{
  "webhook_url": "YOUR_WEBHOOK_URL",
  "hotkey": "ctrl+shift+d",
  "hotkey_clipboard": "ctrl+alt+v"
}
```

## Teknolojiler

- **PySide6** - Qt tabanlı GUI framework
- **requests** - HTTP istekleri
- **keyboard** - Global hotkey desteği
- **PyInstaller** - Executable oluşturma

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request açın

## Güvenlik Uyarısı

Discord webhook URL'nizi asla herkese açık paylaşmayın. Bu URL'ye sahip olan herkes webhook'unuza mesaj gönderebilir.
