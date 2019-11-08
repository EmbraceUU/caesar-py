import time


def id_to_time(object_id):
    """
    根据object_id转换成date
    :param object_id:
    :return:
    """
    time_stamp = int(object_id[:8], 16)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))


if __name__ == '__main__':
    ob = '5dc2d1f9bc70b9959b81cf0b'
    print(id_to_time(ob))
