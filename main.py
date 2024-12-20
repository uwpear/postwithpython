import requests
import random
import string
import time

# Rastgele sayı ve metin üretmek için fonksiyonlar
def generate_random_number():
    return random.randint(1, 1000)

def generate_random_text(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Kullanıcıdan kaç kez istek göndereceğini al
def get_number_of_requests():
    while True:
        try:
            num_requests = int(input("Kaç kez istek göndermek istiyorsunuz? "))
            return num_requests
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")

# Veri boyutunu sormak ve buna göre uzunluk belirlemek
def get_data_size():
    while True:
        try:
            data_size = int(input("Veri boyutunu seçin: 1- Küçük, 2- Orta, 3- Büyük: "))
            if data_size == 1:
                return 10  # Küçük: 10 karakter
            elif data_size == 2:
                return 50  # Orta: 50 karakter
            elif data_size == 3:
                return 200  # Büyük: 200 karakter
            else:
                print("Lütfen geçerli bir seçenek girin.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")

# POST için form verilerini hazırla
def prepare_form_data(field_classes, data_size):
    data = {}
    for field_class in field_classes:
        field_name = field_class.get("name")
        field_type = field_class.get("type")
        
        if field_name:
            if field_type == "number":
                data[field_name] = generate_random_number()
            elif field_type == "text":
                data[field_name] = generate_random_text(data_size)
            else:
                data[field_name] = generate_random_text(data_size)
    return data

# Kullanıcıdan alan class bilgilerini al
def get_form_classes():
    field_classes = []
    num_fields = int(input("Kaç tane input alanı var? "))
    for _ in range(num_fields):
        field_name = input("Input alanının 'name' değerini girin: ")
        field_type = input(f"{field_name} için türü girin (text/number): ")
        field_classes.append({"name": field_name, "type": field_type})
    return field_classes

# GET isteği gönder
def send_get_requests(url, num_requests):
    for i in range(num_requests):
        try:
            response = requests.get(url)
            print(f"{i+1}. GET isteği gönderildi! Durum kodu: {response.status_code}")
            time.sleep(random.uniform(0.5, 2))  # Rastgele bekleme süresi
        except Exception as e:
            print(f"Hata var! GET isteği gönderilemedi: {e}")

# POST isteği gönder
def send_post_requests(url, num_requests, field_classes, data_size):
    for i in range(num_requests):
        try:
            data = prepare_form_data(field_classes, data_size)
            response = requests.post(url, data=data)
            print(f"{i+1}. POST isteği gönderildi! Durum kodu: {response.status_code}")
            print(f"Gönderilen veriler: {data}")
        except Exception as e:
            print(f"Hata var! POST isteği gönderilemedi: {e}")

# Ana işlem
def main():
    url = input("URL'yi girin: ")
    request_type = input("Hangi tür istek göndermek istiyorsunuz? (GET / POST / ALL): ").strip().upper()
    
    # Veri boyutunu al
    data_size = get_data_size()
    
    # Veri boyutuna göre istek sayısını al
    num_requests = get_number_of_requests()

    if request_type == "GET":
        send_get_requests(url, num_requests)
    elif request_type == "POST":
        field_classes = get_form_classes()
        send_post_requests(url, num_requests, field_classes, data_size)
    elif request_type == "ALL":
        field_classes = get_form_classes()
        print("Önce GET istekleri gönderiliyor...")
        send_get_requests(url, num_requests)
        print("Şimdi POST istekleri spamlanıyor...")
        send_post_requests(url, num_requests, field_classes, data_size)
    else:
        print("Geçersiz seçim. Lütfen 'GET', 'POST' veya 'ALL' seçin.")

if __name__ == "__main__":
    main()
