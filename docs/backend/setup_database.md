# Konfigurasi Database Backend

Database yang digunakan dalam proyek ini adalah PostgreSQL dengan ekstensi TimescaleDB. Berikut adalah langkah-langkah untuk mengatur database backend:

**Catatan**: Guide ini ditujukan untuk pengaturan database dilakukan sekali saja, sebelum melakukan deploy backend. Jika terdapat masalah dengan database, Anda dapat mengulangi langkah-langkah ini.

1. **Install PostgreSQL dan TimescaleDB**

    Pastikan Anda telah menginstall PostgreSQL dan TimescaleDB di sistem Anda. Anda dapat mengikuti petunjuk instalasi resmi dari [PostgreSQL](https://www.postgresql.org/download/) dan [TimescaleDB](https://docs.tigerdata.com/self-hosted/latest/install/). Instal sesuai dengan sistem operasi yang Anda gunakan. Khusus untuk server gunakan versi Linux.

    - Saat menjalankan Timescaledb tune, cermati output rekomendasi yang diberikan. Sesuaikan jangan terlalu tinggi atau terlalu rendah.

    !!! info "Versi yang Direkomendasikan"
        Gunakan versi PostgreSQL terbaru yang kompatibel dengan TimescaleDB dengan dukungan UUIDv7. Untuk saat ini, versi terbaru adalah Postgrsql 18.x dan TimeScaleDB 2.24

2. **Buat Database**

    - Setelah PostgreSQL terinstal, buat database dan user yang diperlukan. Gunakan perintah berikut untuk masuk ke PostgreSQL:

        ```bash
        psql -U postgres
        ```

    - Setelah masuk, buat database dengan nama `smart_hydroponic`:

        ```psql
        CREATE DATABASE iot_hydroponik;
        ```

    - Membuat user baru dengan nama sesuai keingingan anda bila dijalankan di lokal, sedangkan di server gunakan user `admin_iot_db`:

        ```psql
        CREATE USER admin_iot_db WITH PASSWORD 'your_password';
        ```

        Catatan: Gantilah `your_password` dengan password yang Anda inginkan. Untuk server, gunakan password yang sudah disepakati bersama.

    - Berikan hak akses kepada user tersebut untuk database yang telah dibuat:

        ```psql
        GRANT ALL PRIVILEGES ON DATABASE iot_hydroponik TO admin_iot_db;
        ```

3. Lakukan deployment pada server sesuai dengan [panduan deploy backend](deploy.md).

!!! warning "Penting"
    Pastikan tidak ada kesalahan saat melakukan konfigrasi, terutama pada ekstensi TimescaleDB.
