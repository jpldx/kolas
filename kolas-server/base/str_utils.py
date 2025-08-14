import base64

def to_base64(input_str):
    # 将字符串转换为字节（UTF-8编码）
    input_bytes = input_str.encode('utf-8')

    # 进行Base64编码，得到字节结果
    encoded_bytes = base64.b64encode(input_bytes)

    # 将字节结果转换回字符串
    encoded_str = encoded_bytes.decode('utf-8')

    return encoded_str
