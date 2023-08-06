from iot_device.iot_tools import IoTools
from iot_device.iot_device_info import IoTDeviceInfo
from iot_device.iot_device import IoTDevice
from iot_thing.iot_thing import IoThing
from iot_thing.iot_thing_event import IoTingEvent
from threading import Timer
import json
import time
import random

class EventComputerStatus(IoTingEvent):
    """
    定义事件：主机是否在线
    """

    def __init__(self):
        self.event_name = "event_computer_offline"
        # params: 离线
        self.is_offline = 0

    def get_event_name(self):
        return self.event_name

    def get_event_data(self):
        return {
            "is_offline": self.is_offline
        }


class SampleThing(IoThing):

    """
    定义物模型: 注意 config/thing.json
    """

    def init_device_thing(self):
        self.event_computer_status = EventComputerStatus()
        self.is_running = False

    def thing_start(self):
        self.is_running = True
        Timer(1, self.check_computer_status, ()).start()

    def check_computer_status(self):
        while self.is_running:
            self.event_computer_status.is_offline = random.randint(0, 1)
            self.post_event(self.event_computer_status)
            time.sleep(30)

    def thing_stop(self):
        self.is_running = False

    def get_thing_topics(self, iotopic):
        pass


if __name__ == '__main__':
    """
    初始化运行
    """
    tools = IoTools()
    # 设备名称:  平台添加
    device_name = "sample"
    product_file = 'sample.ini'
    # 1）平台添加: 准备认证信息: 烧录到芯片中；
    product_key = "a1jGlVZEI9V"
    product = {
        "product_key": "a1jGlVZEI9V",
        "product_secret": "4k5FORqDuZyrw3xu",
        "endpoint": "",
    }

    product_encode = tools.aes_encode(product_key, json.dumps(product))
    # print(product_encode)
    tools.write_text(product_file, product_encode)
    # 2）读取认证信息：初始化设备
    has, secret_info = tools.read_text(product_file)
    if not has:
        raise Exception('未知设备：设备证书不存在')
    # 3) 设备信息
    device_info = IoTDeviceInfo(is_debug=False)
    device_info.init_info(device_name, product_key, secret_info)
    # 4) 物模型
    device_thing = SampleThing()
    # 5) 设备连接运行
    device = IoTDevice(device_info, device_thing)
    device.connect()
    # 6) 运行
    while True:
        # print(device.is_conn)
        time.sleep(1000)
