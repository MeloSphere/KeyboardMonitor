import os
import sys
import threading
import time
import json
from pathlib import Path
import tkinter as tk
from pynput import keyboard


def get_app_root():
    """获取应用程序根目录"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def ensure_app_directory():
    """确保程序在正确的目录下运行"""
    app_root = get_app_root()
    os.chdir(app_root)
    return app_root


class KeyboardMonitor:
    """键盘监控器类，负责处理键盘输入和显示"""

    def __init__(self, callback=None):
        """
        初始化键盘监控器
        Args:
            callback: 可选的回调函数，接收按键文本作为参数
        """
        self.callback = callback
        self.listener = None
        self.running = False

        # 特殊按键映射表
        self.special_keys = {
            keyboard.Key.space: "␣",
            keyboard.Key.enter: "⏎",
            keyboard.Key.backspace: "⌫",
            keyboard.Key.tab: "⇥",
            keyboard.Key.esc: "⎋",
            keyboard.Key.shift: "⇧",
            keyboard.Key.ctrl: "⌃",
            keyboard.Key.alt: "⌥",
            keyboard.Key.caps_lock: "⇪",
            keyboard.Key.left: "←",
            keyboard.Key.right: "→",
            keyboard.Key.up: "↑",
            keyboard.Key.down: "↓",
            keyboard.Key.delete: "⌦",
            keyboard.Key.home: "↖",
            keyboard.Key.end: "↘",
            keyboard.Key.page_up: "⇞",
            keyboard.Key.page_down: "⇟"
        }

    def _on_press(self, key):
        """处理按键事件"""
        if not self.running:
            return False

        try:
            # 获取按键文本
            if hasattr(key, 'char'):
                key_text = key.char
            else:
                key_text = self.special_keys.get(key, str(key).replace('Key.', ''))

            # 如果有回调函数，调用它
            if self.callback:
                self.callback(key_text)

            # ESC键退出
            if key == keyboard.Key.esc:
                self.stop()
                return False

        except Exception as e:
            pass

    def start(self):
        """启动键盘监听"""
        if not self.running:
            self.running = True
            self.listener = keyboard.Listener(on_press=self._on_press)
            self.listener.start()

    def stop(self):
        """停止键盘监听"""
        self.running = False
        if self.listener:
            self.listener.stop()
            self.listener = None


class KeyDisplayConfig:
    """键盘显示配置类"""

    def __init__(self, config_file='config.json'):
        self._set_defaults()

        # 获取配置文件的绝对路径
        self.config_path = os.path.join(get_app_root(), config_file)

        # 尝试从配置文件加载
        self.load_config(self.config_path)

    def _set_defaults(self):
        """设置默认配置"""
        # 显示相关
        self.font_name = 'Arial Bold'
        self.font_size = 32
        self.max_chars = 15
        self.text_color = 'white'
        self.bg_color = '#000000'
        self.opacity = 0.8

        # 窗口相关
        self.window_width = 400
        self.window_height = 60
        self.window_padding_x = 10
        self.window_padding_y = 5

        # 性能相关
        self.update_delay = 1
        self.topmost_check_interval = 100

        # 历史记录
        self.keep_history = True
        self.history = []
        self.history_max_len = 15

        # 添加淡出效果配置
        self.fade_interval = 100  # 淡出效果更新间隔（毫秒）
        self.fade_duration = 3.0  # 开始淡出前的等待时间（秒）
        self.fade_step = 0.05  # 每次淡出的不透明度减少量
        self.fade_enabled = True  # 是否启用淡出效果

    def load_config(self, config_path):
        """从JSON文件加载配置"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # 更新显示配置
                display = config.get('display', {})
                self.font_name = display.get('font_name', self.font_name)
                self.font_size = display.get('font_size', self.font_size)
                self.max_chars = display.get('max_chars', self.max_chars)
                self.text_color = display.get('text_color', self.text_color)
                self.bg_color = display.get('bg_color', self.bg_color)
                self.opacity = display.get('opacity', self.opacity)

                # 更新窗口配置
                window = config.get('window', {})
                self.window_width = window.get('width', self.window_width)
                self.window_height = window.get('height', self.window_height)
                self.window_padding_x = window.get('padding_x', self.window_padding_x)
                self.window_padding_y = window.get('padding_y', self.window_padding_y)

                # 更新性能配置
                performance = config.get('performance', {})
                self.update_delay = performance.get('update_delay', self.update_delay)
                self.topmost_check_interval = performance.get('topmost_check_interval',
                                                              self.topmost_check_interval)

                # 更新历史记录配置
                history = config.get('history', {})
                self.keep_history = history.get('enabled', self.keep_history)
                self.history_max_len = history.get('max_length', self.history_max_len)

                # 加载淡出效果配置
                fade = config.get('fade_effect', {})
                self.fade_interval = fade.get('interval', self.fade_interval)
                self.fade_duration = fade.get('duration', self.fade_duration)
                self.fade_step = fade.get('step', self.fade_step)
                self.fade_enabled = fade.get('enabled', self.fade_enabled)
            else:
                self.save_config(config_path)  # 保存默认配置

        except Exception:
            pass

    def save_config(self, config_file):
        """保存配置到JSON文件"""
        try:
            config = {
                'display': {
                    'font_name': self.font_name,
                    'font_size': self.font_size,
                    'max_chars': self.max_chars,
                    'text_color': self.text_color,
                    'bg_color': self.bg_color,
                    'opacity': self.opacity
                },
                'window': {
                    'width': self.window_width,
                    'height': self.window_height,
                    'padding_x': self.window_padding_x,
                    'padding_y': self.window_padding_y
                },
                'performance': {
                    'update_delay': self.update_delay,
                    'topmost_check_interval': self.topmost_check_interval
                },
                'history': {
                    'enabled': self.keep_history,
                    'max_length': self.history_max_len
                },
                'fade_effect': {
                    'interval': self.fade_interval,
                    'duration': self.fade_duration,
                    'step': self.fade_step,
                    'enabled': self.fade_enabled
                }
            }

            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception:
            pass


class KeyDisplay:
    def __init__(self, config=None):
        self.config = config or KeyDisplayConfig()

        # 创建主窗口
        self.root = tk.Tk()

        # 设置窗口属性
        self.root.attributes(
            '-topmost', True,
            '-alpha', self.config.opacity,
            '-transparent', True
        )

        # 移除窗口边框和标题栏
        self.root.overrideredirect(True)

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 设置窗口大小和位置
        x = (screen_width - self.config.window_width) // 2
        y = screen_height - self.config.window_height - 100
        self.root.geometry(f'{self.config.window_width}x{self.config.window_height}+{x}+{y}')

        # 设置窗口背景为透明
        try:
            # 尝试使用系统透明色
            if sys.platform == 'darwin':  # macOS
                try:
                    self.root.configure(bg='systemTransparent')
                    self.label_bg = 'systemTransparent'
                except:
                    self.root.configure(bg='black')
                    self.label_bg = 'black'
            else:  # Windows/Linux
                self.root.configure(bg='black')
                self.label_bg = 'black'

            # 设置窗口透明度
            self.root.attributes('-alpha', self.config.opacity)

        except Exception:
            self.root.configure(bg='black')
            self.label_bg = 'black'

        # 创建标签
        self.label = tk.Label(
            self.root,
            text="等待输入...",
            font=(self.config.font_name, self.config.font_size),
            fg=self.config.text_color,
            bg=self.label_bg,  # 使用系统特定的透明色
            width=self.config.max_chars
        )
        self.label.pack(expand=True, fill='both', padx=self.config.window_padding_x,
                        pady=self.config.window_padding_y)

        # 创建键盘监控器
        self.keyboard_monitor = KeyboardMonitor(callback=self.update_label)

        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 绑定拖动事件
        self.label.bind('<Button-1>', self.start_move)
        self.label.bind('<B1-Motion>', self.on_move)

        # 标记程序是否运行
        self.running = True

        # 设置样式
        self.update_style()

        # 启动置���检查
        self.check_topmost()

        # 添加淡出相关的属性
        self.last_input_time = time.time()
        self.fade_timer = None
        self.window_opacity = 1.0

        # 从配置中读取淡出效果设置
        if self.config.fade_enabled:
            self.check_fade()

    def check_topmost(self):
        """定期检查并确保窗口保持在最顶层"""
        if self.running:
            try:
                self.root.lift()
                self.root.attributes('-topmost', 1)
            except Exception:
                pass
            finally:
                self.root.after(self.config.topmost_check_interval, self.check_topmost)

    def update_style(self):
        """更新窗口样式"""
        try:
            # 尝试设��窗口圆角（仅在 macOS 上有效）
            if sys.platform == 'darwin':
                from Foundation import NSUserDefaults
                defaults = NSUserDefaults.standardUserDefaults()
                defaults.setObject_forKey_('YES', 'AppleEnableSwipeNavigateWithScrolls')

            # 设置标签样式
            self.label.configure(
                relief='flat',
                padx=10,
                pady=5
            )
        except Exception:
            pass

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_label(self, text):
        """更新标签显示"""
        try:
            # 重置最后输入时间和不透明度
            self.last_input_time = time.time()
            self.window_opacity = 1.0
            self.root.attributes('-alpha', self.config.opacity)

            if self.config.keep_history:
                # 如果窗口已经开始淡出，清除历史后再添加新输入
                if self.window_opacity < 1.0:
                    self.config.history.clear()

                # 更新历史记录
                self.config.history.append(text)
                if len(self.config.history) > self.config.history_max_len:
                    self.config.history.pop(0)

                # 显示最近的按键历史
                display_text = ' '.join(self.config.history)
            else:
                display_text = text

            # 限制显示长度
            if len(display_text) > self.config.max_chars:
                display_text = display_text[-self.config.max_chars:]

            # 更新显示
            self.root.after(self.config.update_delay,
                            lambda: self.label.config(text=display_text))
            self.root.update()
        except Exception:
            pass

    def on_closing(self):
        """处理窗口关闭事件"""
        self.keyboard_monitor.stop()
        self.running = False
        self.root.quit()

    def run(self):
        """运行显示程序"""
        # 启动键盘监听
        self.keyboard_monitor.start()
        # 运行主循环
        self.root.mainloop()

    def update_config(self, **kwargs):
        """更新配置"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

        # 更新显示
        self.label.configure(
            font=(self.config.font_name, self.config.font_size),
            fg=self.config.text_color,
            bg=self.label_bg,  # 使用系统特定的透明色
            width=self.config.max_chars
        )
        self.root.attributes('-alpha', self.config.opacity)
        self.label.pack_configure(padx=self.config.window_padding_x,
                                  pady=self.config.window_padding_y)

    def check_fade(self):
        """检查是否需要开始淡出效果"""
        if self.running and self.config.fade_enabled:
            current_time = time.time()
            time_since_last_input = current_time - self.last_input_time

            # 如果超过等待时间且窗口还可见
            if time_since_last_input >= self.config.fade_duration and self.window_opacity > 0:
                # 清除历���记录
                if self.config.keep_history:
                    self.config.history.clear()
                # 执行淡出
                self.fade_text()
            elif time_since_last_input < self.config.fade_duration:
                # 如果有新输入，恢复窗口不透明度
                if self.window_opacity < 1.0:
                    self.window_opacity = 1.0
                    self.root.attributes('-alpha', self.window_opacity * self.config.opacity)

            # 继续检查
            self.root.after(self.config.fade_interval, self.check_fade)

    def fade_text(self):
        """执行淡出效果"""
        if self.window_opacity > 0:
            self.window_opacity = max(0, self.window_opacity - self.config.fade_step)
            self.root.attributes('-alpha', self.window_opacity * self.config.opacity)


if __name__ == "__main__":
    try:
        # 确保在正确的目录下运行
        app_root = ensure_app_directory()

        # 从配置文件加载配置
        config = KeyDisplayConfig('config.json')

        # 创建显示器实例
        app = KeyDisplay(config)

        # 运行程序
        app.run()
    except Exception as e:
        if isinstance(e, OSError) and "Input monitoring is not allowed" in str(e):
            print("\n权限错误：无法监控键盘输入。请确保已在系统设置中授予必要的权限。")
        sys.exit(1)