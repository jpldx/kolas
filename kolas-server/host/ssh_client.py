import socket
import paramiko

DEFAULT_CONNECTION_TIMEOUT = 5 # 默认建立连接超时时间（s）

class SshClient:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def test_general_connection(self, timeout=DEFAULT_CONNECTION_TIMEOUT):
        """测试基本网络连接（仅检查端口是否可达）"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((self.ip, self.port))
                return result == 0  # 0表示连接成功
        except Exception as e:
            print(f"网络连接错误: {str(e)}")
            return False

    def test_ssh_connection(self, timeout=DEFAULT_CONNECTION_TIMEOUT):
        """测试SSH服务连接及认证"""
        # 先检查基本网络连接
        if not self.test_general_connection(timeout):
            print(f"无法连接到 {self.ip}:{self.port}")
            return False

        try:
            # 创建SSH客户端
            ssh = paramiko.SSHClient()
            # 自动接受未知的主机密钥
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 尝试连接
            ssh.connect(
                hostname=self.ip,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=timeout,
                allow_agent=False,
                look_for_keys=False
            )

            # 连接成功，关闭连接
            ssh.close()
            return True

        except paramiko.AuthenticationException:
            print("认证失败：用户名或密码错误")
            return False
        except Exception as e:
            print(f"SSH连接错误: {str(e)}")
            return False

def main():
    # 测试参数
    server_ip = "172.21.121.178"
    server_port = 22
    username = "het"
    password = "Het@2020"

    ssh_client = SshClient(
        ip=server_ip,
        port=server_port,
        username=username,
        password=password
    )

    # 测试连接
    print(f"测试 {server_ip}:{server_port} 连接...")
    if ssh_client.test_ssh_connection():
        print("连接成功！账号密码验证通过")
    else:
        print("连接失败")


if __name__ == "__main__":
    main()