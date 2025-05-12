import simplekml
import airsim
import math
from xml.etree import ElementTree as ET
import logging
import utm

# 配置日志输出
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_coordinates_from_kml(kml_file_path):
    try:
        with open(kml_file_path, 'r', encoding='utf-8') as file:
            kml_string = file.read()
        root = ET.fromstring(kml_string)
        # 定义命名空间
        ns = {'kml': 'http://www.opengis.net/kml/2.2', 'wpml': 'http://www.dji.com/wpmz/1.0.6'}
        coordinates = []
        # 查找所有 Placemark 元素
        placemarks = root.findall('.//kml:Placemark', ns)
        for placemark in placemarks:
            point = placemark.find('.//kml:Point', ns)
            if point is not None:
                coords_element = point.find('.//kml:coordinates', ns)
                if coords_element is not None:
                    coords_text = coords_element.text.strip()
                    try:
                        lon, lat, = coords_text.split(',')
                        coordinates.append((float(lat), float(lon)))
                        logging.info(f"提取到经纬度: 纬度 {lat}, 经度 {lon}")
                    except ValueError:
                        logging.error(f"无法解析坐标值: {coords_text}")
        return coordinates
    except FileNotFoundError:
        logging.error(f"文件未找到: {kml_file_path}")
        return []
    except ET.ParseError:
        logging.error(f"无法解析 KML 文件: {kml_file_path}")
        return []
    except Exception as e:
        logging.error(f"读取 KML 文件时出错: {e}")
        return []

def latlon_to_ned(lat, lon, ref_lat, ref_lon, ref_alt=0):
    ref_utm = utm.from_latlon(ref_lat, ref_lon)
    target_utm = utm.from_latlon(lat, lon)

    north = target_utm[1] - ref_utm[1]
    east = target_utm[0] - ref_utm[0]
    down = -ref_alt  # 简化处理，假设飞行高度恒定
    return (north, east, down)

# def convert_to_airsim_coords(client, lat, lon):
#     home_gps = client.getHomeGeoPoint()
#     # ref_lat = home_gps.latitude
#     # ref_lon = home_gps.longitude
#     ref_lat, ref_lon, ref_altt = home_gps
#     dLat = lat - ref_lat
#     dLon = lon - ref_lon
#     R = 6371000  # 地球半径，单位：米
#     x = R * math.cos(math.radians(ref_lat)) * math.radians(dLon)
#     y = R * math.radians(dLat)
#     return x, y


def fly_along_coordinates(client, coordinates):
    # home_gps = client.getHomeGeoPoint()
    # ref_lat = home_gps.latitude
    # ref_lon = home_gps.longitude
    ref_lat, ref_lon = 29.92302, 121.62586
    # ref_lat, ref_lon = 29.9229622119221, 121.624936265309
    for lat, lon in coordinates:
        x, y, z = latlon_to_ned(lat, lon, ref_lat, ref_lon)
        print(x, y, z)
        z = -10  # 飞行高度
        speed = 10  # 飞行速度
        client.moveToPositionAsync(x, y, z, speed).join()


if __name__ == "__main__":
    kml_file_path = 'template.kml'
    coordinates = get_coordinates_from_kml(kml_file_path)
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    # 起飞
    client.takeoffAsync().join()
    if coordinates:
        fly_along_coordinates(client, coordinates)
    # 降落
    client.landAsync().join()
    client.armDisarm(False)
    client.enableApiControl(False)
