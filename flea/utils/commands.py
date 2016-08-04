import json


class Command(object):
    DELIMITER = '##FLEA##'
    DELIMITER_BYTES = DELIMITER.encode()

    def __init__(self, name, data=None):
        # validate data's json serializability
        json.dumps(data)
        self._name = name
        self._data = data

    def __eq__(self, x):
        return self.data == x.data

    def __hash__(self):
        return hash(self.serialized)
    
    def __str__(self):
        return '{}: {}'.format(self.name, self.data)

    def __repr__(self):
        return str(self)

    @classmethod
    def parse(cls, input_bytes):
        assert(input_bytes.endswith(cls.DELIMITER_BYTES)),\
            'Given bytes does not ends with required delimiter. Given: {}'\
            .format(input_bytes)

        raw_str = input_bytes.replace(cls.DELIMITER_BYTES, b'').decode()
        raw_json = json.loads(raw_str)

        if not all([k in raw_json for k in ['name', 'data']]):
            raise ValueError(
                'Invalid command message JSON: {}'.format(raw_json)
            )

        return cls(raw_json['name'], raw_json['data'])

    def encode(self):
        return (json.dumps({'name': self.name, 'data': self.data}) + 
                self.DELIMITER).encode()

    @property
    def name(self):
        return self._name

    @property
    def data(self):
        return self._data

    @property
    def serialized_data(self):
        return json.dumps(self.data)

    @property
    def serialized(self):
        return json.dumps({'name': self.name, 'data': self.data})
