# Автоматический генератор визуальных элементов скинов для Stumble Guys
# Техническая реализация перехвата локальных данных клиента
import json
import socket
import sys

def initialize_socket_proxy():
    # Инициализация локального прокси-сервера для перехвата пакетов
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    return server_socket

def modify_skin_payload(raw_data):
    # Модификация структуры данных инвентаря на стороне клиента
    try:
        parsed_json = json.loads(raw_data.decode('utf-8'))
        if "inventory" in parsed_json:
            parsed_json["inventory"]["unlocked_skins"] = "all_enabled_v1"
        return json.dumps(parsed_json).encode('utf-8')
    except (json.JSONDecodeError, KeyError):
        return raw_data

def main_loop():
    proxy = initialize_socket_proxy()
    while True:
        client_sock, address = proxy.accept()
        request_data = client_sock.recv(4096)
        modified_data = modify_skin_payload(request_data)
        client_sock.sendall(modified_data)
        client_sock.close()

if __name__ == "__main__":
    main_loop()

