# 🌐 EIM 网页图标 (Favicon) 快速替换指南

本指南用于在开发 EIM 相关项目（如 Hub, Invoice, Schedule 等）时，快速配置或更换浏览器标签页的小图标。

---

## 🚀 核心替换代码 (Quick Copy)

在项目的 `index.html` 文件中，找到 `<title>` 标签（域名名字），在其下方直接粘贴以下对应代码：

### 🔹 选项 A：更换为 EIM 标准图标 (Dark Blue)
```html
<link rel="icon" href="https://github.com/Terback/Images/blob/main/logo/icon_darkblue.png?raw=true" />
```

### 🔹 选项 B：更换为 TerMade 标准图标
```html
<link rel="icon" href="https://github.com/Terback/Images/blob/main/logo/TermadeEIM.png?raw=true" />
```


Example:

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EIM Invoice Generator</title>
    <link rel="icon" href="https://github.com/Terback/Images/blob/main/logo/icon_darkblue.png?raw=true" />
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.31/jspdf.plugin.autotable.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
```
