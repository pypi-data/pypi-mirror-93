from dfx_utils.helper import json_friendly_dumps


class SuperDict:
    """
    data = SuperDict()
    data['a.b'] = 1 => {'a': {'b': 1}}
    """

    def __init__(self, _dict: dict = None, _sep='.'):
        self._sep = _sep
        self._dict = _dict or {}

    def __getitem__(self, item):
        tmp_data = None
        if self._sep in item:
            tmp_dict = self._dict
            for key in item.split(self._sep):
                tmp_data = tmp_dict.get(key)
                if tmp_data is not None:
                    if tmp_data and isinstance(tmp_data, dict):
                        tmp_dict = tmp_data
        else:
            tmp_data = self._dict.get(item)
        return SuperDict(tmp_data) if isinstance(tmp_data, dict) else tmp_data

    def __setitem__(self, key, value):
        if self._sep in key:
            tmp_dict = self._dict
            keys = key.split(self._sep)
            for idx, item in enumerate(keys):
                if idx == len(keys) - 1:
                    tmp_dict[item] = value
                else:
                    tmp_dict[item] = tmp_dict.get(item, {})
                    tmp_dict = tmp_dict[item]
        else:
            self._dict[key] = value

    def __getattribute__(self, item):
        """ 当调用的函数不存在时，去self._dict里面找 """
        try:
            return super(SuperDict, self).__getattribute__(item)
        except AttributeError:
            return self._dict.__getattribute__(item)

    def __str__(self):
        return json_friendly_dumps(self._dict)

    def clear(self):
        self._dict = {}

    def get(self, item, default=None):
        ret_data = self.__getitem__(item)
        return ret_data if ret_data is not None else default


class FieldContainer(object):
    """ 数据容器 """

    def __init__(self, **kwargs):
        if kwargs:
            self(**kwargs)

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except:
            return None

    def __call__(self, *args, **kwargs):
        for name, val in kwargs.items():
            setattr(self, name, val)


class BaseData:
    def __init__(self, **kwargs):
        self.__dumps = dict()
        self.__container = FieldContainer(**kwargs)

    def __getattribute__(self, item):
        try:
            return super(BaseData, self).__getattribute__(item)
        except:
            return self.__container.__getattribute__(item)

    def __call__(self, force=True):
        if not force and self.__dumps:
            return self.__dumps

        self.__dumps = dict()
        for name in dir(self.__container):
            if not name.startswith('__'):
                self.__dumps[name] = getattr(self.__container, name)
        return self.__dumps

    def add(self, **kwargs):
        self.__container(**kwargs)
