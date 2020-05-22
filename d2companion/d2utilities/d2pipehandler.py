# -*- coding: utf-8 -*-

import json
import struct
import win32file
from ctypes import sizeof, c_int


class D2PipeHandler:
    def __init__(self):
        self.pipe_name = r'\\.\pipe\DiabloInterfacePipe'
        self.c_int_size = sizeof(c_int)
        self.buffer_size = 1024
        
    def _construct_query(self, json_dict):
        s = json.dumps(json_dict).encode("utf-8")
        return struct.pack("i%ds" % (len(s),), len(s), s)
    
    def _pipe_send(self, query):
        request = self._construct_query(query)
        handle = win32file.CreateFile(self.pipe_name, win32file.GENERIC_READ|win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, None)
        win32file.WriteFile(handle, request)
        
        response = win32file.ReadFile(handle, self.buffer_size)[1]
        length = struct.unpack('i', response[:self.c_int_size])[0]

        while len(response) < length + self.c_int_size:
            response += win32file.ReadFile(handle, self.buffer_size)[1]
            win32file.CloseHandle(handle)

        data = json.loads(response[self.c_int_size:], encoding='utf-8')
        return data
    
    def get_item(self, slot):
        '''possible slots:
            'helm','armor','amulet', 'rings', 'belt', 'gloves', 'boots',
            'weapon', 'shield', 'weapon2', 'shield2' '''
        response = self._pipe_send({'EquipmentSlot': slot})
        return response
    
    def get_attribute(self, attribute):
        '''possible attributes:
            ??? --> check for syntax!!!'''
        response = self._pipe_send({'request': attribute})
        return response