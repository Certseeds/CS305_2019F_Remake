import math
import random
import struct
import time
from threading import Timer
from typing import List, Set, Tuple

from lab07.src.udp_socket import UDPsocket

header_length: int = 20
data_length: int = 520
# header_format = "!B3IH"
header_format: str = "!5L"
data_format: str = "UTF-8"
SYN_bit: int = (1 << 0)
FIN_bit: int = (1 << 1)
ACK_bit: int = (1 << 2)
Reset_bit: int = (1 << 3)
udp_packet_length: int = 500
begin_bytes: bytes = b'00000000000000000000'
useless_address: Tuple[str, int] = ("127.0.0.1", 14151)


class rdt_socket(UDPsocket):
    def __init__(self):
        super().__init__()
        self.seq: int = 0
        self.seq_ack: int = 0
        self.accept_null: bool = True

    def connect(self, address):
        self.setblocking(False)
        self.client: bool = True
        header_1 = produce_packets(
            header_format, SYN_bit, self.seq, self.seq_ack)
        while True:
            self.sendto(header_1, address)
            print("send syn finish")
            time.sleep(1)
            data = begin_bytes
            try:
                data, addr_1 = self.recvfrom(data_length, )
            except BlockingIOError:
                time.sleep(1)
                continue
            except TypeError:
                time.sleep(1)
                continue
            header_2 = struct.unpack(header_format, data[0:header_length])
            if header_2[0] != SYN_bit + ACK_bit or header_2[2] != self.seq + 1 or check_sum(data):
                time.sleep(1)
                print("line 46")
                continue
            if header_2[0] == SYN_bit + ACK_bit and header_2[2] == self.seq + 1 and not check_sum(data):
                print("recieve syn ack finish")
                break
        print("jump out")
        self.seq += 1
        self.seq_ack = header_2[1] + 1
        header_3 = produce_packets(
            header_format, ACK_bit, self.seq, self.seq_ack)
        self.sendto(header_3, address)
        time.sleep(1.5)
        print("first step finish")
        re_header = begin_bytes
        for i in range(5):
            try:
                re_header, addr_2 = self.recvfrom(data_length, )
            except BlockingIOError:
                pass
            except TypeError:
                pass
            if re_header != begin_bytes:
                self.sendto(header_3, address)
            time.sleep(1)
            print("{} step finish".format(str(i)))

        self.client_address = address
        # send syn; receive syn, ack; send ack
        # your code here
        self.setblocking(False)
        print("coneect finish ")
        print(time.time())
        print(self.seq, self.seq_ack, "this is seq and seq ack")
        return

    def accept(self):
        self.client = False
        """
        相当于这玩意的作用是
        socket本身接受一个,
        发送一个
        接受一个socket,然后new一个socket with recieve 地址返回.
        :return:
        """
        self.setblocking(True)
        while True:
            self.setblocking(True)
            try:
                data, addr = self.recvfrom(data_length, )
            except TypeError:
                print("line 72")
                continue
            print("recieve syn data")
            self.setblocking(False)
            header_1 = struct.unpack(header_format, data[0:header_length])
            if header_1[0] != SYN_bit or check_sum(data):
                print(check_sum(data))
                print("line 82")
                continue
            self.seq_ack = header_1[1] + 1
            header_2 = produce_packets(
                header_format, SYN_bit + ACK_bit, self.seq, self.seq_ack)
            self.sendto(header_2, addr)
            print("send syn,ack finish")
            header_3 = begin_bytes
            count = 10
            for i in range(5):
                count -= 1
                time.sleep(1)
                try:
                    header_3, addr_2 = self.recvfrom(data_length, )
                except BlockingIOError:
                    time.sleep(1)
                except TypeError:
                    time.sleep(1)
                header_3_unpack = struct.unpack(
                    header_format, header_3[0:header_length])
                print(header_3_unpack[0] == ACK_bit, header_3_unpack[2] ==
                      self.seq + 1, check_sum(header_3), "can it jump out?")
                if header_3_unpack[0] == ACK_bit and header_3_unpack[2] == self.seq + 1 and not check_sum(header_3):
                    break
                self.sendto(header_2, addr)
            break
        time.sleep(count)
        print(header_3_unpack[0])
        print(header_3_unpack[2])
        print(self.seq + 1)
        self.seq += 1
        self.client_address = addr_2
        print("this is addr_2 ", addr_2)
        self.setblocking(False)
        print("accept finish")
        print(time.time())
        print(self.seq, self.seq_ack, "this is seq and seq ack")
        return self, self.getsockname()

        # receive syn ; send syn, ack; receive ack

        # your code here

    def close(self):
        # send fin; receive ack; receive fin; send ack
        # your code here
        if self.client:
            need_sec_true: bool = True
            self.send("")
            while True:
                time.sleep(0.1)
                print("run in one")
                self.sendto(produce_packets(header_format, FIN_bit,
                                            self.seq, self.seq_ack), self.client_address)
                try:
                    header_2, useless_address = self.recvfrom(header_length, )
                except BlockingIOError:
                    print(1)
                    continue
                except TypeError:
                    print(2)
                    continue
                try:
                    header_2_unpack = struct.unpack(
                        header_format, header_2[0:header_length])
                except UnboundLocalError:
                    print(3)
                    continue
                except struct.error:
                    print(4)
                    continue
                if check_sum(header_2):
                    print(5)
                    continue
                if header_2_unpack[0] == ACK_bit and self.seq + 1 == header_2_unpack[2]:
                    break
                if header_2_unpack[0] == FIN_bit and self.seq == header_2_unpack[2]:
                    need_sec_true = False
                    break
            willbe_full: int = -1
            while True and need_sec_true:
                time.sleep(0.1)
                print("run in two")
                try:
                    header_3, useless_address = self.recvfrom(header_length, )
                except BlockingIOError:
                    print(1)
                    continue
                except TypeError:
                    print(2)
                    continue
                try:
                    header_3_unpack = struct.unpack(
                        header_format, header_3[0:header_length])
                except UnboundLocalError:
                    print(3)
                    continue
                except struct.error:
                    print(4)
                    continue
                if check_sum(header_3):
                    print(5)
                    continue
                if header_3_unpack[0] == FIN_bit and self.seq == header_3_unpack[2]:
                    willbe_full = header_3_unpack[1] + 1
                    break
            for i in range(0, 100, 1):
                self.sendto(produce_packets(header_format, FIN_bit,
                                            self.seq, willbe_full), self.client_address)
            print("{} {}".format(self.seq, self.seq_ack))
            time.sleep(1)
            print("Connect Close")
            super().close()
        else:
            for i in range(0, 10, 1):
                try:
                    data_uesless, addr_uesless = self.recvfrom(204800, )
                except BlockingIOError:
                    pass
                except TypeError:
                    pass
            print("server begin close")
            while True:
                time.sleep(0.01)
                print("run in three")
                try:
                    header_1, useles_address_2 = self.recvfrom(header_length, )
                except BlockingIOError:
                    print(1)
                    continue
                except TypeError:
                    print(2)
                    continue
                try:
                    header_1_unpack = struct.unpack(
                        header_format, header_1[0:header_length])
                except UnboundLocalError:
                    print(3)
                    continue
                if check_sum(header_1):
                    print(header_1_unpack)
                    print(4)
                    continue
                if header_1_unpack[0] == FIN_bit:
                    for i in range(0, 100, 1):
                        self.sendto(produce_packets(
                            header_format, ACK_bit, header_1_unpack[2], header_1_unpack[1] + 1), self.client_address)
                    break
                else:
                    print(header_1_unpack)
            time.sleep(1)
            while True:
                time.sleep(0.01)
                print("run in four")
                self.sendto(produce_packets(header_format, ACK_bit,
                                            header_1_unpack[2], header_1_unpack[1] + 1), self.client_address)
                self.sendto(produce_packets(header_format, FIN_bit,
                                            self.seq, header_1_unpack[1]), self.client_address)
                try:
                    header_2, useles_address_3 = self.recvfrom(header_length, )
                except BlockingIOError:
                    pass
                except TypeError:
                    pass
                try:
                    header_2_unpack = struct.unpack(
                        header_format, header_2[0:header_length])
                except UnboundLocalError:
                    pass
                except struct.error:
                    pass
                if check_sum(header_2):
                    continue
                if header_2_unpack[0] == FIN_bit and header_2_unpack[2] == self.seq + 1:
                    break
            time.sleep(1)
            self.seq = 0
            self.seq_ack = 0
            print("Connect Close")
        return

    def recv(self, buffersize: int = data_length):
        print("data in")
        try:
            data_uesless, addr_uesless = self.recvfrom(buffersize, )
        except BlockingIOError:
            pass
        except TypeError:
            pass
        temp_seq: int = self.seq
        temp_ack: int = self.seq_ack
        data_willsend: str = ""
        count: int = 0
        while True:
            print("now count is {}".format(str(count)))
            time.sleep(0.000001)
            try:
                data, addr = self.recvfrom(buffersize, )
            except BlockingIOError:
                print("dont recieve")
                continue
            except TypeError:
                print("Type Error")
                continue
            if check_sum(data):
                print("Wrong packet")
                continue
            data_header = struct.unpack(header_format, data[0:header_length])
            try:
                datas = str(struct.unpack("{}s".format(
                    str(data_header[3])), data[header_length:])[0].decode(data_format))
            except UnicodeDecodeError:
                continue
            except struct.error:
                continue
            if datas == "" and self.accept_null:
                continue
            else:
                print("this time recieve {}".format(datas))
            self.segment = data_header[0]
            print(check_sum(data), data_header[1]
                  == temp_ack, data_header[1], temp_ack)
            if not check_sum(data) and data_header[1] == temp_ack:
                count += 1
                data_willsend += datas
                header_send = produce_packets(
                    header_format, self.segment, temp_seq, temp_ack)
                print(header_send)
                for i in range(0, 10, 1):
                    self.sendto(header_send, self.client_address)
                temp_ack += len(datas)
            if self.segment == count:
                break
        for i in range(0, 100, 1):
            self.sendto(produce_packets(header_format, self.segment,
                                        temp_seq, temp_ack - len(datas)), self.client_address)
            time.sleep(0.01)
        print("recieve finish")
        self.seq_ack = temp_ack
        print(self.seq, self.seq_ack)
        self.accept_null = False
        return data_willsend

    def send(self, data):
        try:
            print(data, self.client_address)
        except AttributeError:
            print(data, " without client_address")
        try:
            data_uesless, addr_uesless = self.recvfrom(204800, )
        except BlockingIOError:
            pass
        except TypeError:
            pass
        length_of_data = len(data)
        packet_number = length_of_data // udp_packet_length + \
            (length_of_data % udp_packet_length != 0)
        packet_list = []
        temp_seq = self.seq
        temp_ack = self.seq_ack
        # accept_list = [False] * len(packet_list)
        seq_list = []
        print("packet number is {}".format(str(packet_number)))
        for i in range(0, packet_number - 1, 1):
            print("length is {} {} {}".format(
                len(data), str(temp_seq - 1), str(temp_seq + 499)))
            packet_list.append(produce_packets(
                header_format, packet_number, temp_seq, temp_ack, data[temp_seq - 1:temp_seq + 499]))
            print("{} was packetd".format(data[temp_seq - 1:temp_seq + 499]))
            seq_list.append(temp_seq)
            temp_seq += 500
            print(temp_seq)
        seq_list.append(temp_seq)
        packet_list.append(produce_packets(
            header_format, packet_number, temp_seq, temp_ack, data[temp_seq - 1:]))
        orders = []
        for i in range(1, (packet_number // 10) + 1, 1):
            orders.append(i * 10)
        if packet_number % 10 != 0:
            orders.append(packet_number)
        if len(orders) == 0:
            orders.append(0)
        print("{} was packetd".format(data[temp_seq - 1:]))
        # temp_seq = 1
        # temp_ack = 1
        print(len(packet_list))
        count = 0
        while True:
            i = count
            print("{} {} ".format(i, count))
            print("this time begin in {}".format(i))
            # while i < packet_number:
            while i < min(orders[count // 10] + 3, packet_number):
                time.sleep(0.01)
                print("run in {}".format(str(i)))
                self.sendto(packet_list[max(0, i - 1)], self.client_address)
                self.sendto(packet_list[i], self.client_address)
                self.sendto(
                    packet_list[min(i + 1, packet_number - 1)], self.client_address)
                try:
                    data_ack, useless_address = self.recvfrom(header_length, )
                except BlockingIOError:
                    i += 1
                    continue
                except TypeError:
                    i += 1
                    continue
                except OSError:
                    continue
                try:
                    data_ack_header = struct.unpack(
                        header_format, data_ack[0:header_length])
                except UnboundLocalError:
                    i += 1
                    continue
                print(data_ack)

                pre_count = -1
                for j in range(0, packet_number, 1):
                    if data_ack_header[2] == seq_list[j] and data_ack_header[0] == packet_number:
                        pre_count = j + 1
                        break
                print(check_sum(data_ack), count < pre_count,
                      data_ack_header[0] == packet_number)
                if not check_sum(data_ack) and count < pre_count:
                    count = pre_count

                """
                if not check_sum(data_ack) and data_ack_header[2] == seq_list[count] and data_ack_header[0] == packet_number:
                    count += 1
                """
                i += 1

            if count == packet_number:
                print("break out!")
                break
            time.sleep(1)
        self.seq += length_of_data
        print("send message finish")
        print(self.seq, self.seq_ack)
        return


def produce_packets(formats: str, bits: int, seq: int, seq_ack: int, data_str: str = "") -> bytes:
    data_bytes: [str, bytes] = data_str
    try:
        data_bytes = bytes(data_str.encode(data_format))
    except AttributeError:
        pass
    except UnicodeEncodeError:
        pass
    print(bits, seq, seq_ack, len(data_str))
    header: bytes = struct.pack(formats, bits, seq, seq_ack, len(data_str), 0)
    header += data_bytes
    check_data: int = check_sum(header)
    willreturn: bytes = struct.pack(formats, bits, seq, seq_ack,
                                    len(data_str), 256 - check_data)
    willreturn += data_bytes
    return willreturn


def get_control(control: int) -> int:
    return (
        control & 0x01,
        (control & 0x02) >> 1,
        (control & 0x04) >> 2,
    )


def get_random() -> int:
    return (int)((2 ** 29 - 1) * random.random())


def check_sum(data: bytes) -> int:
    sum: int = 0
    for byte in data:
        sum += byte
    sum = -(sum % 256)
    return sum & 0xFF
