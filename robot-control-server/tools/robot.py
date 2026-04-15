"""
Robot Controller - 机器人控制模块
负责与机器人硬件通信，执行控制命令
"""

import asyncio
from typing import Dict, Any, Optional
from dataclasses import dataclass
from loguru import logger
import json


@dataclass
class RobotStatus:
    """机器人状态"""
    location_x: float = 0.0
    location_y: float = 0.0
    heading: float = 0.0  # 朝向角度
    battery: int = 100  # 电量百分比
    speed: float = 0.0  # 当前速度
    arm_position: str = "home"  # 机械臂位置
    gripper_state: str = "open"  # 夹爪状态
    led_state: bool = False
    sensors: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.sensors is None:
            self.sensors = {
                "ultrasonic_distance": 0.0,
                "infrared_left": False,
                "infrared_right": False,
                "temperature": 25.0,
                "humidity": 50.0
            }
    
    def to_dict(self) -> Dict:
        return {
            "location": {"x": self.location_x, "y": self.location_y},
            "heading": self.heading,
            "battery": self.battery,
            "speed": self.speed,
            "arm": self.arm_position,
            "gripper": self.gripper_state,
            "led": self.led_state,
            "sensors": self.sensors
        }


class RobotController:
    """
    机器人控制器
    
    负责：
    1. 与机器人硬件通信（串口/CAN）
    2. 执行控制命令
    3. 查询机器人状态
    """
    
    def __init__(
        self,
        serial_port: str = "/dev/ttyUSB0",
        baudrate: int = 115200,
        protocol: str = "json"  # json, custom
    ):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.protocol = protocol
        
        self.connected = False
        self.serial = None
        
        # 模拟机器人状态（实际应从硬件读取）
        self.status = RobotStatus()
        
        # 支持的动作
        self.supported_actions = {
            "move_forward": self._move_forward,
            "move_backward": self._move_backward,
            "turn_left": self._turn_left,
            "turn_right": self._turn_right,
            "stop": self._stop,
            "arm_up": self._arm_up,
            "arm_down": self._arm_down,
            "grip_open": self._grip_open,
            "grip_close": self._grip_close,
            "head_up": self._head_up,
            "head_down": self._head_down,
            "head_left": self._head_left,
            "head_right": self._head_right,
            "led_on": self._led_on,
            "led_off": self._led_off,
        }
        
        # 尝试连接
        self._connect()
    
    def _connect(self):
        """连接机器人"""
        try:
            # 实际实现应该使用pyserial连接
            # import serial
            # self.serial = serial.Serial(
            #     self.serial_port,
            #     self.baudrate,
            #     timeout=1
            # )
            
            self.connected = True
            logger.info(f"Robot connected on {self.serial_port}")
        
        except Exception as e:
            logger.warning(f"Failed to connect to robot: {e}")
            logger.info("Running in simulation mode")
            self.connected = False
    
    def is_connected(self) -> bool:
        """检查连接状态"""
        return self.connected
    
    def execute_action(self, action: str, parameter: float = 1.0) -> str:
        """
        执行机器人动作
        
        Args:
            action: 动作名称
            parameter: 动作参数
        
        Returns:
            执行结果描述
        """
        if action not in self.supported_actions:
            return f"不支持的动作: {action}。支持的动作为: {', '.join(self.supported_actions.keys())}"
        
        try:
            handler = self.supported_actions[action]
            result = handler(parameter)
            
            logger.info(f"Executed action: {action} with parameter {parameter}")
            return result
        
        except Exception as e:
            logger.error(f"Action execution error: {e}")
            return f"动作执行失败: {str(e)}"
    
    def get_status(self, status_type: str = "all") -> str:
        """
        获取机器人状态
        
        Args:
            status_type: all, location, battery, sensors, motors
        
        Returns:
            状态描述
        """
        # 模拟状态更新（实际应从硬件读取）
        self._update_status()
        
        if status_type == "all":
            return self._format_status_all()
        elif status_type == "location":
            return f"当前位置: ({self.status.location_x:.2f}, {self.status.location_y:.2f}), 朝向: {self.status.heading:.1f}°"
        elif status_type == "battery":
            return f"电池电量: {self.status.battery}%"
        elif status_type == "sensors":
            return f"传感器数据: 超声波距离={self.status.sensors['ultrasonic_distance']:.1f}cm, 温度={self.status.sensors['temperature']:.1f}°C"
        elif status_type == "motors":
            return f"机械臂位置: {self.status.arm_position}, 夹爪状态: {self.status.gripper_state}"
        else:
            return "未知的查询类型"
    
    def _update_status(self):
        """更新机器人状态（模拟）"""
        # 实际实现应该从硬件读取真实数据
        pass
    
    def _format_status_all(self) -> str:
        """格式化所有状态"""
        status_dict = self.status.to_dict()
        
        lines = [
            "=== 机器人状态 ===",
            f"位置: ({status_dict['location']['x']:.2f}, {status_dict['location']['y']:.2f})",
            f"朝向: {status_dict['heading']:.1f}°",
            f"电量: {status_dict['battery']}%",
            f"速度: {status_dict['speed']:.1f} m/s",
            f"机械臂: {status_dict['arm']}",
            f"夹爪: {status_dict['gripper']}",
            f"LED: {'开启' if status_dict['led'] else '关闭'}",
            "--- 传感器 ---",
            f"超声波: {status_dict['sensors']['ultrasonic_distance']:.1f}cm",
            f"温度: {status_dict['sensors']['temperature']:.1f}°C",
            f"湿度: {status_dict['sensors']['humidity']:.1f}%"
        ]
        
        return "\n".join(lines)
    
    # ========== 动作处理函数 ==========
    
    def _move_forward(self, distance: float) -> str:
        """前进"""
        self.status.location_x += distance * abs(self.status.heading - 90) / 90
        self.status.speed = 0.5
        
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "move",
                "action": "forward",
                "distance": distance
            })
        
        return f"机器人已向前移动{distance}米"
    
    def _move_backward(self, distance: float) -> str:
        """后退"""
        self.status.location_x -= distance * 0.5
        self.status.speed = -0.5
        
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "move",
                "action": "backward",
                "distance": distance
            })
        
        return f"机器人已向后移动{distance}米"
    
    def _turn_left(self, angle: float) -> str:
        """左转"""
        self.status.heading = (self.status.heading + angle) % 360
        
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "turn",
                "direction": "left",
                "angle": angle
            })
        
        return f"机器人已向左转{angle}度"
    
    def _turn_right(self, angle: float) -> str:
        """右转"""
        self.status.heading = (self.status.heading - angle) % 360
        
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "turn",
                "direction": "right",
                "angle": angle
            })
        
        return f"机器人已向右转{angle}度"
    
    def _stop(self, parameter: float) -> str:
        """停止"""
        self.status.speed = 0
        
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "stop"
            })
        
        return "机器人已停止"
    
    def _arm_up(self, parameter: float) -> str:
        """机械臂上升"""
        self.status.arm_position = f"up_{int(parameter * 100)}%"
        
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "arm",
                "action": "up",
                "parameter": parameter
            })
        
        return f"机械臂已上升至{parameter * 100:.0f}%"
    
    def _arm_down(self, parameter: float) -> str:
        """机械臂下降"""
        self.status.arm_position = f"down_{int(parameter * 100)}%"
        
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "arm",
                "action": "down",
                "parameter": parameter
            })
        
        return f"机械臂已下降至{parameter * 100:.0f}%"
    
    def _grip_open(self, parameter: float) -> str:
        """张开夹爪"""
        self.status.gripper_state = "open"
        
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "gripper",
                "action": "open"
            })
        
        return "夹爪已张开"
    
    def _grip_close(self, parameter: float) -> str:
        """合拢夹爪"""
        self.status.gripper_state = "closed"
        
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "gripper",
                "action": "close"
            })
        
        return "夹爪已合拢"
    
    def _head_up(self, angle: float) -> str:
        """抬头"""
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "head",
                "action": "up",
                "angle": angle
            })
        return f"机器人头部已向上转动{angle}度"
    
    def _head_down(self, angle: float) -> str:
        """低头"""
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "head",
                "action": "down",
                "angle": angle
            })
        return f"机器人头部已向下转动{angle}度"
    
    def _head_left(self, angle: float) -> str:
        """左转头"""
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "head",
                "action": "left",
                "angle": angle
            })
        return f"机器人头部已向左转动{angle}度"
    
    def _head_right(self, angle: float) -> str:
        """右转头"""
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "head",
                "action": "right",
                "angle": angle
            })
        return f"机器人头部已向右转动{angle}度"
    
    def _led_on(self, parameter: float) -> str:
        """LED开启"""
        self.status.led_state = True
        
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "led",
                "action": "on",
                "brightness": parameter
            })
        
        return "LED已开启"
    
    def _led_off(self, parameter: float) -> str:
        """LED关闭"""
        self.status.led_state = False
        
        if self.protocol == "json" and self.connected:
            self._send_command({
                "type": "led",
                "action": "off"
            })
        
        return "LED已关闭"
    
    def _send_command(self, command: Dict):
        """发送命令到机器人"""
        if self.serial and self.serial.is_open:
            try:
                data = json.dumps(command) + "\n"
                self.serial.write(data.encode('utf-8'))
                logger.debug(f"Sent command: {command}")
            except Exception as e:
                logger.error(f"Failed to send command: {e}")
    
    def disconnect(self):
        """断开连接"""
        if self.serial and self.serial.is_open:
            self.serial.close()
        self.connected = False
        logger.info("Robot disconnected")
