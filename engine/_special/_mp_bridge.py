from .._constants.multiprocessing import COMMANDS_SEPARATOR, ARGS_SEPARATOR
from ._buffer import Buffer


class ProcessBridge:
    __slots__ = ('_input', '_output', '_wr_buffer', '_encoding', '_c_sep', '_a_sep', '_enc_data_only')

    def __init__(self, inp, out, encoding):
        self._input = inp
        self._output = out
        self._wr_buffer = Buffer(64)
        self._enc_data_only = True
        self._encoding = encoding
        self._c_sep = COMMANDS_SEPARATOR.encode(encoding)
        self._a_sep = ARGS_SEPARATOR.encode(encoding)

    def _build_msg(self):
        if self._enc_data_only:
            return b''.join(self._wr_buffer.buffer())
        msg = []
        oneline = True
        bytes_last = False

        for arg in self._wr_buffer.buffer():
            if isinstance(arg, bytes):
                if bytes_last:
                    msg[-1] = msg[-1] + arg
                else:
                    msg.append(arg)
                bytes_last = True
                continue
            else:
                oneline = bytes_last = False
            msg.append(arg)

        return msg[0] if oneline else tuple(msg)

    def _decode_msg(self):
        data = self._input.recv()
        c_sep = self._c_sep
        enc = self._encoding
        cm_splitter = self._decode_cm

        if isinstance(data, bytes):
            return [tuple(cm_splitter(cm.decode(enc))) for cm in data.split(c_sep) if len(cm) > 0]

        cm_list = [[]]
        for v in data:
            if isinstance(v, bytes):
                commands = v.split(c_sep)
                if len(commands) > 1:
                    for cm in commands:
                        if len(cm) > 0:
                            cm_list[-1].extend(cm_splitter(cm.decode(enc)))
                            cm_list.append([])
                else:
                    cm_list[-1].extend(cm_splitter(v.decode(enc)))
            else:
                cm_list[-1].append(v)
        return cm_list

    def _decode_cm(self, command: str):
        a_sep = self._a_sep.decode(self._encoding)
        return (i for i in command.split(a_sep) if len(i) > 0)

    def _reset_buffer(self):
        if not self._wr_buffer.empty():
            self._output.send(self._build_msg())
            self._enc_data_only = True

    def tr_end(self):
        self._reset_buffer()

    def send(self, command, *args, tr_end=False):
        enc = self._encoding
        args_sep = self._a_sep
        buffer = self._wr_buffer
        
        if len(buffer) + len(args) * 2 + 2 > buffer.size():
            buffer.expand()

        buffer.push(command.encode(enc))
        buffer.push(args_sep)

        for a in args:
            args_sep_flag = True
            if isinstance(a, str):
                buffer.push(a.encode(enc))
            elif isinstance(a, int):
                buffer.push(str(a).encode(enc))
            elif isinstance(a, float):
                buffer.push(f'{a:.16f}'.encode(enc))
            else:
                self._enc_data_only = False
                buffer.push(a)
                args_sep_flag = False
            if args_sep_flag:
                buffer.push(args_sep)

        buffer.push(self._c_sep)
        if tr_end:
            self._reset_buffer()

    def read(self):
        if self._input.poll():
            return self._decode_msg()
        return []

    def read_all(self):
        while self._input.poll():
            yield self._decode_msg()
