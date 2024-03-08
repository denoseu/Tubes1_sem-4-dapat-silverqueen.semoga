# Tubes1_sem-4-dapat-silverqueen.semoga
## Anggota:
# Denise Felicia Tiowanni 13522013
# Shazya Audrea Taufik 13522063
# Shulha 13522087

## Implementasi Greedy
Salah satu alternatif algoritma yang digunakan pada bot kami adalah algoritma greedy by distance, diamond, dan defence. Pendekatan algoritma ini pertama-tama mencari jarak bot dengan diamond-diamond pada board dan kemudian mengambil diamond terdekat dengan mengutamakan pengambilan diamond merah dibanding biru apabila jarak antara bot dengan diamond merah lebih dekat dibanding biru. Selanjutnya, algoritma juga menghitung jarak bot dengan bot lain sehingga apabila posisi mereka adjacent, bot akan menghindar sehingga tidak terjadi tabrakan.


## Struktur Singkat Program

```
│
├── doc
│
├── src
│   ├── superqueen
│   │   ├── game
│   │   │   ├── logic
│   │   │   │   ├── super_silverqueen.py
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   ├── board_handler.py
│   │   │   ├── models.py
│   │   │   ├── util.py
│   │   ├── decode.py
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── run-bots.bat
│   │   └── run-bots.sh
│
└── README.md
```

## Prerequisite (Game-Engine)
### Catatan: Apabila game-engine di run pada sistem MacOS, hapus <code>&& cd ../..</code> pada line 7 (build) pada file package.json
1. Download .zip game-engine pada tautan berikut. 
    ```
    https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0
    ```
2. Extract .zip dan buka folder pada terminal.
3. Pindah ke direktori game-engine dengan `cd tubes1-IF2110-game-engine-1.1.0`
4. Unduh dependencies menggunakan <code>yarn</code>
5. Setup default environment variable dengan menjalankan script berikut.
    Untuk Windows
    ```
    ./scripts/copy-env.bat
    ```
    Untuk Linux dan macOS
    ``` 
    chmod +x ./scripts/copy-env.sh
    ./scripts/copy-env.sh
    ```
6. Setup local database (buka aplikasi docker desktop terlebih dahulu, lalu jalankan command `docker compose up -d database` di terminal).
7. Jalankan script berikut.
    Untuk Windows
    ```
    ./scripts/setup-db-prisma.bat
    ```
    Untuk Linux dan macOS
    ``` 
    chmod +x ./scripts/setup-db-prisma.sh
    ./scripts/setup-db-prisma.sh
    ``` 
8. Jalankan command <code>npm run build</code> di terminal.
8. Jalankan command <code>npm run start</code> di terminal.

## How to Run
1. Clone repository ini dengan 
    ```
    git clone https://github.com/denoseu/Tubes1_sem-4-dapat-silverqueen.semoga.git
    ```
2. Buka folder repository pada terminal.
3. Pindah ke direktori *src* dengan `cd src`
3. Pindah ke direktori *superqueen* dengan `cd superqueen`
4. Install dependencies menggunakan pip <code>pip install -r requirements.txt</code>
5. Run bot... (Adjust jenis python yang digunakan, apabila mengunakan python/python3).
    Untuk menjalankan satu bot superqueen pada Windows:
    ```
    start cmd /c "python main.py --logic SuperSilverqueen --email=superqueen@email.com --name=superqueen --password=superqueen --team etimo"
    ```
    Untuk menjalankan bot superqueen pada Linux dan macOS:
    ```
    python3 main.py --logic SuperSilverqueen --email=superqueen@email.com --name=superqueen --password=superqueen --team etimo &
    ```
    Untuk menjalankan beberapa bot superqueen pada Windows:
    ```
    ./run-bots.bat
    ```
    Untuk menjalankan beberapa bot superqueen pada Linus dan macOS:
    ```
    ./run-bots.sh
    ```