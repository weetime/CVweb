# 手势控制浏览器页面项目

## 项目简介

这是一个基于计算机视觉的手势控制浏览器页面项目。通过摄像头捕获手势，使用 MediaPipe 进行手势识别，并通过 WebSocket 与前端页面通信，实现手势控制网页滚动功能。

## 项目架构

```
CVweb/
├── python/                    # Python 后端
│   ├── main.py               # 主程序入口
│   ├── gesture_recognizer.py # 手势识别模块
│   └── requirements.txt      # Python 依赖
├── web/                      # Node.js 前端
│   ├── server.js            # WebSocket 服务器
│   ├── package.json         # Node.js 依赖
│   └── public/
│       └── index.html       # 前端页面
└── allaboutproject.md       # 项目说明文档
```

## 主要功能

### 手势识别功能
- **scroll_up**: 手腕位置在屏幕上方（y < 0.4）时触发向上滚动
- **scroll_down**: 手腕位置在屏幕下方（y > 0.6）时触发向下滚动

### 技术栈
- **后端**: Python + OpenCV + MediaPipe + WebSocket
- **前端**: Node.js + Express + WebSocket
- **通信**: WebSocket 实时通信

## 安装和运行

### 1. 安装 Python 依赖
```bash
cd python
pip install -r requirements.txt
```

### 2. 安装 Node.js 依赖
```bash
cd web
npm install
```

### 3. 启动服务
```bash
# 启动 WebSocket 服务器
cd web
node server.js

# 启动手势识别程序
cd python
python main.py
```

### 4. 访问页面
打开浏览器访问 `http://localhost:8080`

## 模块说明

### GestureRecognizer 类

手势识别核心模块，提供以下功能：

#### 初始化参数
- `max_num_hands`: 最大检测手数（默认：1）
- `smoothing_window`: 手势平滑窗口大小（默认：5帧）

#### 主要方法
- `process_frame(frame)`: 处理单帧图像，返回标注后的图像和检测到的手势
- `_detect_gesture(hand_landmarks)`: 基于手部关键点检测具体手势
- `_apply_gesture_smoothing(raw_gesture)`: 应用手势平滑处理，减少抖动
- `reset_gesture_state()`: 重置手势识别状态
- `release()`: 释放资源

#### 优化特性
- **多关键点检测**: 使用手腕、中指MCP、食指指尖等多个关键点
- **手势平滑**: 基于历史帧的手势稳定性验证
- **置信度检查**: 60%置信度阈值，确保手势准确性
- **稳定性验证**: 需要连续3帧稳定才触发手势

#### 返回值说明
- `process_frame()` 返回 `(annotated_frame, gesture)`
  - `annotated_frame`: 标注了手部关键点的图像
  - `gesture`: 检测到的手势名称（"scroll_up"、"scroll_down" 或 None）

### main.py 主程序

主程序负责：
1. 初始化摄像头和手势识别器
2. 循环处理视频帧
3. 通过 WebSocket 发送手势指令
4. 资源清理

### WebSocket 通信协议

#### 消息格式
```json
{
  "type": "gesture",
  "action": "scroll_up" | "scroll_down"
}
```

## 使用示例

### 基本使用
```python
from gesture_recognizer import GestureRecognizer
import cv2

# 初始化手势识别器
recognizer = GestureRecognizer()

# 处理视频帧
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    annotated_frame, gesture = recognizer.process_frame(frame)
    
    if gesture:
        print(f"检测到手势: {gesture}")
    
    cv2.imshow("Gesture", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 常见问题

### 1. 摄像头无法打开
- 确保摄像头权限已授予
- 检查摄像头是否被其他程序占用
- 尝试更改摄像头索引（0, 1, 2...）

### 2. 手势识别不准确
- 确保手部在摄像头视野范围内
- 保持适当的光线条件
- 手部与摄像头保持适当距离

### 3. WebSocket 连接失败
- 确保 WebSocket 服务器已启动
- 检查端口 8080 是否被占用
- 确认防火墙设置

## 调试建议

1. **查看控制台输出**: 程序会打印检测到的手势信息
2. **调整手势阈值**: 在 `gesture_recognizer.py` 中修改 y 坐标阈值
3. **检查网络连接**: 确保 WebSocket 连接正常
4. **摄像头测试**: 使用 `cv2.imshow()` 确认摄像头工作正常

## 版本历史

- **v1.0.0**: 初始版本，基本手势识别功能
- **v1.1.0**: 模块化重构，分离手势识别逻辑
- **v1.2.0**: 手势识别灵敏度优化
  - 改进检测算法，使用多个手部关键点
  - 添加手势平滑处理，减少抖动
  - 提高检测阈值敏感度
  - 增加置信度验证和稳定性检查
