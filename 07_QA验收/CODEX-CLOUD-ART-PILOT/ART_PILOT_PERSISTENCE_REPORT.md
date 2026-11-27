# REI-PET-ART-PILOT-PERSIST｜专项持久化报告

## 状态

`ART_PIPELINE_TECHNICAL_PASS` · `PENDING_VISUAL_ACCEPTANCE`

基准为 `feat/p4b-review-center-v1` 的 `6fd635a3d83336a4b5445e021a7f0eddfdf39fc6`。10 张试验帧只有 `ART_CANDIDATE` 资格。它们有独立的人工验收记录，并且未加入 171 帧候选清单、正式图集或 P4-C 进度。

## 原图及 Alpha 证据

三个原始 PNG 与云端专项试验交付文件逐字节一致。以下计数为整张源图中实际从 Alpha 1/255 改为 0 的像素数。前后 RGBA 像素 SHA-256 对未编码的像素缓冲计算，原始 PNG SHA-256 单独记录。此步骤保留 RGB 与其他 Alpha 值。每张标准帧另有像素 SHA-256 和 PNG 文件 SHA-256。

| 原图 | 阈值 | 清理像素数 | 结果 |
| --- | ---: | ---: | --- |
| 校服 waiting attempt-01 | 1/255 | 235,178 | 6 帧 `STRUCTURE_PASS` |
| 黑服四方向 attempt-01 | 1/255 | 17,552 | `FAILED`，源图边界 Alpha 最大为 2/255 |
| 黑服四方向 attempt-02 | 1/255 | 76,705 | 4 帧 `STRUCTURE_PASS` |

Alpha 清理记录和输入、输出哈希见 [专项资产清单](CODEX_CLOUD_ART_PILOT_MANIFEST.json)。按 [SHA256SUMS](SHA256SUMS) 校验持久化文件。按原条件复跑脚本后，10 张通过帧、4 张失败样本登记帧及正式分帧 QA JSON 均与归档逐字节一致。

从仓库根目录复跑时指定独立输出目录，例如：

```bash
pilot="07_QA验收/CODEX-CLOUD-ART-PILOT"
out="$(mktemp -d)"
PYTHONDONTWRITEBYTECODE=1 python3 "$pilot/pilot_qa.py" --root . --out-dir "$out" \
  waiting "$pilot/raw/waiting-attempt-01.png" --attempt attempt-01
```

## 保护范围

`rei_atlas_tools.py verify` 通过 6 份冻结原画及备份、3 份派生母版、171 帧及 3 套标准图集。与指定基准的路径比较也确认，冻结目录、三套角色资产目录、正式资产清单、恢复矩阵及 Review Center 正式数据与代码均一致。试验未生成新素材。

[Review Center 增量 QA 报告](REVIEW_CENTER_PILOT_QA_REPORT.md) · [专项试验报告](CODEX_CLOUD_ART_PILOT_REPORT.md) · [云端能力报告](CODEX_CLOUD_CAPABILITY_REPORT.md)
