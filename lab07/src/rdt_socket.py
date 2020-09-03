#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds/CS305_2019F_Remake
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-07-03 13:08:19
LastEditors: nanoseeds
LastEditTime: 2020-08-08 22:54:28
"""
""" CS305_2019F_Remake 
    Copyright (C) 2020  nanoseeds

    CS305_2019F_Remake is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    CS305_2019F_Remake is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import time
from typing import List

from lab07.src.config import *
from lab07.src.rdt_body import rdt_body
from lab07.src.rdt_header import rdt_header
from lab07.src.udp_socket import UDPsocket

data_length: int = 520

SYN_bit: int = (1 << 0)
FIN_bit: int = (1 << 1)
ACK_bit: int = (1 << 2)
Reset_bit: int = (1 << 3)
udp_packet_length: int = 500
begin_bytes: bytes = b'0' * 20


class rdt_socket(UDPsocket):
    def __init__(self):
        super().__init__()
        self.begin_time: float = time.time()
        self.setblocking(False)
        self.seq_num: int = 0
        self.ack_num: int = 0
        self.accept_null: bool = True
        self.client: bool = True
        self.header_format: str = header_format  # 5个 每个4bytes, 8bits per byte
        self.target_address: Tuple[str, int]

    def sendto(self, data: bytes, *args: address_tuple) -> int:
        self.setblocking(False)
        if len(args) == 0:
            return super().sendto(data, self.target_address)
        elif len(args) == 1:
            assert len(args[0]) == 2
            assert isinstance(args[0][0], str)
            assert isinstance(args[0][1], int)
            return super().sendto(data, args[0])
        else:
            return -1

    # Done
    def connect(self, address: Tuple[str, int]) -> None:
        self.setblocking(False)
        self.target_address = address
        header_1: rdt_header = rdt_header(SYN_bit, self.seq_num, self.ack_num)
        header_2: rdt_header
        while True:
            self.sendto(header_1.to_bytes())
            print("send syn finish")
            time.sleep(1)
            data: bytes = begin_bytes
            try:
                data, addr_1 = self.recvfrom(data_length, )
            except (BlockingIOError, TypeError) as e:
                time.sleep(1)
                continue
            header_2 = rdt_header.unpack(data)
            if check_sum(data) == 0 and header_2.equal(bits=SYN_bit + ACK_bit, ack_num=self.seq_num + 1):
                print("recieve syn ack finish")
                break
            else:
                time.sleep(1)
                print("header 2 is not ok")
        # done in here
        print("jump out")
        self.seq_num += 1
        self.ack_num = header_2.seq_num + 1
        header_3: rdt_header = rdt_header(ACK_bit, self.seq_num, self.ack_num)
        for i in range(3):
            self.sendto(header_3.to_bytes())
        # 这个包丢了实际上没问题,server可以通过正文来判断
        print(time.time() - self.begin_time, "finish first stege")
        print(self.seq_num, self.ack_num, "this is seq and seq ack of connect finish")

    # Done
    def accept(self) -> Tuple['rdt_socket', Tuple[str, int]]:
        """
        相当于这玩意的作用是
        socket本身接受一个socket,然后new一个socket with recieve 地址返回.
        """
        # receive syn ; send syn, ack; receive ack
        self.client = False
        self.setblocking(True)
        header_1: rdt_header
        header_2: rdt_header
        header_3: rdt_header
        while True:
            self.setblocking(True)
            try:
                data: bytes
                addr: Tuple[str, int]
                data, self.target_address = self.recvfrom(data_length, )
            except TypeError as e:
                print("line 112")
                continue
            print("recieve syn data")
            self.setblocking(False)
            header_1 = rdt_header.unpack(data)
            if check_sum(data) == 0:
                if header_1.equal(bits=SYN_bit):
                    self.ack_num = header_1.seq_num + 1
                    header_2: rdt_header = rdt_header(bits=SYN_bit + ACK_bit, seq_num=self.seq_num,
                                                      ack_num=self.ack_num)
                    self.sendto(header_2.to_bytes())
                    print("send syn,ack finish")
                    break
            else:
                print("line 120")
        while True:
            time.sleep(1)
            data: bytes = begin_bytes
            try:
                data, addr_2 = self.recvfrom(data_length, )
            except (BlockingIOError, TypeError) as e:
                time.sleep(1)
            header_3: rdt_header = rdt_header.unpack(data)
            print(header_3, check_sum(data), "can it jump out?")
            if check_sum(data) == 0 and header_3.equal(bits=ACK_bit, ack_num=self.seq_num + 1):
                break
            self.sendto(header_2.to_bytes())
        print(header_3.bits, header_3.ack_num, self.seq_num + 1)
        self.seq_num += 1
        print("this is addr_2 ", addr_2)
        print(time.time() - self.begin_time)
        print(self.seq_num, self.ack_num, "this is seq and seq ack of accept finish")
        return self, self.getsockname()

    # Done
    def close(self) -> None:
        self.setblocking(False)
        if self.client:
            try:
                self.close_client()
            except ConnectionResetError:
                return
        else:
            self.close_server()
        # send fin; receive ack; receive fin; send ack
        # your code here

    # Done
    def close_client(self) -> None:
        self.setblocking(False)
        self.clear_buffer()
        self.send("")
        header_1: rdt_header
        header_2: rdt_header
        while True:
            time.sleep(0.1)
            print("run in one")
            header_1 = rdt_header(FIN_bit, self.seq_num, self.ack_num)
            self.sendto(header_1.to_bytes())
            try:
                data, addr = self.recvfrom(data_length, )
            except (BlockingIOError, TypeError) as e:
                print(e)
                # traceback.print_exc()
                continue
            try:
                header_2 = rdt_header.unpack(data)
            except (UnboundLocalError, struct.error) as e:
                print(e)
                traceback.print_exc()
                continue
            if check_sum(data) == 0 and header_2.equal(bits=ACK_bit, ack_num=self.seq_num + 1) or \
                    header_2.equal(bits=FIN_bit + ACK_bit, ack_num=self.seq_num + 1):
                break
        while True:
            print("client close stage 3")
            self.sendto(rdt_header(ACK_bit, self.seq_num + 1, header_2.seq_num + 1).to_bytes())
            self.clear_buffer()
            print("client close stage buffer clear")
            time.sleep(2)
            try:
                data_3, _useless_ = self.recvfrom(data_length, )
            except (BlockingIOError, ConnectionResetError):
                break
        print("{} {}".format(self.seq_num, self.ack_num))
        time.sleep(1)
        print("Connect Close")
        super().close()

    # Done
    def close_server(self) -> None:
        self.clear_buffer()
        print("server begin close")
        header_1: rdt_header
        header_2: rdt_header
        while True:
            time.sleep(0.01)
            print("run in three")
            try:
                data, _uesless_ = self.recvfrom(data_length, )
            except (BlockingIOError, TypeError) as e:
                pass
            try:
                header_1: rdt_header = rdt_header.unpack(data)
            except UnboundLocalError:
                print(3)
                continue
            if header_1.equal(bits=FIN_bit) and check_sum(data) == 0:
                self.sendto(rdt_header(ACK_bit, self.seq_num, header_1.seq_num + 1).to_bytes())
                self.sendto(rdt_header(FIN_bit + ACK_bit, self.seq_num, header_1.seq_num + 1).to_bytes())
                break
            else:
                print(header_1)
        while True:
            time.sleep(1)
            print("run in four")
            self.sendto(rdt_header(ACK_bit, self.seq_num, header_1.seq_num + 1).to_bytes())
            self.sendto(rdt_header(FIN_bit, self.seq_num, header_1.seq_num + 1).to_bytes())
            try:
                data_4, _useless_ = self.recvfrom(data_length, )
            except (BlockingIOError, TypeError) as e:
                print(e)
                traceback.print_exc()
            try:
                header_4: rdt_header = rdt_header.unpack(data_4)
            except (UnboundLocalError, struct.error) as e:
                print(e)
            if check_sum(data_4) == 0 and header_4.equal(bits=ACK_bit, ack_num=self.seq_num + 1):
                break
        time.sleep(1)
        self.seq_num = 0
        self.ack_num = 0
        print("Connect Close")

    # TODO 写关于握手,分手丢包的文档
    # TODO 写recv send sendall 以及内在的send_packet 函数
    def recv(self, buffersize: int = data_length):
        print("data in")
        self.clear_buffer()
        temp_seq: int = self.seq_num
        temp_ack: int = self.ack_num
        data_willsend: str = ""
        count: int = 0
        while True:
            print("now count is {}".format(str(count)))
            time.sleep(0.0005)
            try:
                data, addr = self.recvfrom(buffersize, )
            except (BlockingIOError, TypeError) as e:
                traceback.print_exc()
                print(e)
                continue
            if check_sum(data) != 0:
                print("Wrong packet")
                continue
            data_header = struct.unpack(header_format, data[0:header_length])
            try:
                datas = str(struct.unpack("{}s".format(
                    str(data_header[3])), data[header_length:])[0].decode(data_format))
            except (BlockingIOError, struct.error) as e:
                traceback.print_exc()
                print(e)
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
                    self.sendto(header_send)
                temp_ack += len(datas)
            if self.segment == count:
                break
        for i in range(0, 100, 1):
            self.sendto(produce_packets(header_format, self.segment,
                                        temp_seq, temp_ack - len(datas)))
            time.sleep(0.01)
        print("recieve finish")
        self.ack_num = temp_ack
        print(self.seq_num, self.ack_num)
        self.accept_null = False
        return data_willsend

    def send(self, data: str):
        self.clear_buffer()
        length_of_data = len(data)
        packet_number = length_of_data // udp_packet_length + \
                        (length_of_data % udp_packet_length != 0)
        packet_list = []
        temp_seq: int = self.seq_num
        temp_ack: int = self.ack_num
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
                self.sendto(packet_list[max(0, i - 1)])
                self.sendto(packet_list[i])
                self.sendto(
                    packet_list[min(i + 1, packet_number - 1)])
                try:
                    data_ack, useless_address = self.recvfrom(header_length, )
                except (BlockingIOError, TypeError, OSError):
                    i += 1
                    continue
                try:
                    data_ack_header = struct.unpack(header_format, data_ack[0:header_length])
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
                i += 1
            if count == packet_number:
                print("break out!")
                break
            time.sleep(1)
        self.seq_num += length_of_data
        print("send message finish")
        print(self.seq_num, self.ack_num)
        return

    def sendall(self, data: bytes, flags: int = ...) -> None:
        self.setblocking(False)
        length_of_data: int = len(data)
        packet_enough: int = length_of_data // udp_packet_length  # 长度满500的包的数量
        packet_less: bool = length_of_data % udp_packet_length > 0  # 是否有小段残余
        # x*500+1 -> (x+1)*499 都是(x,1)
        # (x+1)*500  (x+1,0)
        package_list: List[rdt_body] = []
        for i in range(0, packet_enough):
            package_list.append(
                rdt_body(ACK_bit, self.seq_num + i * udp_packet_length, 1,
                         data[i * udp_packet_length:(i + 1) * udp_packet_length]))
        if packet_less is True:
            package_list.append(rdt_body(ACK_bit, self.seq_num + len(package_list) * udp_packet_length,
                                         1, data[(len(package_list)) * udp_packet_length:]))
        count: int = 0
        print("length of list is {}".format(str(len(package_list))))
        while True:
            time.sleep(0.1)
            for i in range(0, 20):
                will_use = min(count + i, len(package_list) - 1)
                print("{} send finish,count is {},seq is {}".format(str(will_use), str(count),
                                                                    str(package_list[will_use].seq_num)))
                self.sendto(package_list[will_use].to_bytes())
            # 发了20个包,接下来收20个包
            for i in range(0, 20):
                data_2: bytes = begin_bytes
                try:
                    data_2, _uesless = self.recvfrom(data_length, )
                except (BlockingIOError, TypeError, OSError) as e:
                    print(e)
                try:
                    body = rdt_body.unpack(data_2)
                except (UnboundLocalError, struct.error, TypeError) as e:
                    print(e)
                if check_sum(data_2) == 0 and body.equal(bits=ACK_bit):
                    if body.ack_num // udp_packet_length > count:
                        count = body.ack_num // udp_packet_length
                    elif body.ack_num // udp_packet_length + 20 <= count:
                        count -= body.ack_num // udp_packet_length
                    elif body.ack_num - 1 > count * udp_packet_length:
                        count = body.ack_num // udp_packet_length + 1

            if count == len(package_list):
                return

    def recvall(self) -> str:
        data_willreturn: str = ""
        count: int = 0
        while True:
            print("count is {}".format(str(count)))
            print("length of receive is {}".format(len(data_willreturn)))
            time.sleep(0.01)
            try:
                data, addr = self.recvfrom(data_length, )
            except (BlockingIOError, TypeError) as e:
                traceback.print_exc()
                continue
            if len(data) == 0:
                continue
            try:
                body: rdt_body = rdt_body.unpack(data)
            except (BlockingIOError, struct.error) as e:
                traceback.print_exc()
                continue
            print("{} is body.seq_num".format(str(body.seq_num)))
            if check_sum(data) == 0 and len(data) > header_length and body.equal(bits=ACK_bit) \
                    and body.seq_num // udp_packet_length == count:
                count += 1
                self.ack_num += body.length
                self.sendto(rdt_header(ACK_bit, self.seq_num, body.seq_num).to_bytes())
                try:
                    data_willreturn += body.data_bytes.decode(encoding='utf-8')
                except UnicodeEncodeError:
                    pass
            else:
                self.sendto(rdt_header(ACK_bit, self.seq_num, self.ack_num).to_bytes())
                print("Wrong packet")
            if check_sum(data) == 0 and body.equal(bits=ACK_bit) is False:
                break
        return data_willreturn

    def listen(self, __backlog: int = ...) -> None:
        # 装个样子,什么也不干
        pass

    def clear_buffer(self):
        print("begin clear buffer")
        while True:
            try:
                _ = self.recvfrom(data_length, )
            except BlockingIOError:
                return


def main():
    pass


if __name__ == "__main__":
    main()
