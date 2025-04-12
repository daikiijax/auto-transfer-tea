# Auto TEA Sepolia Transfer Bot

Bot Python untuk mengirim token native TEA di jaringan TEA Sepolia secara otomatis ke beberapa alamat penerima, dengan interval waktu tertentu.

## Fitur
- Transfer otomatis setiap beberapa detik
- Randomisasi penerima dari daftar alamat
- Estimasi biaya gas
- Koneksi ke RPC kustom
- Deteksi koneksi jaringan

## Instalasi
```bash
pip install -r requirements.txt

Konfigurasi
Buat file .env dengan isi:
SENDER_ADDRESS=0xAlamatWallet
PRIVATE_KEY=privatekey
TEA_SEPOLIA_RPC=https://rpc-kamu
RECEIVER_ADDRESSES=0xReceiver1,0xReceiver2

Menjalankan
bash
python auto_tea_transfer.py
