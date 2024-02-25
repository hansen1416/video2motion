# -*- coding: utf-8 -*-
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Access the environment variables using os.environ
OSS_ACCESS_KEY_ID = os.environ.get("OSS_ACCESS_KEY_ID")
print(OSS_ACCESS_KEY_ID)

# 使用环境变量中获取的RAM用户的访问密钥配置访问凭证。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
