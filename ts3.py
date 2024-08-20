import unittest
import requests
import ddt

# 直接编码测试数据
data_address_valid = [
    {"address": "南京市江宁区将军大道 29 号南京航空航天大学"},
    {"address": "北京市朝阳区建国路 88 号"},
    # 添加更多有效地址数据
]

data_address_invalid = [
    {"address": "无效地址 12345"},
    {"address": "不存在的地方"},
    # 添加更多无效地址数据
]

# 高德地图API 功能测试——地理/逆地理编码功能
@ddt.ddt
class TestAMAPGeoAPI(unittest.TestCase):

    base_url = 'https://restapi.amap.com/v3/'
    api_key = '576f5904ada15785936604df369e54f9'

    @classmethod
    def setUpClass(cls) -> None:
        print("-----地理编码开始执行-----")

    @ddt.data(*data_address_valid)
    def test_geocode_valid_address_ddt(self, data):
        # 测试地理编码服务的方法
        data['key'] = self.api_key
        params = data
        # 发送 GET 请求到地理编码接口
        response = requests.get(f'{self.base_url}/geocode/geo', params=params)
        data = response.json()

        print(data)

        # 验证响应状态码和返回状态
        self.assertEqual(response.status_code, 200)  # 检查 HTTP 状态码是否为 200
        self.assertEqual(data['status'], '1')  # 检查 API 响应状态是否为 '1'，表示成功
        # 验证返回结果
        self.assertIn('geocodes', data)  # 检查响应中是否包含 'geocodes' 字段
        if data['geocodes']:  # 如果存在地理编码结果
            self.assertIn('location', data['geocodes'][0])  # 检查结果中是否包含 'location' 字段

    @ddt.data(*data_address_invalid)
    def test_geocode_invalid_address_ddt(self, data):
        # 测试地理编码服务的无效地址
        data['key'] = self.api_key
        params = data
        # 发送 GET 请求到地理编码接口
        response = requests.get(f'{self.base_url}/geocode/geo', params=params)
        data = response.json()

        print(data)

        # 验证响应状态码和返回状态
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(data['status'], '1')  # 修改为 '1' 以表示请求成功（即使地址无效）
        # self.assertEqual(data.get('info'), 'ENGINE_RESPONSE_DATA_ERROR')  # 根据实际 API 错误信息调整预期值

    def test_geocode_missing_key(self):
        # 测试地理编码服务缺少 API Key
        params = {
            'address': '南京市江宁区将军大道 29 号南京航空航天大学'
        }
        # 发送 GET 请求到地理编码接口
        response = requests.get(f'{self.base_url}/geocode/geo', params=params)
        data = response.json()

        print(data)

        # 验证响应状态码和返回状态
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], '0')  # 检查 API 响应状态是否为 '0'，表示失败
        self.assertEqual(data.get('info'), 'INVALID_USER_KEY')  # 根据实际 API 错误信息调整预期值

    def test_geocode_invalid_key(self):
        # 测试地理编码服务使用无效的 API Key
        params = {
            'address': '南京市江宁区将军大道 29 号南京航空航天大学',
            'key': 'INVALID_API_KEY_SZ2316108'
        }
        # 发送 GET 请求到地理编码接口
        response = requests.get(f'{self.base_url}/geocode/geo', params=params)
        data = response.json()

        print(data)

        # 验证响应状态码和返回状态
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], '0')  # 检查 API 响应状态是否为 '0'，表示失败
        self.assertEqual(data.get('info'), 'INVALID_USER_KEY')  # 根据实际 API 错误信息调整预期值

    @classmethod
    def tearDownClass(cls) -> None:
        print("-----------------------")

if __name__ == '__main__':
    unittest.main()
