def define_property(self, name, value=None, readable=True, writable=True):
    # "_User__name" のような name mangling 後の名前.
    field_name = "_{}__{}".format(self.__class__.__name__, name)

    # 初期値を設定する.
    setattr(self, field_name, value)

    # getter/setter を生成し, プロパティを定義する.
    getter = (lambda self: getattr(self, field_name)) if readable else None
    setter = (lambda self, value: setattr(
        self, field_name, value)) if writable else None
    setattr(self.__class__, name, property(getter, setter))
