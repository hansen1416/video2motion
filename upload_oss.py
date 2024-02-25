import os

import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()


# 使用环境变量中获取的RAM用户的访问密钥配置访问凭证。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())


# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
endpoint = "oss-ap-southeast-1.aliyuncs.com"

# 填写Bucket名称，并设置连接超时时间为30秒。
bucket = oss2.Bucket(auth, endpoint, "pose-daten", connect_timeout=30)

print(bucket)


def upload_screen_shot():

    data_dir = os.path.join(os.path.dirname(__file__), "video-recorder", "data")
    humanoid_name = "dors.glb"

    humanoid_path = os.path.join(data_dir, humanoid_name)

    for animation_name in os.listdir(humanoid_path):

        animation_name_path = os.path.join(humanoid_path, animation_name)

        for elevation in os.listdir(animation_name_path):

            elevation_path = os.path.join(animation_name_path, elevation)

            for azimuth in os.listdir(elevation_path):

                azimuth_path = os.path.join(elevation_path, azimuth)

                for file in os.listdir(azimuth_path):

                    object_name = f"screenshot/{humanoid_name}/{animation_name}/{elevation}/{azimuth}/{file}"

                    local_file = os.path.join(azimuth_path, file)

                    # check if `object_name` already exists in the bucket
                    if bucket.object_exists(object_name):
                        print(f"{object_name} already exists in the bucket")
                        continue

                    # print(object_name, local_file)

                    # 上传文件到OSS。
                    # yourObjectName由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
                    # yourLocalFile由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
                    result = bucket.put_object_from_file(object_name, local_file)

                    # HTTP返回码。
                    print("http status: {0}".format(result.status))

                    if int(result.status) != 200:
                        # output the local file path to local log
                        with open("upload-error.log", "a") as f:
                            f.write(f"{local_file}\n")


if __name__ == "__main__":

    upload_screen_shot()
