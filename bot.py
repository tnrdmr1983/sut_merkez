import requests
from bs4 import BeautifulSoup
import json

# 1. SGK Duyurular Sayfasını Tara
def sgk_tara():
    url = "https://www.sgk.gov.tr/duyurular"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # "Bedeli Ödenecek İlaçlar" geçen en son duyuruyu bul
    duyuru = soup.find("a", text=lambda t: t and "Bedeli Ödenecek İlaçlar" in t)
    
    if duyuru:
        print("Yeni bir duyuru bulundu!")
        # Burada Excel indirme ve okuma işlemleri yapılacak
        # Şimdilik simüle ediyoruz:
        yeni_kurallar = {
            "kolesterol": {"ldl_sinir": 160, "mesaj": "SGK Duyurusu ile güncellendi."},
            "beslenme": {"vki_sinir": 18.5, "mesaj": "Güncel SUT verisi."}
        }
        
        with open('kurallar.json', 'w', encoding='utf-8') as f:
            json.dump(yeni_kurallar, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    sgk_tara()
