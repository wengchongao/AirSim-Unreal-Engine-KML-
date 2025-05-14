# 利用UE4引擎与python脚本实现无人机仿真飞行
## 项目简介
本项目基于 Microsoft AirSim 和 Unreal Engine 平台，构建了一个具备真实地理参考坐标的城市建筑仿真环境，结合 Python 控制脚本，实现了无人机沿 KML 文件定义路径的精准飞行。系统支持导入 FBX 建筑模型，并在场景中通过 GeoReferencingSystem 设定与现实地理坐标一致的原点，实现了从真实地理数据到虚拟空间的严密对齐。
适用于城市感知、无人机路径规划、虚拟遥感测试、航迹重建等科研和教学应用。

相同版本的airsim文件可通过git clone https://github.com/Microsoft/AirSim.git进行下载和安装
## 项目特性
* 使用 Unreal Engine 的 GeoReferencingSystem 设置地理原点（WGS84 / UTM）
* 导入 Blender 建模并导出的 FBX 建筑模型，并精确对齐世界坐标原点
* 支持从 Google Earth 导出的 .kml 文件中提取航线点
* 将 KML 中经纬度点转换为 AirSim 所用的本地 NED 坐标
* 使用 Python 脚本控制无人机逐点或整条路径飞行
* 支持设置飞行速度、高度、起飞与降落控制
* 提供 main.py 和 survey.py 两套控制脚本（分别实现点对点与连续轨迹控制）
## 文件结构

AirSim/                  # Microsoft AirSim 模拟器源码或子模块（或链接）
UnrealEnvironment/       # Unreal 工程，包含建筑模型及地理参考配置的地图场景
airsim_python/
├── main.py              # 读取 KML 并逐点控制飞行的主控脚本
├── survey.py            # 圆形轨迹飞行、匀速测试控制脚本
├── template.kml         # 测试用航迹文件（Google Earth 导出）
settings.json            # 配置无人机原点坐标的 AirSim 参数文件
README.md                # 项目说明文档（本文件）


## 快速启动

1. 打开 Unreal Engine 工程 `UnrealEnvironment`，加载包含 GeoReferencingSystem 的地图；
2. 启动 AirSim 并加载相应地图场景（需启用“GeoReferencing”插件）；
3. 确保 `settings.json` 中设置了 OriginGeopoint 与 GeoReferencing 原点一致；
4. 运行 Python 控制脚本：


脚本将：
* 自动解析 `template.kml` 中的路径
* 将经纬度转换为 NED 坐标
* 控制无人机起飞 → 按路径飞行 → 自动降落

## 核心依赖

* Python 3.x
* airsim (Python API)
* numpy, utm, xml.etree.ElementTree（用于 KML 解析与坐标转换）
* Unreal Engine 4.27+（支持 GeoReferencing 插件）

## 扩展建议

* 加入 `YawMode` 控制，使无人机始终朝向飞行方向
* 按 KML 中时间戳动态控制速度，实现真实节奏还原
* 扩展功能：采集照片、构建点云、路径重建、SLAM 数据模拟
* 支持从 Spline 曲线构建飞行路径，提升飞行平滑性

## 致谢

本项目参考 Microsoft AirSim 框架，感谢 Unreal Engine 提供的高质量可视化平台，以及社区关于 GeoReferencing + FBX 坐标对齐的经验分享。

作者：翁崇奥
日期：2025年5月

