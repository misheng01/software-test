import unittest
import requests
import ddt

# 定义硬编码的测试数据
data_address_valid = [
    {'address': '江苏省南京市江宁区将军大道29号', 'key': '576f5904ada15785936604df369e54f9'},
    {'address': '江苏省南京市秦淮区御道街29号', 'key': '576f5904ada15785936604df369e54f9'},
    {'address': '江苏省溧阳市滨河东路29号', 'key': '576f5904ada15785936604df369e54f9'}
]

data_address_invalid = [
    {'address': '无效地址', 'key': '576f5904ada15785936604df369e54f9'},
    {'address': 'xxx', 'key': '576f5904ada15785936604df369e54f9'}
]

# 高德地图API 功能测试——地理/逆地理编码功能
@ddt.ddt
class TestAMAPGeoAPI(unittest.TestCase):

    base_url = 'https://restapi.amap.com/v3/geocode/geo'

    @classmethod
    def setUpClass(cls) -> None:
        print("-----地理编码测试-----")

    @ddt.data(*data_address_valid)
    def test_geocode_valid_address_ddt(self, data):
        params = {'address': data['address'], 'key': data['key']}
        response = requests.get(self.base_url, params=params)
        data = response.json()

        print("Valid Address Response:", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('status'), '1')
        self.assertIn('geocodes', data)
        if data.get('geocodes'):
            self.assertIn('location', data['geocodes'][0])

    @ddt.data(*data_address_invalid)
    def test_geocode_invalid_address_ddt(self, data):
        params = {'address': data['address'], 'key': data['key']}
        response = requests.get(self.base_url, params=params)
        data = response.json()

        print("Invalid Address Response:", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('status'), '0')
        self.assertIn(data.get('info'), ['ENGINE_RESPONSE_DATA_ERROR', 'INVALID_PARAMS'])

    def test_geocode_missing_key(self):
        params = {'address': '南京市江宁区将军大道 29 号南京航空航天大学'}
        response = requests.get(self.base_url, params=params)
        data = response.json()

        print("Missing Key Response:", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('status'), '0')
        self.assertEqual(data.get('info'), 'INVALID_USER_KEY')

    def test_geocode_invalid_key(self):
        params = {
            'address': '南京市江宁区将军大道 29 号南京航空航天大学',
            'key': 'INVALID_API_KEY_SZ2316108'
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()

        print("Invalid Key Response:", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('status'), '0')
        self.assertEqual(data.get('info'), 'INVALID_USER_KEY')

    @classmethod
    def tearDownClass(cls) -> None:
        print("-----TestAMAPGeoAPI 结束-----")

if __name__ == '__main__':
    unittest.main()
