from src.server.server import Server

"""Server Address"""
IP = "127.0.0.1"
PORT = 9000

def main():
    server = Server(IP, PORT)
    server.run()
    
if __name__ == '__main__':
    main()