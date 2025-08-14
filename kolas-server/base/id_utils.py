import uuid

def get_uuid() -> str:
    return uuid.uuid4().hex

if __name__ == '__main__':
    print(get_uuid())