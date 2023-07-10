import time

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from common.tool import Tools, Email
from users.models import User, SMSCode


class UserSerializer(serializers.ModelSerializer):
    """用戶模型的序列化器"""
    code = serializers.CharField(label='驗證碼', write_only=True)
    code_id = serializers.CharField(label='驗證碼ID', write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'avatar', 'role', 'code_id', 'code']
        read_only_fields = ['id', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """用戶模型需要重寫create方法"""
        return User.objects.create_user(**validated_data)  # **validated_data表示將字典拆分成鍵值對

    def update(self, instance, validated_data):
        """用戶模型的update方法需要處理password字段"""
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

    def validate(self, data):
        if self.instance is None:  # 如果是创建(POST請求),需要校驗驗證碼(注冊用戶)
            code_id, code = data.pop('code_id'), data.pop('code')  # code_id和code兩個字段需要刪除
            code_obj = SMSCode.objects.filter(id=code_id, code=code, email=data['email']).first()  # 使用查詢校驗驗證碼
            if not code_obj:  # 驗證碼不存在
                raise serializers.ValidationError({'code': '驗證失敗,請重新獲取驗證碼'})

            time_diff = time.time() - code_obj.create_time.timestamp()  # 計算驗證碼創建時間, timestamp()表示轉換為時間戳
            code_obj.delete()  # 刪除驗證碼(避免用戶在有效期内,使用同一個驗證碼重複請求)
            if time_diff >= 60 * 3:  # 校驗驗證碼是否過期(過期時間3分鐘)
                raise serializers.ValidationError({'code': '驗證碼已過期,請重新獲取驗證碼'})
        # else:  # 否則説明是修改請求
        #   添加修改请求的验证逻辑
        #   raise serializers.ValidationError('Value was invalid')
        return data


class SMSCodeSerializer(serializers.ModelSerializer):
    """驗證碼模型的序列化器"""

    class Meta:
        model = SMSCode
        fields = ['id', 'email']

    def validate(self, data):
        data['code'] = Tools.generate_verification_code()  # code字段由後端生成,隨機生成一個6位數驗證碼
        result = Email().send(email=data['email'], code=data['code'])  # 发送验证码邮件
        if result['code'] != 'OK':  # 如果發送失敗給前端返回錯誤
            raise serializers.ValidationError({'email': '无法发送验证码邮件'})
        return data
