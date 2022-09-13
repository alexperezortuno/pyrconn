import sys
import argparse

from core.ftp import Ftp
from core.ssh import Ssh


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Cli for send commands to ssh",
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("-d", "--domain", help="host ip or domain", type=str)
        parser.add_argument("-u", "--username", help="username", type=str)
        parser.add_argument("-p", "--password", help="password", type=str)
        parser.add_argument("-c", "--command", help="command", type=str)
        parser.add_argument("--private", help="private", type=bool, default=False)
        parser.add_argument("--port", help="port", type=int, default=22)
        parser.add_argument("--connection", help="port", type=str, default="ssh")
        args = parser.parse_args()

        if args.connection == "ssh":
            ssh = Ssh(vars(args))
            ssh.start()
        if args.connection == "ftp":
            ftp = Ftp(vars(args))
            ftp.start()
        sys.exit(0)
    except KeyboardInterrupt as e:
        print(f'KeyboardInterrupt {e}')
        sys.exit(1)
