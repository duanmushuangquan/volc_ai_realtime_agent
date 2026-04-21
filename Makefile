# Makefile - 火山 RTC AI 机器人控制系统

.PHONY: help new-research new-plan show-plan done test test-unit test-integration build lint sync-push sync-pull download-sdk ci clean

# 默认目标
help:
	@echo "火山 RTC AI 机器人控制系统 - Makefile"
	@echo ""
	@echo "=== 调研与计划 ==="
	@echo "  make new-research TOPIC=<topic>   # 创建调研文档"
	@echo "  make new-plan TOPIC=<topic>       # 创建计划文档"
	@echo "  make show-plan TOPIC=<topic>       # 显示计划进度"
	@echo "  make done TASK=N TOPIC=<topic>    # 标记任务完成"
	@echo ""
	@echo "=== 开发 ==="
	@echo "  make build                       # 编译项目"
	@echo "  make test                        # 运行所有测试"
	@echo "  make test-unit                   # 运行单元测试"
	@echo "  make test-integration            # 运行集成测试"
	@echo "  make lint                        # 代码检查"
	@echo ""
	@echo "=== 云电脑同步 ==="
	@echo "  make sync-push                   # 推送到云电脑"
	@echo "  make sync-pull                   # 从云电脑拉取"
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
	@echo "  make done TASK=1 TOPIC=volc_rtc"

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

# ============ 云电脑同步 ============

sync-push:
	@bash scripts/sync-push.sh

sync-pull:
	@bash scripts/sync-pull.sh

# ============ 火山 SDK ============

download-sdk:
ifndef PRODUCT
	$(error PRODUCT is required. Usage: make download-sdk PRODUCT=<product>)
endif
	@bash scripts/download-sdk.sh $(PRODUCT)

# ============ CI/CD ============

ci:
	@bash scripts/ci.sh

clean:
	@bash scripts/clean.sh
