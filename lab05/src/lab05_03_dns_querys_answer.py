#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-22 23:40:31 
@LastEditors  : nanoseeds
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

from lab05.src.lab05_03_dns_querys import dns_querys
from lab05.src.lab05_03_helper_functions import *


class dns_querys_answer(object):
    def __init__(self, response: bytes):
        """
        首先呢,为了信息压缩,使用指针的方式来重复利用域名,
        Name部分有两种可能,一是两个八位数组,其中第一个八位数组的前两个value == 11
        第二个是传统的{Number (几个八位数组表示的字符) } * n +00(第二种情况还有可能在末尾有一个情况1).
        Type,class仍为两个八位数组
        TTL:四个八位数组,代表时间间隔
        RDLENGTH:预示接下来的RDATA长度,两个八位数组.
        RDATA:RDLENGTH个八位数组,其中的具体表现形式,还可以为嵌套的方式,即其中的最后一部分被表示为指针.
        """
        self.HQ = dns_querys(response)
        self.answers_number = trans_bit_toint(self.HQ.header[6], self.HQ.header[7]) + \
                              trans_bit_toint(self.HQ.header[8], self.HQ.header[9])
        self.initime = int(time.time())
        self.ttl: List[Tuple[int, int]] = []
        self.ans_names: List[List[int]] = []
        self.ans_types: List[List[int]] = []
        self.ans_classes: List[List[int]] = []
        self.ans_ttls: List[List[int]] = []
        self.ans_rdlengths: List[List[int]] = []
        self.ans_rdatas: List[List[int]] = []
        pointer: int = 0
        times: int = 0
        while pointer < len(self.HQ.Answers) and times < self.answers_number:
            times += 1
            # 192 = 0xc0 = 0b11000000 = 128+64
            if self.HQ.Answers[pointer] == 0xc0:
                ans_name = self.HQ.Answers[pointer:pointer + 2]
                pointer += 2
            else:
                namelength = get_ques_domain_end(self.HQ.Answers[pointer:], 0)
                ans_name = self.HQ.Answers[pointer:pointer + namelength]
                # namelength = self.HQ.Answers[pointer:].index(0)
                # ans_name = self.HQ.Answers[pointer:pointer + namelength]
                pointer += namelength
            ans_type = self.HQ.Answers[pointer:pointer + 2]
            pointer += 2
            ans_class = self.HQ.Answers[pointer:pointer + 2]
            pointer += 2
            ans_ttl = self.HQ.Answers[pointer:pointer + 4]
            self.ttl.append((pointer, trans_bit_toint(
                trans_bit_toint(
                    self.HQ.Answers[pointer], self.HQ.Answers[pointer + 1]),
                trans_bit_toint(
                    self.HQ.Answers[pointer + 2], self.HQ.Answers[pointer + 3]),
                16)))
            pointer += 4
            ans_rdlength = self.HQ.Answers[pointer:pointer + 2]
            rd_length = trans_bit_toint(self.HQ.Answers[pointer], self.HQ.Answers[pointer + 1])
            pointer += 2
            ans_rdata = self.HQ.Answers[pointer:pointer + rd_length]
            pointer += rd_length
            print("this is the ans_name", ans_name)
            self.ans_names.append(ans_name)
            self.ans_types.append(ans_type)
            self.ans_classes.append(ans_class)
            self.ans_ttls.append(ans_ttl)
            self.ans_rdlengths.append(ans_rdlength)
            self.ans_rdatas.append(ans_rdata)
            print("this is the pointer", pointer,
                  " this is ANswers.length", len(self.HQ.Answers))

    def get_header_question_answers(self) -> bytes:
        """
        :return: 一个byte流,其中由这个responsex的各个部分组合而成
        """
        will_return: List[int] = self.HQ.get_querys_header_question()
        # print(will_return)
        for i in range(0, self.answers_number, 1):
            will_return += list_poly(self.ans_names[i], self.ans_types[i],
                                     self.ans_classes[i], self.ans_ttls[i],
                                     self.ans_rdlengths[i], self.ans_rdatas[i])
        #    print(will_return)
        return bytes(will_return)

    def get_min_ttl(self) -> Tuple[int, int]:
        will_return: Tuple[int, int] = (0x00110011, 0x3f3f3f3f)
        for i in self.ttl:
            if i[1] < will_return[1]:
                will_return = i
        return will_return

    def judge_is_out(self, live_time: int = 1024) -> bool:
        return time.time() - self.initime > min(self.get_min_ttl()[1], live_time)
