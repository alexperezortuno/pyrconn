import getpass
import threading
import sys
import paramiko


class Ssh:
    client: paramiko.SSHClient

    def __init__(self, param: dict = {}):
        self.host = param.get('domain', '')
        self.username = param.get('username', '')
        self.password = param.get('password', '')
        self.command = param.get('command', '')
        self.port = param.get('port', 22)
        self.private = param.get('private', False)

        if self.private:
            self.private_key_path = param.get('private_key_path', '~/.ssh/id_rsa')
            self.key = paramiko.RSAKey.from_private_key_file(self.private_key_path)

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.load_system_host_keys()

        # thread = threading.Thread(target=self.executing_command)
        # thread.daemon = True
        # thread.start()

    def get_parameters(self):
        try:
            if self.private is False:
                if self.host == '':
                    self.host = input('domain or host ip: ')
                if self.username == '':
                    self.username = input('user: ')
                if self.password == '':
                    self.password = getpass.getpass()
                if self.command == '':
                    self.command = input('command: ')
        except Exception as e:
            print(f'error getting parameters {e}')
            sys.exit(1)

    def create_connection(self):
        try:
            if self.private is False:
                self.client.connect(hostname=self.host,
                                    username=self.username,
                                    password=self.password,
                                    port=self.port)
            else:
                self.client.connect(hostname=self.host,
                                    username=self.username,
                                    pkey=self.key,
                                    port=self.port)
        except Exception as e:
            print(f'connection error: {e}')
            sys.exit(1)

    def executing_command(self):
        try:
            commands = ";".join(self.command.split("\n"))
            stdin, stdout, stderr = self.client.exec_command(commands,
                                                             bufsize=-1,
                                                             timeout=None,
                                                             get_pty=True,
                                                             environment=None)
            print(stdout.read().decode('utf-8'))
        except Exception as e:
            print(f'error execution command {e}')
            sys.exit(1)

    def start(self):
        try:
            self.get_parameters()
            self.create_connection()
            self.executing_command()
            sys.exit(0)
        except Exception as e:
            print(f'ssh connection error: {e}')
            sys.exit(1)
        finally:
            self.client.close()
