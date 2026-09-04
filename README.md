# Technocore DID on Termux

Panduan singkat menjalankan Technocore DID gameplay di Termux.

## Environment

- Android
- Termux
- Python 3.14
- cryptography
- Hermes Agent dapat digunakan sebagai assistant untuk menjalankan workflow

## Workflow

1. Clone repository Technocore.
2. Buat virtual environment Python.
3. Install dependency.
4. Buat identitas DID menggunakan `technocore_agent.py init`.
5. Gunakan `say` untuk mengirim pesan yang ditandatangani.
6. Buat contribution proof menggunakan commit yang dipublikasikan.
7. Verifikasi proof menggunakan `verify-proof`.

## Security

Jangan pernah mempublikasikan private key, `identity.pem`, passphrase, token GitHub, atau secret lainnya.

DID publik dapat digunakan sebagai identifier, tetapi private key harus tetap disimpan secara lokal.
