import paramiko
import sys
from paramiko.transport import Transport


class Ftp:
    client: paramiko.SFTPClient

    def __init__(self, param: dict = {}):
        self.host = param.get('domain', '')
        self.username = param.get('username', '')
        self.password = param.get('password', '')

    def create_connection(self) -> None:
        try:
            transport: Transport = Transport((self.host, self.port))
            transport.connect(username=self.username, password=self.password)
            self.client = paramiko.SFTPClient.from_transport(transport)
        except Exception as e:
            print(f'connection error: {e}')
            sys.exit(1)

    def start(self) -> None:
        try:
            self.create_connection()
            self.client.listdir()
        except Exception as e:
            print(f'ftp connection error: {e}')
        finally:
            self.client.close()
