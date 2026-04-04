# Vercel 子域名迁移与 Cloudflare DNS 配置指南 🌐

本文档记录了如何将托管在 **Vercel** 的项目绑定到由 **Cloudflare** 解析的子域名（例如 `hub.eimtechnology.com`）。

---

## 🛠 配置流程

### 第一步：在 Vercel 中绑定域名
1. 登录 [Vercel Dashboard](https://vercel.com/)，选择目标项目。
2. 进入 **Settings** > **Domains**。
3. 输入完整域名：`hub.eimtechnology.com`，点击 **Add**。
4. **获取记录信息**：Vercel 会提示 `Invalid Configuration`，记录下推荐的 **CNAME** 信息：
   - **Type**: `CNAME`
   - **Name**: `hub`
   - **Value**: `cname.vercel-dns.com`

---

### 第二步：在 Cloudflare 中配置 DNS
1. 登录 [Cloudflare](https://dash.cloudflare.com/)，进入 `eimtechnology.com` 控制台。
2. 点击 **DNS** > **Records** > **Add record**。
3. 填写以下信息：
   - **Type**: `CNAME`
   - **Name**: `hub`
   - **Target**: `cname.vercel-dns.com`
   - **Proxy status**: 💡 **重要：** 初始配置请设置为 **DNS Only** (灰色小云朵)。
     > *注：Vercel 需要直接验证解析以签发 SSL 证书。待 Vercel 侧显示 Active 后，可根据需要重新开启橙色云朵。*
4. 点击 **Save**。

---

### 第三步：验证与生效
1. 返回 Vercel 的 Domains 页面。
2. 点击 **Refresh**，等待状态变为绿色的 `Valid Configuration`。
3. 确认 **SSL** 状态显示为 `Active`。

---

## ⚠️ 常见问题排查 (Troubleshooting)

### 1. 出现 "Too many redirects" (重定向循环)
**现象**：浏览器提示重定向次数过多，无法打开页面。
**解决**：
- 检查 Cloudflare 的 **SSL/TLS** 设置。
- **必须**将加密模式设置为 **Full** 或 **Full (Strict)**。
- **原因**：Vercel 强制 HTTPS，若 Cloudflare 设为 *Flexible*，会尝试用 HTTP 请求 Vercel，导致无限循环。

### 2. DNS 更改未生效
**确认**：使用终端命令检查解析是否指向 Vercel：
```bash
nslookup hub.eimtechnology.com
