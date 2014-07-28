
def serialize_string(str_, serialize_class):
    obj_ = serialize_class()
    obj_.ParseFromString(str_)
    return obj_
