# SSH密钥资产台账
规则：一台设备仅1套密钥，每条记录对应一台电脑；新增部署公钥立刻更新本表；设备报废直接按本条批量删除所有公钥

## 条目1：Win_taikang工作机（id_rsa_vps_willjay）
- 密钥指纹：【ssh-keygen -lf ~/.ssh/id_rsa_vps_willjay.pub 复制输出指纹】
- 生成时间：2026-06-24
- 本机私钥文件：id_rsa_vps_willjay
- 公钥部署位置清单（丢机器要全部删除）：
  1. GitHub账号 → SSH Keys 标题：wintaikang
  2. VPS服务器 123.45.67.89 用户root → authorized_keys
- 状态：在用

## 条目2：Linux学习机（id_rsa_linux_vps）
- 密钥指纹：xxx
- 生成时间：2026-06-24
- 本机私钥文件：id_rsa_linux_vps
- 公钥部署位置：
  1. GitHub账号 → SSH Keys 标题：Vps_Ubuntu
- 状态：在用

## 废弃记录（机器淘汰/重装）
- 旧笔记本2024：已全部删除GitHub、云服务器公钥，作废日期2025-12