from src.client import Client
import random

if __name__ == "__main__":
    client = Client()
    while True:
        client_input:str = input("-->")
        if client_input == "connect":
            client.connect()
        elif client_input.startswith("ip"):
            print("set ip to " + client_input[2:])
            client.serverAddress.ip = client_input[2:]
        elif client_input.startswith("port"):
            print("set port to " + client_input[4:])
            client.serverAddress.port = int(client_input[4:])
        else:
            response = client.send_tcp_message(client_input)
            print(response)
    