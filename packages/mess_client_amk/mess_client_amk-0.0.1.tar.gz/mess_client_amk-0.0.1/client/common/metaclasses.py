import dis


class ClientVerifier(type):
    """
    Метакласс, проверяющий, что в результирующем классе нет серверных
    вызовов, таких как: accept, listen. Также проверяется, что сокет не
    создаётся внутри конструктора класса.
    """
    def __init__(self, cls_name, bases, cls_dict):
        methods = []
        for func in cls_dict:
            try:
                instrs = dis.get_instructions(cls_dict[func])
            except TypeError:
                pass
            else:
                for instr in instrs:
                    print(instr)
                    if instr.opname == 'LOAD_GLOBAL':
                        if instr.argval not in methods:
                            methods.append(instr.argval)
            print(methods)

        if 'accept' in methods or 'listen' in methods or 'socket' in methods:
            raise TypeError(f'В классе используется запрещенный метод {i.argval}')
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют функции, работающие с сокетами')

        super().__init__(cls_name, bases, cls_dict)


class ServerVerifier(type):
    """
    Метакласс, проверяющий, что в результирующем классе нет клиентских
    вызовов, таких как: connect. Также проверяется, что серверный
    сокет является TCP и работает по IPv4 протоколу.
    """
    def __init__(self, cls_name, bases, cls_dict):
        methods = []
        attrs = []

        for func in cls_dict:
            try:
                instrs = dis.get_instructions(cls_dict[func])
            except TypeError:
                pass
            else:
                for instr in instrs:
                    if instr.opname == 'LOAD_GLOBAL':
                        if instr.argval not in methods:
                            methods.append(instr.argval)
                    if instr.opname == 'LOAD_ATTR':
                        if instr.argval not in attrs:
                            attrs.append(instr.argval)
        if 'connect' in methods:
            raise TypeError('Использование метода "connect" недопустимо в серверном классе')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета')

        super().__init__(cls_name, bases, cls_dict)