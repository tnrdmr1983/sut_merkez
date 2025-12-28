import requests
from bs4 import BeautifulSoup
import json

def sut_verisi_cek():
    # Bu kısım senin sitendeki güncel listeyi simüle eder veya SGK'dan çeker
    # Şimdilik sistemin çalışması için örnek bir veri seti oluşturuyoruz
    kurallar = {
        "kolesterol": {
            "baslik": "Kolesterol (LDL) Sınırı",
            "ldl_sinir": 160
        },
        "beslenme": {
            "baslik": "Mama (VKI) Sınırı",
            "vki_sinir": 18.5
        }
    }
    
    # Dosyayı oluşturmayı zorla
    with open('taslak_kurallar.json', 'w', encoding='utf-8') as f:
        json.dump(kurallar, f, ensure_ascii=False, indent=4)
    print("Taslak dosyası başarıyla oluşturuldu!")

if __name__ == "__main__":
    sut_verisi_cek()
