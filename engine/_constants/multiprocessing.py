__all__ = ['COMMANDS_SEPARATOR', 'ARGS_SEPARATOR', 'STARTUP', 'SHUTDOWN',
           'SET_CONFIG', 'LOAD_RESOURCES',
           'CREATE_CAMERA', 'CHANGE_CAMERA',
           'CLEAR', 'DRAW_SHAPE']


__CONST = object()

COMMANDS_SEPARATOR = __CONST
ARGS_SEPARATOR = __CONST
STARTUP = __CONST
STARTUP_ERROR = __CONST
SHUTDOWN = __CONST
SET_CONFIG = __CONST
LOAD_RESOURCES = __CONST
DRAW_SHAPE = __CONST
CLEAR = __CONST
CREATE_CAMERA = __CONST
CHANGE_CAMERA = __CONST


def __init(const):
    gl = globals()
    cnt = 0
    const_v = gl[const]

    for k, v in list(gl.items()):
        if k != const and v is const_v:
            gl[k] = bytes([cnt]).decode('utf-8')
            cnt += 1


__init('__CONST')
