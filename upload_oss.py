# -*- coding: utf-8 -*-
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

# 使用环境变量中获取的RAM用户的访问密钥配置访问凭证。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
