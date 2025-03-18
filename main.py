import subprocess
import time

def start_service(service_name, command):
    """Servisi başlatan yardımcı fonksiyon"""
    print(f"{service_name} servisi başlatılıyor...")
    subprocess.Popen(command, shell=True)
    time.sleep(1)  # Biraz bekleyelim, servis tam olarak başlasın

def main():
    # Mikroservislerin çalıştırılması için komutlar
    auth_service_command = "python auth_service.py"
    translate_text_command = "python src/text_translate/translate-text.py"
    Data_access_command = "python src/Data_access/db.py"
    Speech_recognition_command = "python src/Speech_Recognition/Speech_recognation.py"
    api_gateway_command = "python src/gateway.py"

    

    # Mikroservisleri başlat
    # start_service("Authentication", auth_service_command)
    start_service("translate-text", translate_text_command)
    start_service("Data_access", Data_access_command)
    start_service("API Gateway", api_gateway_command)
    start_service("API Speech_Recognition", Speech_recognition_command)

    # Servislerin çalışmasını bekleyelim (opsiyonel)
    print("Tüm servisler başlatıldı. Sistem çalışıyor...")
    while True:
        time.sleep(60)  # Servisler çalışırken sürekli bekleme

if __name__ == "__main__":
    main()
