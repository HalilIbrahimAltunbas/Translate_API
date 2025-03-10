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
    operation_a_command = "python operation_a.py"
    operation_b_command = "python operation_b.py"
    api_gateway_command = "python api_gateway.py"

    # Mikroservisleri başlat
    start_service("Authentication", auth_service_command)
    start_service("Operation A", operation_a_command)
    start_service("Operation B", operation_b_command)
    start_service("API Gateway", api_gateway_command)

    # Servislerin çalışmasını bekleyelim (opsiyonel)
    print("Tüm servisler başlatıldı. Sistem çalışıyor...")
    while True:
        time.sleep(60)  # Servisler çalışırken sürekli bekleme

if __name__ == "__main__":
    main()
