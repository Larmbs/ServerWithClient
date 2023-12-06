from abc import ABC, abstractmethod
from socket import socket
from src.user.request import UDPRequest, TCPRequest
import threading

Address_Type = tuple[str, int]

"""Abstract Connection base class for server client communication"""
class Connection(ABC):
    @abstractmethod
    def __init__(self, server, conn:socket, addr:Address_Type, buffer:int):
        self.server = server
        self.conn:socket = conn
        self.addr:Address_Type = addr
        self.header:int = buffer
        self.isRunning:bool = True
    
    @abstractmethod
    def listenFor(self) -> None:
        """Listens for incoming message"""

    @abstractmethod
    def process(self, message:str) -> str:
        """Return server response after necessary operations"""
        
    @abstractmethod
    def sendTo(self, message:str, addr:Address_Type) -> None:
        """Sends message"""

    
"""UDP connection handler"""
class UDPConnection(Connection):
    def __init__(self, server, addr:Address_Type, buffer:int, message:bytes):
        super().__init__(server, None, addr, buffer)
        self.message:bytes = message
        self.isRunning:bool = True
        print(type(message))
        self.connection = threading.Thread(target=self.process, args=(message,))
        self.connection.start()
    
    def listenFor(self) -> None:
        # Ignore
        return super().listenFor()
    
    def process(self, message:bytes) -> None:
        clientMsg = self.server.decode_message(message)

        response = UDPRequest(clientMsg, self.addr).response()
        if response == "ignore":
            return
        self.sendTo(response, self.addr)
        
    def sendTo(self, message:str, addr:Address_Type) -> None:
        self.server.send_udp_message(message, addr)


"""TCP connection handler"""
class TCPConnection(Connection):
    def __init__(self, server, conn:socket, addr:Address_Type, buffer:int):
        super().__init__(server, conn, addr, buffer)
        self.isRunning:bool = True
        
        self.listener = threading.Thread(target=self.listenFor, args=())
        self.listener.start()
        
    def listenFor(self) -> None:
        while self.isRunning:
            try:
                msg_length = self.server.decode_message(self.conn.recv(self.header))
                if msg_length:
                    message = self.server.decode_message(self.conn.recv(int(msg_length)))
                    data = self.process(message)
                    if data == "bye":
                        # Handle the case where the process method indicates the connection should be closed
                        self.isRunning = False
                        print("Disconnected")
                        return

                    if data != "ignore":
                        self.sendTo(data)  # Add a newline character when sending the response

            except ConnectionResetError:
                print("Connection reset by peer. Client may have closed the connection.")
                self.isRunning = False
                self.sendTo("Error")
                return

            except Exception as e:
                print(f"Error in listenFor: {e}")
                self.sendTo("Error")

        self.conn.close()

                    
    
    def close(self):
        self.isRunning = False
        self.conn.close()
        
    def process(self, message:str) -> None:
        response = TCPRequest(message, self.addr).response()
        return response

    def sendTo(self, message:str) -> None:
        self.server.send_tcp_message(message, self.conn)
        