import unittest
import requests
import ddt

# 直接定义数据
data_latitude_longitude_valid = [
    {'location': '118.896075,31.959850'},  # 示例有效经纬度
    {'location': '116.397228,39.907500'}   # 示例有效经纬度
]

data_latitude_longitude_invalid = [
    {'location': '999.999999,99.999999'},  # 示例无效经纬度
    {'location': '000.000000,00.000000'}   # 示例无效经纬度
]

@ddt.ddt
class TestAMAPReverseGeoAPIddt(unittest.TestCase):
    base_url = 'https://restapi.amap.com/v3/'
    api_key = 'e79c3b9e1f31fd06394dc591f4ef81e1'

    @classmethod
    def setUpClass(cls) -> None:
        print("-----逆地理编码执行后开始-----")

    @ddt.data(*data_latitude_longitude_valid)
    def test_reverse_geocode_valid_address_ddt(self, data):
        # 测试逆地理编码服务
        data['key'] = self.api_key
        params = data
        # 发送 GET 请求到逆地理编码接口
        response = requests.get(f'{self.base_url}/geocode/regeo', params=params)
        data = response.json()
        print(data)
        # 验证响应状态码和返回状态
        self.assertEqual(response.status_code, 200)  # 检查 HTTP 状态码是否为 200
        self.assertEqual(data['status'], '1')  # 检查 API 响应状态是否为 '1'，表示成功
        # 验证返回结果
        self.assertIn('regeocode', data)  # 检查响应中是否包含 'regeocode' 字段
        self.assertIn('formatted_address', data['regeocode'])  # 检查结果中是否包含 'formatted_address' 字段

    @ddt.data(*data_latitude_longitude_invalid)
    def test_reverse_geocode_invalid_address_ddt(self, data):
        # 测试逆地理编码服务的无效地址
        data['key'] = self.api_key
        params = data
        # 发送 GET 请求到逆地理编码接口
        response = requests.get(f'{self.base_url}/geocode/regeo', params=params)
        data = response.json()
        print(data)
        # 验证响应状态码和返回状态
        self.assertEqual(response.status_code, 200)  # 检查 HTTP 状态码是否为 200
        self.assertEqual(data['status'], '1')  # 检查 API 响应状态是否为 '1'，表示成功
        # 验证返回结果
        self.assertIn('regeocode', data)  # 检查响应中是否包含 'regeocode' 字段
        self.assertIn('formatted_address', data['regeocode'])  # 检查结果中是否包含 'formatted_address' 字段
        # self.assertEqual(data['regeocode']['formatted_address'], '[]')  # 结果为空，则说明没有查询到该经纬度位置

    def test_reverse_geocode_invalid_key(self):
        # 测试地理编码服务使用无效的 API Key
        params = {
            'location': '118.896075,31.959850',
            'key': 'INVALID_API_KEY_SZ2316108'
        }
        # 发送 GET 请求到地理编码接口
        response = requests.get(f'{self.base_url}/geocode/regeo', params=params)
        data = response.json()
        print(data)
        # 验证响应状态码和返回状态
        self.assertEqual(response.status_code, 200)  # 检查 HTTP 状态码是否为 200
        self.assertEqual(data['status'], '0')  # 检查 API 响应状态是否为 '0'，表示失败
        self.assertEqual(data.get('info'), 'INVALID_USER_KEY')  # 检查错误信息是否为 'INVALID_USER_KEY'

    def test_reverse_geocode_missing_key(self):
        # 测试地理编码服务缺少 API Key
        params = {
            'location': '118.896075,31.959850'
        }
        # 发送 GET 请求到地理编码接口
        response = requests.get(f'{self.base_url}/geocode/regeo', params=params)
        data = response.json()
        print(data)
        # 验证响应状态码和返回状态
        self.assertEqual(response.status_code, 200)  # 检查 HTTP 状态码是否为 200
        self.assertEqual(data['status'], '0')  # 检查 API 响应状态是否为 '0'，表示失败
        self.assertEqual(data.get('info'), 'INVALID_USER_KEY')  # 检查错误信息是否为 'INVALID_PARAMETERS'

    @classmethod
    def tearDownClass(cls) -> None:
        print("-----------------------")

if __name__ == '__main__':
    unittest.main()
    print("hello world")
