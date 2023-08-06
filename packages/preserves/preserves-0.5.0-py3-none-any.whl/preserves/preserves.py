import sys
import numbers
import struct

try:
    basestring
except NameError:
    basestring = str

if isinstance(chr(123), bytes):
    _ord = ord
else:
    _ord = lambda x: x

class Float(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return 'Float(' + repr(self.value) + ')'

    def __preserve_on__(self, encoder):
        encoder.buffer.append(0x82)
        encoder.buffer.extend(struct.pack('>f', self.value))

class Symbol(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '#' + self.name

    def __preserve_on__(self, encoder):
        bs = self.name.encode('utf-8')
        encoder.buffer.append(0xb3)
        encoder.varint(len(bs))
        encoder.buffer.extend(bs)

class Record(object):
    def __init__(self, key, fields):
        self.key = key
        self.fields = tuple(fields)
        self.__hash = None

    def __eq__(self, other):
        return isinstance(other, Record) and (self.key, self.fields) == (other.key, other.fields)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if self.__hash is None:
            self.__hash = hash((self.key, self.fields))
        return self.__hash

    def __repr__(self):
        return str(self.key) + '(' + ', '.join((repr(f) for f in self.fields)) + ')'

    def __preserve_on__(self, encoder):
        encoder.buffer.append(0xb4)
        encoder.append(self.key)
        for f in self.fields:
            encoder.append(f)
        encoder.buffer.append(0x84)

    def __getitem__(self, index):
        return self.fields[index]

    @staticmethod
    def makeConstructor(labelSymbolText, fieldNames):
        return Record.makeBasicConstructor(Symbol(labelSymbolText), fieldNames)

    @staticmethod
    def makeBasicConstructor(label, fieldNames):
        if type(fieldNames) == str:
            fieldNames = fieldNames.split()
        arity = len(fieldNames)
        def ctor(*fields):
            if len(fields) != arity:
                raise Exception("Record: cannot instantiate %r expecting %d fields with %d fields"%(
                    label,
                    arity,
                    len(fields)))
            return Record(label, fields)
        ctor.constructorInfo = RecordConstructorInfo(label, arity)
        ctor.isClassOf = lambda v: \
                         isinstance(v, Record) and v.key == label and len(v.fields) == arity
        def ensureClassOf(v):
            if not ctor.isClassOf(v):
                raise TypeError("Record: expected %r/%d, got %r" % (label, arity, v))
            return v
        ctor.ensureClassOf = ensureClassOf
        for fieldIndex in range(len(fieldNames)):
            fieldName = fieldNames[fieldIndex]
            # Stupid python scoping bites again
            def getter(fieldIndex):
                return lambda v: ensureClassOf(v)[fieldIndex]
            setattr(ctor, '_' + fieldName, getter(fieldIndex))
        return ctor

class RecordConstructorInfo(object):
    def __init__(self, key, arity):
        self.key = key
        self.arity = arity

    def __eq__(self, other):
        return isinstance(other, RecordConstructorInfo) and \
            (self.key, self.arity) == (other.key, other.arity)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if self.__hash is None:
            self.__hash = hash((self.key, self.arity))
        return self.__hash

    def __repr__(self):
        return str(self.key) + '/' + str(self.arity)

# Blub blub blub
class ImmutableDict(dict):
    def __init__(self, *args, **kwargs):
        if hasattr(self, '__hash'): raise TypeError('Immutable')
        super(ImmutableDict, self).__init__(*args, **kwargs)
        self.__hash = None

    def __delitem__(self, key): raise TypeError('Immutable')
    def __setitem__(self, key, val): raise TypeError('Immutable')
    def clear(self): raise TypeError('Immutable')
    def pop(self, k, d=None): raise TypeError('Immutable')
    def popitem(self): raise TypeError('Immutable')
    def setdefault(self, k, d=None): raise TypeError('Immutable')
    def update(self, e, **f): raise TypeError('Immutable')

    def __hash__(self):
        if self.__hash is None:
            h = 0
            for k in self:
                h = ((h << 5) ^ (hash(k) << 2) ^ hash(self[k])) & sys.maxsize
            self.__hash = h
        return self.__hash

    @staticmethod
    def from_kvs(kvs):
        i = iter(kvs)
        result = ImmutableDict()
        result_proxy = super(ImmutableDict, result)
        try:
            while True:
                k = next(i)
                try:
                    v = next(i)
                except StopIteration:
                    raise DecodeError("Missing dictionary value")
                result_proxy.__setitem__(k, v)
        except StopIteration:
            pass
        return result

def dict_kvs(d):
    for k in d:
        yield k
        yield d[k]

class DecodeError(ValueError): pass
class EncodeError(ValueError): pass
class ShortPacket(DecodeError): pass

class Codec(object): pass

inf = float('inf')

class Annotated(object):
    def __init__(self, item):
        self.annotations = []
        self.item = item

    def __preserve_on__(self, encoder):
        for a in self.annotations:
            encoder.buffer.append(0x85)
            encoder.append(a)
        encoder.append(self.item)

    def strip(self, depth=inf):
        return strip_annotations(self, depth)

    def peel(self):
        return strip_annotations(self, 1)

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.item == other.item

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.item)

    def __repr__(self):
        return ' '.join(list('@' + repr(a) for a in self.annotations) + [repr(self.item)])

def is_annotated(v):
    return isinstance(v, Annotated)

def strip_annotations(v, depth=inf):
    if depth == 0: return v
    if not is_annotated(v): return v

    next_depth = depth - 1
    def walk(v):
        return strip_annotations(v, next_depth)

    v = v.item
    if isinstance(v, Record):
        return Record(strip_annotations(v.key, depth), tuple(walk(f) for f in v.fields))
    elif isinstance(v, list):
        return tuple(walk(f) for f in v)
    elif isinstance(v, tuple):
        return tuple(walk(f) for f in v)
    elif isinstance(v, set):
        return frozenset(walk(f) for f in v)
    elif isinstance(v, frozenset):
        return frozenset(walk(f) for f in v)
    elif isinstance(v, dict):
        return ImmutableDict.from_kvs(walk(f) for f in dict_kvs(v))
    elif is_annotated(v):
        raise ValueError('Improper annotation structure')
    else:
        return v

def annotate(v, *anns):
    if not is_annotated(v):
        v = Annotated(v)
    for a in anns:
        v.annotations.append(a)
    return v

class Decoder(Codec):
    def __init__(self, packet=b'', include_annotations=False, decode_pointer=None):
        super(Decoder, self).__init__()
        self.packet = packet
        self.index = 0
        self.include_annotations = include_annotations
        self.decode_pointer = decode_pointer

    def extend(self, data):
        self.packet = self.packet[self.index:] + data
        self.index = 0

    def nextbyte(self):
        if self.index >= len(self.packet):
            raise ShortPacket('Short packet')
        self.index = self.index + 1
        return _ord(self.packet[self.index - 1])

    def nextbytes(self, n):
        start = self.index
        end = start + n
        if end > len(self.packet):
            raise ShortPacket('Short packet')
        self.index = end
        return self.packet[start : end]

    def varint(self):
        v = self.nextbyte()
        if v < 128:
            return v
        else:
            return self.varint() * 128 + (v - 128)

    def peekend(self):
        matched = (self.nextbyte() == 0x84)
        if not matched:
            self.index = self.index - 1
        return matched

    def nextvalues(self):
        result = []
        while not self.peekend():
            result.append(self.next())
        return result

    def nextint(self, n):
        if n == 0: return 0
        acc = self.nextbyte()
        if acc & 0x80: acc = acc - 256
        for _i in range(n - 1):
            acc = (acc << 8) | self.nextbyte()
        return acc

    def wrap(self, v):
        return Annotated(v) if self.include_annotations else v

    def unshift_annotation(self, a, v):
        if self.include_annotations:
            v.annotations.insert(0, a)
        return v

    def next(self):
        tag = self.nextbyte()
        if tag == 0x80: return self.wrap(False)
        if tag == 0x81: return self.wrap(True)
        if tag == 0x82: return self.wrap(Float(struct.unpack('>f', self.nextbytes(4))[0]))
        if tag == 0x83: return self.wrap(struct.unpack('>d', self.nextbytes(8))[0])
        if tag == 0x84: raise DecodeError('Unexpected end-of-stream marker')
        if tag == 0x85:
            a = self.next()
            v = self.next()
            return self.unshift_annotation(a, v)
        if tag == 0x86:
            if self.decode_pointer is None:
                raise DecodeError('No decode_pointer function supplied')
            return self.wrap(self.decode_pointer(self.next()))
        if tag >= 0x90 and tag <= 0x9f: return self.wrap(tag - (0xa0 if tag > 0x9c else 0x90))
        if tag >= 0xa0 and tag <= 0xaf: return self.wrap(self.nextint(tag - 0xa0 + 1))
        if tag == 0xb0: return self.wrap(self.nextint(self.varint()))
        if tag == 0xb1: return self.wrap(self.nextbytes(self.varint()).decode('utf-8'))
        if tag == 0xb2: return self.wrap(self.nextbytes(self.varint()))
        if tag == 0xb3: return self.wrap(Symbol(self.nextbytes(self.varint()).decode('utf-8')))
        if tag == 0xb4:
            vs = self.nextvalues()
            if not vs: raise DecodeError('Too few elements in encoded record')
            return self.wrap(Record(vs[0], vs[1:]))
        if tag == 0xb5: return self.wrap(tuple(self.nextvalues()))
        if tag == 0xb6: return self.wrap(frozenset(self.nextvalues()))
        if tag == 0xb7: return self.wrap(ImmutableDict.from_kvs(self.nextvalues()))
        raise DecodeError('Invalid tag: ' + hex(tag))

    def try_next(self):
        start = self.index
        try:
            return self.next()
        except ShortPacket:
            self.index = start
            return None

def decode(bs, **kwargs):
    return Decoder(packet=bs, **kwargs).next()

def decode_with_annotations(bs, **kwargs):
    return Decoder(packet=bs, include_annotations=True, **kwargs).next()

class Encoder(Codec):
    def __init__(self, encode_pointer=id):
        super(Encoder, self).__init__()
        self.buffer = bytearray()
        self.encode_pointer = encode_pointer

    def contents(self):
        return bytes(self.buffer)

    def varint(self, v):
        if v < 128:
            self.buffer.append(v)
        else:
            self.buffer.append((v % 128) + 128)
            self.varint(v // 128)

    def encodeint(self, v):
        bitcount = (~v if v < 0 else v).bit_length() + 1
        bytecount = (bitcount + 7) // 8
        if bytecount <= 16:
            self.buffer.append(0xa0 + bytecount - 1)
        else:
            self.buffer.append(0xb0)
            self.varint(bytecount)
        def enc(n,x):
            if n > 0:
                enc(n-1, x >> 8)
                self.buffer.append(x & 255)
        enc(bytecount, v)

    def encodevalues(self, tag, items):
        self.buffer.append(0xb0 + tag)
        for i in items: self.append(i)
        self.buffer.append(0x84)

    def encodebytes(self, tag, bs):
        self.buffer.append(0xb0 + tag)
        self.varint(len(bs))
        self.buffer.extend(bs)

    def append(self, v):
        if hasattr(v, '__preserve_on__'):
            v.__preserve_on__(self)
        elif v is False:
            self.buffer.append(0x80)
        elif v is True:
            self.buffer.append(0x81)
        elif isinstance(v, float):
            self.buffer.append(0x83)
            self.buffer.extend(struct.pack('>d', v))
        elif isinstance(v, numbers.Number):
            if v >= -3 and v <= 12:
                self.buffer.append(0x90 + (v if v >= 0 else v + 16))
            else:
                self.encodeint(v)
        elif isinstance(v, bytes):
            self.encodebytes(2, v)
        elif isinstance(v, basestring):
            self.encodebytes(1, v.encode('utf-8'))
        elif isinstance(v, list):
            self.encodevalues(5, v)
        elif isinstance(v, tuple):
            self.encodevalues(5, v)
        elif isinstance(v, set):
            self.encodevalues(6, v)
        elif isinstance(v, frozenset):
            self.encodevalues(6, v)
        elif isinstance(v, dict):
            self.encodevalues(7, list(dict_kvs(v)))
        else:
            try:
                i = iter(v)
            except TypeError:
                self.buffer.append(0x86)
                self.append(self.encode_pointer(v))
                return
            self.encodevalues(5, i)

def encode(v, **kwargs):
    e = Encoder(**kwargs)
    e.append(v)
    return e.contents()
