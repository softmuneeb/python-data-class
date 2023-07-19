class Data:
    DEFAULT_VALUE = 100

    def __init__(self, **kwargs):
        self._data = {
            "id": "",
            "name": "",
            "metadata": {
                "system": {},
                "user": {}
            }
        }
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_dict(cls, data_dict):
        instance = cls()
        instance._data = data_dict
        return instance

    def to_dict(self):
        return self._data

    def __getattr__(self, attr):
        # Check root level first
        if attr in self._data:
            return self._data[attr]

        # Check metadata -> system level
        if attr in self._data['metadata']['system']:
            return self._data['metadata']['system'][attr]

        # Check metadata -> user level
        if attr in self._data['metadata']['user']:
            return self._data['metadata']['user'][attr]

        # If not found, set default value in metadata -> system
        self._data['metadata']['system'][attr] = self.DEFAULT_VALUE
        return self.DEFAULT_VALUE

    def __setattr__(self, attr, value):
        # To avoid recursive setting and stack overflow
        if attr == "_data":
            self.__dict__['_data'] = value
            return
        if attr in self._data:
            self._data[attr] = value
            return

        # For now, default to storing extra attributes in metadata -> system
        self._data['metadata']['system'][attr] = value

    def __dir__(self):
        return list(self._data.keys()) + list(self._data['metadata']['system'].keys()) + list(self._data['metadata']['user'].keys())


data = {
    "id": "1",
    "name": "first",
    "metadata": {
        "system": {
            "size": 10.7
        },
        "user": {
            "batch": 10
        }
    }
}

# load from dict
my_inst_1 = Data.from_dict(data)

# load from inputs
my_inst_2 = Data(name="my")

# reflect inner value
print(my_inst_1.size)  # should print 10.7
# print(my_inst_1.batch)  # should print 10
# print(my_inst_1.name)  # should print first

# default values
# should print 100 and should set a default value of 100 in metadata.system.height
print(my_inst_1.height)
# print(my_inst_1.way)  # should print 100 and should set a default value of 100 in the metadata.system.way
# print(my_inst_1.anything)  # should print 100 and should set a default value of 100 in metadata.system.anything

print(my_inst_1.to_dict()['metadata']['system']['height'])  # should print the default value

# autocomplete - should complete to data.metadata
# print(data.me)
# print(my_inst_1.metadata)
