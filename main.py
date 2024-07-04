import json
import os

import requests
import mqtt_client

headers = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Host": "api.hcyun.net",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13)XWEB/9185"
}

data = {
    "device_type_id": 1,
    "time": 30,
    "id": "9386",
    "login_key": os.environ['LOGIN_KEY'],
    "browser": 1
}


class PowerData:
    def __init__(self, remaining_power, degree_all, remaining_money, update_time, degree_list):
        self.remaining_power = remaining_power
        self.degree_all = degree_all
        self.remaining_money = remaining_money
        self.update_time = update_time
        self.degree_list = degree_list

    def get_latest_degree(self):
        latest_degree_item = self.degree_list[-1]
        latest_degree = latest_degree_item["degree"]
        return latest_degree

    def get_month_degree(self):
        month_degree = 0
        for item in self.degree_list:
            month_degree += float(item["degree"])
        return month_degree


def get_power_data():
    resp = requests.post("https://api.hcyun.net/mini/device/deviceInfo", headers=headers, data=json.dumps(data))
    if resp.status_code == 200:
        org_data = resp.json()['orgData']
        power_data = PowerData(org_data['device']['degree'], org_data['device']['degree_all'],
                               org_data['device']['price'],
                               org_data['device']['last_time'], org_data['degree'])
        return power_data
    else:
        print(resp.status_code)


if __name__ == '__main__':
    power_data = get_power_data()
    topic1 = "home/electricity/usage"
    mqtt_client.run({
        "consumption": float(power_data.get_latest_degree())
    }, topic1)

    topic2 = "home/electricity/usage/month"
    mqtt_client.run({
        "consumption": float(power_data.get_month_degree())
    }, topic2)

    topic3 = "home/electricity/remaining/money"
    mqtt_client.run({
        "remaining": float(power_data.remaining_money)
    }, topic3)
