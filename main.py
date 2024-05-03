import os
import numpy
import colorama
import threading

from mcstatus import JavaServer

class Main:
    def __init__(self, address):
        self.connected = 0
        self.disconnected = 0

        self.address = address
    
    def title_update_thread(self):
        while True:
            os.system(f"title MC Port Sniper / Connected: {self.connected} / Disconnected: {self.disconnected}")

    def scan_server_thread(self, port_start_range, port_end_range):
        start_range = int(port_start_range)
        end_range = int(port_end_range)

        current_range = start_range

        while True:
            address = f"{self.address}:{current_range}"

            server = JavaServer.lookup(address)
            try:
                status = server.status()
                self.connected += 1
                print(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.GREEN}+{colorama.Fore.LIGHTBLACK_EX}] {colorama.Fore.YELLOW}<{status.version.name}> {colorama.Fore.RESET}{address}")
            except:
                self.disconnected += 1
            
            if current_range == end_range:
                break

            current_range += 1

        return

def main():
    colorama.init(convert=True)

    os.system("cls")

    address_input = input("Address(FQDN): ")
    main_cls = Main(address_input)

    port_range_input = input("Port Range: ")
    try:
        ports = list(range(int(port_range_input.split("-")[0]), int(port_range_input.split("-")[1])))
    except:
        print(f"{colorama.Fore.RED}Port Rangeが無効です{colorama.Fore.RESET}")
        return
    
    threads_input = input("Threads: ")
    if not threads_input.isnumeric():
        print(f"{colorama.Fore.RED}スレッド数が無効です{colorama.Fore.RESET}")
        return
    
    ports_group = numpy.array_split(ports, int(threads_input))

    os.system("cls")
    print(f"{colorama.Fore.GREEN}処理を開始します{colorama.Fore.RESET}")

    threading.Thread(target=main_cls.title_update_thread).start()

    threads = []

    for port_group in ports_group:
        start_range = port_group[0]
        end_range = port_group[-1]
        thread = threading.Thread(target=main_cls.scan_server_thread, args=(start_range, end_range,))
        threads.append(thread)
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"{colorama.Fore.GREEN}全ての処理が終了して、合計「{colorama.Fore.YELLOW}{main_cls.connected}{colorama.Fore.GREEN}」個のポートを発見しました。{colorama.Fore.RESET}")

if __name__ == "__main__":
    main()
    os.system("pause")