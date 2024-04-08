import argparse
import socket
import logging
import time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor


def scan_port(host, port):
    start_time=time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 设置超时时间
        port = int(port)
        result = sock.connect_ex((host, port))
        if result == 0:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error scanning port {port}: {e}")
    finally:
        sock.close()
        end_time=time.time()
        scan_duration = end_time - start_time
        logging.info(f"Scanning port {port} took {scan_duration:.2f} seconds")


def parse_args():
    parser = argparse.ArgumentParser(description="Python Port Scanner")
    parser.add_argument("-he", "--host", help="Target host or URL")
    parser.add_argument("-p", "--port",  help="Target port")
    parser.add_argument("-pf", "--portfile",
                        help="File containing list of ports")
    parser.add_argument("-hf", "--hostfile",
                        help="File containing list of hosts")
    parser.add_argument("-l", "--log", help="Log file name")
    return parser.parse_args()


def sport(host, port):
    # 指定特定端口
    if("," in port):
        ports = port.split(',')
        for p in ports:
            p = int(p)
            if scan_port(host, p):
                print(f"Port {p} is open on {host}")
                logging.info(f"Port {p} is open on {host}")
            else:
                print(f"Port {p} is closed on {host}")
                logging.info(f"Port {p} is closed on {host}")
    # 指定端口范围
    elif("-" in port):
        ports = port.split('-')
        start = int(ports[0])
        end = int(ports[1])
        with ThreadPoolExecutor(100) as t:
            for p in range(start, end+1):
                if scan_port(host, p):
                    print(f"Port {p} is open on {host}")
                    logging.info(f"Port {p} is open on {host}")
                else:
                    print(f"Port {p} is closed on {host}")
                    logging.info(f"Port {p} is closed on {host}")
    # 单个端口
    else:
        if scan_port(host, port):
            print(f"Port {port} is open on {host}")
            logging.info(f"Port {port} is open on {host}")
        else:
            print(f"Port {port} is closed on {host}")
            logging.info(f"Port {port} is closed on {host}")


def main():
    args = parse_args()

    # 设置日志
    logging.basicConfig(filename=args.log, level=logging.INFO,
                        format='%(asctime)s %(message)s')
    if args.hostfile:
        with open(args.hostfile, 'r') as f:
            for line in f:
                url = urlparse(line.strip())
                host = url.netloc or url.path
                if args.port:
                    sport(host, args.post)
                elif args.portfile:
                    with open(args.file, 'r') as f:
                        for line in f:
                            port = line.strip()
                            if scan_port(host, port):
                                print(f"Port {port} is open on {host}")
                                logging.info(f"Port {port} is open on {host}")
                            else:
                                print(f"Port {port} is closed on {host}")
                                logging.info(f"Port {port} is closed on {host}")
    elif args.host:
        url = urlparse(args.host.strip())
        host = url.netloc or url.path
        if args.portfile:
            with open(args.file, 'r') as f:
                for line in f:
                    port = line.strip()
                    if scan_port(arg.host, port):
                        print(f"Port {port} is open on {host}")
                        logging.info(f"Port {port} is open on {host}")
                    else:
                        print(f"Port {port} is closed on {host}")
                        logging.info(f"Port {port} is closed on {host}")
        elif args.port:
            sport(host,args.port)
        else:
            logging.info("we need posts")
    else:
        logging.info("we need a host")


if __name__ == "__main__":
    main()
