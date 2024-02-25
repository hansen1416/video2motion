"""
python quaternion to euler
same logic as in three.js
"""

import math
import os
import json


class Euler:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def to_array(self):
        return [self.x, self.y, self.z]


class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


class Quaternion:
    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)

    def normalize(self):
        l = self.length()

        if l == 0:
            self.x = 0
            self.y = 0
            self.z = 0
            self.w = 1
        else:
            l = 1 / l
            self.x *= l
            self.y *= l
            self.z *= l
            self.w *= l


class Matrix4:
    def __init__(self):
        self.elements = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]


def matrix_rotation_from_quaternion(
    position: Vector3 = Vector3(0, 0, 0),
    quaternion: Quaternion = Quaternion(0, 0, 0, 1),
    scale: Vector3 = Vector3(1, 1, 1),
):
    quaternion.normalize()

    matrix = Matrix4()
    te = matrix.elements

    x = quaternion.x
    y = quaternion.y
    z = quaternion.z
    w = quaternion.w

    x2 = x + x
    y2 = y + y
    z2 = z + z

    xx = x * x2
    xy = x * y2
    xz = x * z2

    yy = y * y2
    yz = y * z2
    zz = z * z2

    wx = w * x2
    wy = w * y2
    wz = w * z2

    sx = scale.x
    sy = scale.y
    sz = scale.z

    te[0] = (1 - (yy + zz)) * sx
    te[1] = (xy + wz) * sx
    te[2] = (xz - wy) * sx
    te[3] = 0

    te[4] = (xy - wz) * sy
    te[5] = (1 - (xx + zz)) * sy
    te[6] = (yz + wx) * sy
    te[7] = 0

    te[8] = (xz + wy) * sz
    te[9] = (yz - wx) * sz
    te[10] = (1 - (xx + yy)) * sz
    te[11] = 0

    te[12] = position.x
    te[13] = position.y
    te[14] = position.z
    te[15] = 1

    return matrix


def clamp(value, min_value, max_value):
    """
    function clamp( value, min, max ) {

            return Math.max( min, Math.min( max, value ) );

    }
    """
    return max(min_value, min(max_value, value))


def euler_from_matrix(matrix: Matrix4, order: str = "XYZ"):

    te = matrix.elements
    m11 = te[0]
    m12 = te[4]
    m13 = te[8]
    m21 = te[1]
    m22 = te[5]
    m23 = te[9]
    m31 = te[2]
    m32 = te[6]
    m33 = te[10]

    if order == "XYZ":
        y = math.asin(clamp(m13, -1, 1))

        if abs(m13) < 0.9999999:
            x = math.atan2(-m23, m33)
            z = math.atan2(-m12, m11)
        else:
            x = math.atan2(m32, m22)
            z = 0

    elif order == "YXZ":
        x = math.asin(-clamp(m23, -1, 1))

        if abs(m23) < 0.9999999:
            y = math.atan2(m13, m33)
            z = math.atan2(m21, m22)
        else:
            y = math.atan2(-m31, m11)
            z = 0

    elif order == "ZXY":
        x = math.asin(clamp(m32, -1, 1))

        if abs(m32) < 0.9999999:
            y = math.atan2(-m31, m33)
            z = math.atan2(-m12, m22)
        else:
            y = 0
            z = math.atan2(m21, m11)

    elif order == "ZYX":
        y = math.asin(-clamp(m31, -1, 1))

        if abs(m31) < 0.9999999:
            x = math.atan2(m32, m33)
            z = math.atan2(m21, m11)
        else:
            x = 0
            z = math.atan2(-m12, m22)

    elif order == "YZX":
        z = math.asin(clamp(m21, -1, 1))

        if abs(m21) < 0.9999999:
            x = math.atan2(-m23, m22)
            y = math.atan2(-m31, m11)
        else:
            x = 0
            y = math.atan2(m13, m33)

    elif order == "XZY":
        z = math.asin(-clamp(m12, -1, 1))

        if abs(m12) < 0.9999999:
            x = math.atan2(m32, m22)
            y = math.atan2(m13, m11)
        else:
            x = math.atan2(-m23, m33)
            y = 0

    else:
        raise ValueError(f"Unknown order: {order}")

    return Euler(x, y, z)


def euler_from_quaternion(quaternion: Quaternion, order: str = "XYZ") -> Euler:
    matrix = matrix_rotation_from_quaternion(quaternion=quaternion)
    return euler_from_matrix(matrix, order)


if __name__ == "__main__":
    data_dir = os.path.join(".", "anim-json")
    data_dir_euler = os.path.join(".", "anim-json-euler")

    filenames = []

    # iterate ovedr folder /public/anim-json
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filenames.append(filename)

    for fname in filenames:

        data = json.load(open(os.path.join(data_dir, fname), "r"))

        tracks = data["tracks"]

        tracks_euler = {}

        for track in tracks:
            if track["type"] == "quaternion":

                track_info = {
                    "times": track["times"],
                    "values": [],
                }

                for i in range(0, len(track["values"]), 4):
                    quaternion = Quaternion(
                        track["values"][i],
                        track["values"][i + 1],
                        track["values"][i + 2],
                        track["values"][i + 3],
                    )

                    euler = euler_from_quaternion(quaternion)

                    track_info["values"].append(euler.to_array())

                tracks_euler[track["name"].replace(".quaternion", "")] = track_info

        with open(os.path.join(data_dir_euler, fname), "w") as f:
            json.dump(tracks_euler, f, indent=2)
