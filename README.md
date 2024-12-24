# KeyBoard Monitor

一个实时显示键盘输入的悬浮窗口工具，支持优雅的显示效果和丰富的自定义配置。

## 主要功能

- 实时显示键盘输入
- 支持特殊按键的符号显示（如空格、回车、方向键等）
- 可拖动的半透明悬浮窗口
- 支持按键历史记录显示
- 智能淡出效果
- 高度可定制化的配置

## 配置说明

配置文件为 `config.json`，包含以下主要配置项：

### 显示配置 (display)

| 参数 | 说明 | 默认值 |
|------|------|--------|
| font_name | 字体名称 | Arial Bold |
| font_size | 字体大小（像素） | 28 |
| max_chars | 最大显示字符数 | 20 |
| text_color | 文字颜色（支持颜色名或十六进制） | white |
| bg_color | 背景颜色 | systemTransparent |
| opacity | 窗口整体透明度 (0.0-1.0) | 0.9 |

### 窗口配置 (window)

| 参数 | 说明 | 默认值 |
|------|------|--------|
| width | 窗口宽度（像素） | 400 |
| height | 窗口高度（像素） | 60 |
| padding_x | 文字水平内边距（像素） | 10 |
| padding_y | 文字垂直内边距（像素） | 5 |

### 性能配��� (performance)

| 参数 | 说明 | 默认值 |
|------|------|--------|
| update_delay | 显示更新延迟（毫秒） | 2 |
| topmost_check_interval | 窗口置顶检查间隔（毫秒） | 100 |

### 历史记录配置 (history)

| 参数 | 说明 | 默认值 |
|------|------|--------|
| enabled | 是否启用按键历史记录 | true |
| max_length | 历史记录最大长度 | 10 |

### 淡出效果配置 (fade_effect)

| 参数 | 说明 | 默认值 |
|------|------|--------|
| interval | 淡出效果更新间隔（毫秒） | 100 |
| duration | 开始淡出前的等待时间（秒） | 3.0 |
| step | 每次淡出的不透明度减少量 (0.02-0.1) | 0.05 |
| enabled | 是否启用淡出效果 | true |

## 特殊按键显示

程序会将特殊按键转换为易读的符号显示：

- 空格键 → ␣
- 回车键 → ⏎
- 退格键 → ⌫
- Tab键 → ⇥
- Esc键 → ⎋
- Shift键 → ⇧
- Ctrl键 → ⌃
- Alt键 → ⌥
- Caps Lock → ⇪
- 方向键 → ←↑→↓
- 删除键 → ⌦
- Home键 → ↖
- End键 → ↘
- Page Up → ⇞
- Page Down → ⇟

## 使用说明

1. 确保已安装必要的Python依赖
2. 运行程序后会在屏幕底部显示一个半透明窗口
3. 可以通过鼠标拖动调整窗口位置
4. 按ESC键可以退出程序
5. 配置文件修改后会自动生��

## 注意事项

- 程序需要键盘监听权限
- 建议根据实际需求调整配置参数
- 如果遇到性能问题，可以适当调整update_delay和topmost_check_interval参数 