import random
import string


class Tools:

    @staticmethod
    def generate_verification_code():
        """隨機生成一個6位數驗證碼"""
        characters = string.digits + string.ascii_letters  # 包含数字和字母的字符集
        code = ''.join(random.choices(characters, k=6))
        return code


class Email:
    """模擬發送手機驗證碼"""

    @staticmethod
    def send(email: str, code: str):
        print("假裝發送驗證碼[email:{}, 驗證碼:{}]".format(email, code))
        return {'code': "OK", "message": "驗證碼發送成功"}
