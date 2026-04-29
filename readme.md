## Shadowrocket 规则 · 个人 Fork

本仓库 Fork 自 [Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever)，在原项目基础上添加了个人定制规则，通过手动触发 GitHub Actions 更新发布。

## 规则列表

规则 | 说明
--- | ---
[国内外划分 + 去广告](https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/sr_cnip_ad.conf) | 国内直连，国外代理，含广告过滤
[国内外划分](https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/sr_cnip.conf) | 国内直连，国外代理
[仅去广告](https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/sr_ad_only.conf) | 仅广告过滤规则，无分流
[懒人配置 + 广告](https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/lazy_ad.conf) | 开箱即用，含广告过滤、自定义规则注入
[懒人配置](https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/lazy.conf) | 开箱即用，含自定义规则注入
[懒人配置-含策略组 + 广告](https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/lazy_group_ad.conf) | 含代理分组、广告过滤、自定义规则注入
[懒人配置-含策略组](https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/lazy_group.conf) | 含代理分组、自定义规则注入

局域网请求均直连。

## 自定义规则

在 `factory/custom_rules.conf` 中添加规则，格式同 Shadowrocket `[Rule]` 条目（如 `DOMAIN-SUFFIX,example.com,DIRECT`）。构建时会以最高优先级注入到全部规则文件的 `[Rule]` 顶部。

## 鸣谢与来源

- 原始项目：[h2y/Shadowrocket-ADBlock-Rules](https://github.com/h2y/Shadowrocket-ADBlock-Rules)
- 维护分支：[Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever)
- 懒人规则来源：[LOWERTOP/Shadowrocket](https://github.com/LOWERTOP/Shadowrocket)
- [gfwlist](https://github.com/gfwlist/gfwlist)
- [Greatfire Analyzer](https://github.com/Loyalsoldier/cn-blocked-domain)
- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)
- [乘风广告过滤规则](https://github.com/xinggsf/Adblock-Plus-Rule)
- [EasyList China](https://adblockplus.org/)
- [Peter Lowe 广告和隐私跟踪域名](https://pgl.yoyo.org/)
