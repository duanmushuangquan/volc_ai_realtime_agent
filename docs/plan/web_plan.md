# web 实施计划 - 火山 RTC Web Demo

## 背景
- 官方 Demo 已下载，需要跑通验证
- 作为 Web 部分迭代起点

## 阶段目标
跑通火山 RTC Web Demo，验证实时音视频功能

---

## 子任务清单

### [x] Task 1: 提交官方 Demo
**目标**: 将官方 Demo 原封不动提交到 Git

**实施方案**:
1. 解压 `VolcengineRTC_QuickStart_Web_4.66_ReactDemo.zip`
2. 整理目录结构到 `src/web/`
3. 清理临时文件
4. 提交 Git

**验收标准**:
- [x] Demo 代码已提交
- [x] `.gitignore` 已配置

---

### [ ] Task 2: 配置火山参数
**目标**: 配置 AppId 和 Token

**实施方案**:
1. 创建 `config/volc.json` 配置模板
2. 修改 Demo 代码读取配置
3. 填入火山控制台获取的 AppId

**验收标准**:
- [ ] config/volc.json 存在
- [ ] Demo 能读取配置

**文件改动**:
- `config/volc.json` (新增)
- `src/web/src/` (修改)

---

### [ ] Task 3: 安装依赖
**目标**: 安装 npm 依赖

**实施方案**:
1. `cd src/web && pnpm install`
2. 验证 node_modules

**验收标准**:
- [ ] node_modules 存在
- [ ] 无致命错误

---

### [ ] Task 4: 运行 Demo
**目标**: 本地运行 Web Demo

**实施方案**:
1. `cd src/web && pnpm dev`
2. 访问页面
3. 加入房间测试

**验收标准**:
- [ ] 页面正常打开
- [ ] 能加入房间
- [ ] 能看到本地视频

---

### [ ] Task 5: 部署验证
**目标**: 验证 Coze 沙箱部署

**实施方案**:
1. 使用 Coze CLI 启动服务
2. 确认端口可用

**验收标准**:
- [ ] 服务可访问
- [ ] 外部可访问（如需要）

---

## 执行记录

| 日期 | 完成任务 | 状态 |
|------|----------|------|
| 2026-04-21 | Task 1: 提交官方 Demo | ✅ |
| 2026-04-21 | Task 2: 配置火山参数 | ⏳ |
| 2026-04-21 | Task 3: 安装依赖 | ⏳ |
| 2026-04-21 | Task 4: 运行 Demo | ⏳ |
| 2026-04-21 | Task 5: 部署验证 | ⏳ |

---

## 命令清单

```bash
# 安装依赖
cd src/web && pnpm install

# 开发模式
cd src/web && pnpm dev

# 构建
cd src/web && pnpm build
```
