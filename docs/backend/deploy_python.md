# Cara Deploy Backend (Python)

Untuk Backend yang menggunakan Python dapat dideploy menggunakan Docker. Berikut adalah langkah-langkah untuk melakukan deploy:

1. **Clone Repository**

    Gunakan perintah berikut untuk meng-clone repository:

     ```bash
     git clone https://github.com/IoT-Smart-Hydroponic/smart-hydroponic.git -b dev-python
     ```

    !!! note "Catatan"
        Pastikan Anda meng-clone repository dengan branch `dev-python`. Branch ini khusus untuk backend yang menggunakan Python. Dapat berubah sewaktu-waktu ketika versi stabil sudah siap.

2. **Masuk ke Direktori Backend**

    Setelah repository berhasil di-clone, masuk ke direktori backend dengan perintah berikut:

    ```bash
    cd smart-hydroponic/backend
    ```

3. **Build Docker Image**

    Gunakan perintah berikut untuk membuild Docker image:

    ```bash
    docker compose up -d
    ```

    Perintah ini akan membaca file `docker-compose.yml` yang ada di direktori backend dan membuild image TimeScaleDB + PostgreSQL serta image untuk aplikasi backend Python.

4. **Cek Status Container**
    Setelah build selesai, cek status container dengan perintah berikut:

    ```bash
    docker ps
    ```

    Pastikan container untuk backend berjalan dengan baik.

5. **Cek Log Aplikasi**
    Untuk memastikan aplikasi berjalan dengan baik, cek log aplikasi dengan perintah berikut:

    ```bash
    docker logs <container_id>
    ```

    Gantilah `<container_id>` dengan ID container backend yang didapat dari perintah `docker ps`.

    atau bisa menggunakan:

    ```bash
    docker compose logs -f
    ```

    Perintah ini akan menampilkan log secara real-time.

6. **Akses Aplikasi**
    Akses aplikasi dengan membuka browser dan mengunjungi `http://your_domain_or_ip`.

    Gantilah `your_domain_or_ip` dengan domain atau alamat IP server tempat backend di-deploy.

7. **Menghentikan Aplikasi**
    Jika Anda perlu menghentikan aplikasi, gunakan perintah berikut:

    ```bash
    docker compose down
    ```

    Perintah ini akan menghentikan dan menghapus container yang berjalan.

    dan untuk menjalankan kembali:

    ```bash
    docker compose up -d
    ```
