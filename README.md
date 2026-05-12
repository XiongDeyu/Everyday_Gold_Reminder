# Everyday_Gold_Reminder

每日金价提醒 Agent。

## 功能

- 请求实时金价（默认：`https://api.gold-api.com/price/XAU`）
- 输出每日提醒消息（可配置提醒阈值）
- 支持通过 GitHub Actions 每日自动执行

## 本地运行

```bash
python gold_reminder_agent.py
python gold_reminder_agent.py --threshold 2300
python gold_reminder_agent.py --mock-price 2400
```

## 运行测试

```bash
python -m unittest discover -v
```

## 自动提醒

仓库包含工作流：`.github/workflows/daily_gold_reminder.yml`

- 每天 UTC 00:00 自动运行
- 支持手动触发（`workflow_dispatch`）
