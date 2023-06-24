# Component and Guide
1. Monitoring   : read sla change python automation
2. Approute     : read graffic sla change python automation
3. Python version 3.7+ for windows and linux
4. Ubah user akses ke controller vmanage pada file vmanage_login.yaml
5. Kemudian jalan file events_SLA_TLK.py events_SLA_LA.py pada folder Monitoring-SLA-change
6. Secara otomatis program berjalan secara realtime dan akan mencari sla change pada batas parameter jitter, loss, latency.
7. SLA change indikator display yaitu nama hostnamenya.
8. Cari System IP pada hostname tersebut.
9. Kemudian jalankan file approute_bifast.py
10. Masukkan system ip loopbacknya
11. Menampilkan graffic terjadinya loss, jitter, latency
12. Done

# Guide User
1. Ubah private1 atau private2 sebagai tunnel protokol ipsecnya lintas/telkom.
![image](https://github.com/sourchib/python-automation-networking-sdwan/assets/60887634/8307cb22-1c30-4aec-98b4-6876395da0da)
![image](https://github.com/sourchib/python-automation-networking-sdwan/assets/60887634/ae87dcc3-e2ad-4c06-aa81-ff0c7e95beea)
ipsec menggunakan AH_SHA1_HMAC
![WhatsApp Image 2023-06-23 at 16 03 35](https://github.com/sourchib/python-automation-networking-sdwan/assets/60887634/69f8633b-4d1a-48c1-a125-ce3f8828f486)
3. Edit range dan time data zonenya start time (awal shift) sampai end_time (akhir shift)
![WhatsApp Image 2023-06-23 at 16 03 35](https://github.com/sourchib/python-automation-networking-sdwan/assets/60887634/1ab11902-220c-49f1-b82c-151740b0addb)
4. Kemudian tambahkan system ip loopback pada router, jika belum tau loopbacknya sh ip int brie.
![WhatsApp Image 2023-06-23 at 16 04 19](https://github.com/sourchib/python-automation-networking-sdwan/assets/60887634/9fcdcd80-dae1-4dea-8255-1c141cb95e52)

Thanksyou.
Best Regarts
Muchammad Muchib Zainul Fikry By github.com
Doc. https://developer.cisco.com/docs/sdwan/
