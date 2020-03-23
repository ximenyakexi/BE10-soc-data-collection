refer to opcua\ua\uatypes.py for nodeid type.

'''
def _from_string(string):
        l = string.split(";")
        identifier = None
        namespace = 0
        ntype = None
        srv = None
        nsu = None
        for el in l:
            if not el:
                continue
            k, v = el.split("=", 1)
            k = k.strip()
            v = v.strip()
            if k == "ns":
                namespace = int(v)
            elif k == "i":
                ntype = NodeIdType.Numeric
                identifier = int(v)
            elif k == "s":
                ntype = NodeIdType.String
                identifier = v
            elif k == "g":
                ntype = NodeIdType.Guid
                identifier = v
            elif k == "b":
                ntype = NodeIdType.ByteString
                identifier = v
            elif k == "srv":
                srv = v
            elif k == "nsu":
                nsu = v
'''