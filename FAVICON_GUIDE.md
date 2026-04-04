# 🌐 EIM 网页小图标 (Favicon) 快速替换指南

本指南用于在开发 EIM 相关项目时，快速配置浏览器标签页的小图标。

---

## 1. 快速引用地址 (CDN)

从 GitHub 引用时，**必须**在 URL 末尾保留 `?raw=true` 确保返回的是图片原始文件。

| 品牌 / 项目 | 图标描述 | 引用地址 (Direct Link) |
| :--- | :--- | :--- |
| **EIM Technology** | 深蓝标准图标 (Dark Blue) | `https://github.com/Terback/Images/blob/main/logo/icon_darkblue.png?raw=true` |
| **TerMade** | TerMade EIM 混合标志 | `https://github.com/Terback/Images/blob/main/logo/TermadeEIM.png?raw=true` |

---

## 2. 代码集成方式

### 🔹 标准 HTML (index.html)
在 `<head>` 标签内添加以下代码：

```html
<link rel="icon" type="image/png" href="[https://github.com/Terback/Images/blob/main/logo/icon_darkblue.png?raw=true](https://github.com/Terback/Images/blob/main/logo/icon_darkblue.png?raw=true)" />
