# web 调研 - 火山 RTC Web Demo

## 调研信息
- 调研时间：2026-04-21
- 状态：进行中
- 参考文档：
  - https://www.volcengine.com/docs/6348/77374?lang=zh
  - https://www.volcengine.com/docs/6348/106914?lang=zh

## 官方 Demo 信息

| 项目 | 说明 |
|------|------|
| **文件名** | VolcengineRTC_QuickStart_Web_4.66_ReactDemo.zip |
| **框架** | React |
| **版本** | 4.66 |
| **SDK** | @volcengine/rtc |
| **端口** | 5173 (Vite 默认) |

## 目录结构

```
src/web/
├── src/
│   ├── components/      # 组件
│   ├── utils/           # 工具函数
│   ├── App.tsx          # 主应用
│   └── main.tsx         # 入口
├── public/              # 静态资源
├── index.html           # HTML 入口
├── vite.config.ts       # Vite 配置
├── tsconfig.json        # TypeScript 配置
├── package.json         # 依赖管理
└── README.md            # 说明文档
```

## 当前目标

1. 原封不动提交官方 Demo
2. 配置火山 AppId/Token
3. 成功运行 Demo

## 待确认

- [ ] AppId 获取方式
- [ ] Token 生成方式
- [ ] 端口部署配置
