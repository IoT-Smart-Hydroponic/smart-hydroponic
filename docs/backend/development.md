# Backend Development Guide

Panduan ini ditujukan untuk pengembang yang ingin berkontribusi pada pengembangan backend dari proyek Smart Hydroponic. Backend ini dibangun menggunakan JavaScript (Node.js) dan Python, serta menggunakan PostgreSQL dengan ekstensi TimescaleDB sebagai database.

!!! note "Catatan"
    Rencana kedepan adalah Backend menggunakan 1 Bahasa pemrograman saja, yaitu Python. Untuk JavaScript untuk pengembangan Dashboard. (Semoga Python-nya gak ngebug 🏃‍♂️💨)

## Prerequisites

Hal-hal yang perlu dipersiapkan sebelum memulai pengembangan backend:

1. Pengetahuan dasar tentang JavaScript ([Node.js](https://nodejs.org)) dan/atau [Python](https://www.python.org).
2. Pengetahuan dasar tentang [PostgreSQL](https://www.postgresql.org) dan [TimescaleDB](https://docs.timescale.com).
!!! note "Catatan"
    PostgreSQL wajib dipelajari (mirip SQL pada umumnya), sedangkan TimescaleDB adalah ekstensi untuk mengelola data time-series. Lihat dokumentasi resmi: [PostgreSQL Docs](https://www.postgresql.org/docs/) dan [TimescaleDB Docs](https://docs.timescale.com).
3. Dependency management tool seperti [npm](https://docs.npmjs.com/) (untuk JavaScript) atau [pip](https://pip.pypa.io/en/stable/) (untuk Python).
!!! info "Info"
    Untuk Python, disarankan menggunakan [`uv`](https://docs.astral.sh/uv/) dari Astral sebagai dependency management tool dan menggunakan virtual environment ([venv](https://docs.python.org/3/library/venv.html)).
4. Sintaks Linux dasar untuk menjalankan perintah di terminal (contoh: [Command-line basics](https://ubuntu.com/tutorials/command-line-for-beginners)).
5. [Docker](https://www.docker.com) (opsional, tapi disarankan) untuk menjalankan database dan backend dalam container. Lihat juga [Docker Desktop](https://www.docker.com/products/docker-desktop) dan [Dokumentasi Docker](https://docs.docker.com).

!!! info "Info"
    Semua akan dijelaskan dan dipelajari secara terpisah.
