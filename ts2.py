import unittest
import requests
import ddt

# 用于测试的数据
data_valid = [
    {'locations': '116.481499,39.990475', 'coordsys': 'gps'},
    {'locations': '121.473701,31.230416', 'coordsys': 'gps'}
]

data_invalid = [
    {'locations': '300.000000,39.990475', 'coordsys': 'gps'},  # 无效的经度
    {'locations': '116.481499,1000.000000', 'coordsys': 'gps'}  # 无效的纬度
]

data_coordsys_invalid = [
    {'locations': '116.481499,39.990475', 'coordsys': 'invalid_coordsys'},  # 无效的坐标系
    {'locations': '121.473701,31.230416', 'coordsys': 'unknown'}  # 未知的坐标系
]


@ddt.ddt
class TestAMAPCoordinateConvertAPI(unittest.TestCase):
    base_url = 'https://restapi.amap.com/v3/assistant/coordinate/convert'
    api_key = '576f5904ada15785936604df369e54f9'

    @classmethod
    def setUpClass(cls) -> None:
        print("-----坐标转换开始执行-----")

    @ddt.data(*data_valid)
    def test_coordinate_conversion_ddt(self, data):
        data['key'] = self.api_key
        data['coordsys'] = 'gps'
        params = data

        # 发送 GET 请求到坐标转换接口
        response = requests.get(self.base_url, params=params)
        data = response.json()

        print(data)

        # 验证响应状态码和返回状态
        self.assertEqual(response.status_code, 200)  # 检查 HTTP 状态码是否为 200
        self.assertEqual(data['status'], '1')  # 检查 API 响应状态是否为 '1'，表示成功
        # 验证返回结果
        self.assertIn('locations', data)  # 检查响应中是否包含 'locations' 字段
        self.assertIsInstance(data['locations'], str)  # 确保 'locations' 字段是字符串

    @ddt.data(*data_invalid)
    def test_coordinate_conversion_invalid_location_ddt(self, data):
        data['key'] = self.api_key
        data['coordsys'] = 'gps'
        params = data

        # 发送 GET 请求到坐标转换接口
        response = requests.get(self.base_url, params=params)
        data = response.json()

        print(data)

        # 验证响应状态码和返回状态
        self.assertEqual(response.status_code, 200)  # 检查 HTTP 状态码是否为 200
        self.assertEqual(data['status'], '1')  # 检查 API 响应状态是否为 '0'，表示失败
        self.assertEqual(data.get('info'), 'ok')  # 检查错误信息是否为 'INVALID_PARAMS'



    @ddt.data(*data_coordsys_invalid)
    def test_coordinate_conversion_invalid_coordsys_ddt(self, data):
        data['key'] = self.api_key
        params = data

        # 发送 GET 请求到坐标转换接口
        response = requests.get(self.base_url, params=params)
        data = response.json()

        print(data)

        # 验证响应状态码和返回状态
        self.assertEqual(response.status_code, 200)  # 检查 HTTP 状态码是否为 200
        self.assertEqual(data['status'], '1')  # 检查 API 响应状态是否为 '0'，表示失败
        self.assertEqual(data.get('info'), 'ok')  # 检查错误信息是否为 'INVALID_PARAMS'

    @classmethod
    def tearDownClass(cls) -> None:
        print("-----------------------")


if __name__ == '__main__':
    unittest.main()
