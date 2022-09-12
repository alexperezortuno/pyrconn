import getpass
from typing import Any

import threading, paramiko
import sys
import argparse

from paramiko.transport import Transport


class Ssh:
    client_ssh: paramiko.SSHClient
    client_ftp: paramiko.SFTPClient

    def __init__(self, param: dict = {}):
        self.host = param.get('domain', '')
        self.username = param.get('username', '')
        self.password = param.get('password', '')
        self.command = param.get('command', '')
        self.port = param.get('port', 22)

        thread = threading.Thread(target=self.executing_command)
        thread.daemon = True
        thread.start()

    def get_parameters(self):
        try:
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
            self.client_ssh = paramiko.SSHClient()
            self.client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client_ssh.load_system_host_keys()
            self.client_ssh.connect(hostname=self.host,
                                username=self.username,
                                password=self.password,
                                port=self.port)
        except Exception as e:
            print(f'connection error: {e}')
            sys.exit(1)

    def executing_command(self):
        try:
            stdin, stdout, stderr = self.client_ssh.exec_command(self.command,
                                                             bufsize=-1,
                                                             timeout=None,
                                                             get_pty=True,
                                                             environment=None)
            print(stdout.read().decode('utf-8'))
            # for line in iter(stdout.readline, ""):
            #     print(line, end="")
        except Exception as e:
            print(f'error execution command {e}')
            sys.exit(1)

    def start(self):
        self.get_parameters()
        self.create_connection()

        shell = self.client.invoke_shell()

        try:
            self.executing_command()
        except Exception as e:
            print(f'ssh connection error: {e}')
            sys.exit(1)
        finally:
            shell.close()
            self.client_ssh.close()


class Ftp:
    def __init__(self, param: dict = {}):
        self.host = param.get('domain', '')
        self.username = param.get('username', '')
        self.password = param.get('password', '')

    def create_connection(self) -> None:
        try:
            transport: Transport = Transport((self.host, self.port))
            transport.connect(username=self.username, password=self.password)
            self.client_ftp = paramiko.SFTPClient.from_transport(transport)
        except Exception as e:
            print(f'connection error: {e}')
            sys.exit(1)

    def start(self) -> None:
        try:
            self.create_connection()
            self.client_ftp.listdir()
        except Exception as e:
            print(f'ftp connection error: {e}')
        finally:
            self.client_ftp.close()


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Cli for send commands to ssh",
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("-d", "--domain", help="host ip or domain", type=str)
        parser.add_argument("-u", "--username", help="username", type=str)
        parser.add_argument("-p", "--password", help="password", type=str)
        parser.add_argument("-c", "--command", help="command", type=str)
        parser.add_argument("--port", help="port", type=int, default=22)
        parser.add_argument("--connection", help="port", type=str, default="ssh")
        args = parser.parse_args()

        if args.connection == "ssh":
            ssh = Ssh(vars(args))
            ssh.start()
        if args.connection == "ftp":
            ftp = Ftp(vars(args))
            ftp.start()
    except KeyboardInterrupt as e:
        print(f'KeyboardInterrupt {e}')
        sys.exit(1)
