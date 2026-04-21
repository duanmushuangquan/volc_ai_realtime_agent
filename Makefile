# Makefile - 火山 RTC AI 机器人控制系统

.PHONY: help new-research new-plan show-plan done test test-unit test-integration build lint sync-github sync-trigger sync-all sync-status sync-pull cloud-ssh cloud-webhook download-sdk ci clean

# 云电脑配置
CLOUD_IP := 115.190.107.107
CLOUD_USER := coze
CLOUD_DIR := /home/coze/projects/volc_ai_realtime_agent
SSH_KEY := .ssh/id_ed25519

# 默认目标
help:
	@echo "火山 RTC AI 机器人控制系统 - Makefile"
	@echo ""
	@echo "=== 调研与计划 ==="
	@echo "  make new-research TOPIC=<topic>   # 创建调研文档"
	@echo "  make new-plan TOPIC=<topic>       # 创建计划文档"
	@echo "  make show-plan TOPIC=<topic>      # 显示计划进度"
	@echo "  make done TASK=N TOPIC=<topic>   # 标记任务完成"
	@echo ""
	@echo "=== 开发 ==="
	@echo "  make build                       # 编译项目"
	@echo "  make test                        # 运行所有测试"
	@echo "  make test-unit                   # 运行单元测试"
	@echo "  make test-integration            # 运行集成测试"
	@echo "  make lint                        # 代码检查"
	@echo ""
	@echo "=== 云电脑同步 (Git + Webhook) ==="
	@echo "  make sync-github                # 推送到 GitHub"
	@echo "  make sync-trigger               # 触发云电脑编译"
	@echo "  make sync-all                   # 推送并触发"
	@echo "  make sync-status                # 查看云电脑状态"
	@echo "  make sync-pull                  # 从云电脑拉取"
	@echo ""
	@echo "=== 云电脑操作 ==="
	@echo "  make cloud-ssh                  # SSH 连接到云电脑"
	@echo "  make cloud-webhook              # 在云电脑上启动 Webhook 服务"
	@echo ""
	@echo "=== 火山 SDK ==="
	@echo "  make download-sdk PRODUCT=<product>  # 下载 SDK (rtc|ai)"
	@echo ""
	@echo "=== CI/CD ==="
	@echo "  make ci                          # 本地 CI 检查"
	@echo ""
	@echo "=== 示例 ==="
	@echo "  make new-research TOPIC=volc_rtc"
	@echo "  make new-plan TOPIC=volc_rtc"
	@echo "  make sync-all"

# ============ 调研与计划 ============

new-research:
ifndef TOPIC
	$(error TOPIC is required. Usage: make new-research TOPIC=<topic>)
endif
	@bash scripts/new-research.sh $(TOPIC)

new-plan:
ifndef TOPIC
	$(error TOPIC is required. Usage: make new-plan TOPIC=<topic>)
endif
	@bash scripts/new-plan.sh $(TOPIC)

show-plan:
ifndef TOPIC
	$(error TOPIC is required. Usage: make show-plan TOPIC=<topic>)
endif
	@bash scripts/show-plan.sh $(TOPIC)

done:
ifndef TASK
	$(error TASK is required. Usage: make done TASK=N TOPIC=<topic>)
endif
ifndef TOPIC
	$(error TOPIC is required. Usage: make done TASK=N TOPIC=<topic>)
endif
	@bash scripts/done.sh $(TASK) $(TOPIC)

# ============ 开发 ============

build:
	@bash scripts/build.sh

test:
	@bash scripts/test.sh

test-unit:
	@bash scripts/test-unit.sh

test-integration:
	@bash scripts/test-integration.sh

lint:
	@bash scripts/lint.sh

# ============ 云电脑同步 (Git + Webhook) ============

# 推送到 GitHub
sync-github:
	@echo "推送到 GitHub..."
	@git add -A && git commit -m "chore: sync from Coze sandbox" && git push origin main

# 触发云电脑编译 (通过 HTTP Webhook)
sync-trigger:
	@echo "触发云电脑编译..."
	@curl -s -X POST http://$(CLOUD_IP):8000/webhook/git || echo "Webhook 不可用，请在云电脑上运行: python3 scripts/cloud_build.py --webhook"

# 推送并触发 (完整流程)
sync-all: sync-github sync-trigger
	@echo "完成! 云电脑正在编译..."

# 查看云电脑状态
sync-status:
	@curl -s http://$(CLOUD_IP):8000/status 2>/dev/null || echo "状态服务不可用"

# 从云电脑拉取
sync-pull:
	@echo "从云电脑拉取..."
	@scp -i $(SSH_KEY) $(CLOUD_USER)@$(CLOUD_IP):$(CLOUD_DIR)/build_status.json . 2>/dev/null || echo "拉取失败"
	@cat build_status.json 2>/dev/null || echo "无状态文件"

# SSH 连接到云电脑
cloud-ssh:
	@ssh -i $(SSH_KEY) -o StrictHostKeyChecking=no $(CLOUD_USER)@$(CLOUD_IP)

# 在云电脑上启动 Webhook 服务
cloud-webhook:
	@ssh -i $(SSH_KEY) $(CLOUD_USER)@$(CLOUD_IP) "cd $(CLOUD_DIR) && python3 scripts/cloud_build.py --webhook"

# ============ 火山 SDK ============

download-sdk:
ifndef PRODUCT
	$(error PRODUCT is required. Usage: make download-sdk PRODUCT=<product>)
endif
	@bash scripts/download-sdk.sh $(PRODUCT)

# ============ CI/CD ============

ci:
	@bash scripts/ci.sh

# ============ 清理 ============

clean:
	@bash scripts/clean.sh
