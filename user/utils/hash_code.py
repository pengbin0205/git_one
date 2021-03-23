import hashlib

from user.utils.salt import get_salt


def hash_pwd(pwd, salt):
    h = hashlib.md5()
    pwd += salt
    h.update(pwd.encode())

    return h.hexdigest()

def hash_email(code):
    h = hashlib.md5()
    h.update(code.encode())
    return h.hexdigest()

"""
# 通过hashlib的构造函数来创建一个hash对象
h = hashlib.md5()

# 使用hash对象的update方法添加要添加的信息 update()方法只接收bytes类型的数据
h.update(b"mm123456" + b'sdhj893;.')

# 获取bytes类型的摘要
print(h.digest())

# 获取16进制 str类型的加密后的信息
m = h.hexdigest()
print(m, len(m))
"""
