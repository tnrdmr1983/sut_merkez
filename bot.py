import requests
from bs4 import BeautifulSoup
import pandas as pd # Excel okumak için
import json
import re # Metin içinden sayıları ayıklamak için

def veriyi_ayikla(metin):
    # Metin içinde LDL ve yanındaki sayıyı arar
    ldl_match = re.search(r'LDL\s*[>=]*\s*(\d+)', metin)
    vki_match = re.search(r'VKI\s*[<=]*\s*(\d+\.?\d*)', metin)
    
    sonuc = {}
    if ldl_match: sonuc['ldl_sinir'] = int(ldl_match.group(1))
    if vki_match: sonuc['vki_sinir'] = float(vki_match.group(1))
    return sonuc

def sgk_bot_calistir():
    # 1. Adım: Duyuruları tara
    url = "https://www.sgk.gov.tr/duyurular"
    try:
        r = requests.get(url, timeout=30)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # En güncel "Bedeli Ödenecek İlaçlar Listesi" duyurusunu bul
        link = soup.find("a", string=re.compile("Bedeli Ödenecek İlaçlar Listesi", re.I))
        
        if link:
            excel_url = "https://www.sgk.gov.tr" + link['href']
            print(f"Excel indiriliyor: {excel_url}")
            
            # 2. Adım: Excel'i indir ve Oku
            df = pd.read_excel(excel_url)
            
            # 3. Adım: Kritik satırları tara
            kurallar = {
                "kolesterol": {"baslik": "Kolesterol", "ldl_sinir": 190},
                "beslenme": {"baslik": "Mama", "vki_sinir": 18.5}
            }
            
            # Excel sütun ismini kontrol et (SGK bazen AÇIKLAMALAR bazen NOTLAR yazabilir)
            sutun_adi = 'AÇIKLAMALAR' if 'AÇIKLAMALAR' in df.columns else df.columns[-1]
            
            for index, row in df.iterrows():
                aciklama = str(row[sutun_adi])
                bulunan = veriyi_ayikla(aciklama)
                if 'ldl_sinir' in bulunan: kurallar['kolesterol']['ldl_sinir'] = bulunan['ldl_sinir']
                if 'vki_sinir' in bulunan: kurallar['beslenme']['vki_sinir'] = bulunan['vki_sinir']

            # --- DEĞİŞİKLİK BURADA: CANLIYI BOZMA, TASLAK OLUŞTUR ---
            # 4. Adım: Taslak dosyayı kaydet (Admin onayı için)
            with open('taslak_kurallar.json', 'w', encoding='utf-8') as f:
                json.dump(kurallar, f, ensure_ascii=False, indent=2)
            print("İşlem tamam: taslak_kurallar.json oluşturuldu. Onay bekleniyor.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    sgk_bot_calistir()
 
