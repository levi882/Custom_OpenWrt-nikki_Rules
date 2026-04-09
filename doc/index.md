Welcome to the Custom_OpenWrt-nikki_Rules wiki!

# 写在前面：

确认你固件的防火墙是firewall4(nftables)才行！

```bash
opkg list-installed | grep firewall
```

```bash
apk info | grep firewall
```

✅：

<img src="https://github.com/user-attachments/assets/0735bf92-dfb5-4032-b979-ec7370ae82e4" style="max-width:100%; height:auto;">

<img src="https://github.com/user-attachments/assets/1f5d3a4c-22a6-44db-ae22-524a15363fc6" style="max-width:100%; height:auto;">

<img src="https://github.com/user-attachments/assets/1dd86e04-57ed-407a-bcef-4b42308028fc" style="max-width:100%; height:auto;">

❌：

<img src="https://github.com/user-attachments/assets/ce97e4d5-3cb1-4f71-aacb-f1ad422d8c4f" style="max-width:100%; height:auto;">

需要搭配 `Aethersailor/Custom_OpenClash_Rules` 的模板才能实现相同的效果！

仓库模板地址如下：

[Aethersailor/Custom_OpenClash_Rules/Custom_Clash.ini](https://raw.githubusercontent.com/Aethersailor/Custom_OpenClash_Rules/refs/heads/main/cfg/Custom_Clash.ini)

# Openwrt-Nikki下载地址：

[OpenWrt-nikki/releases](https://github.com/nikkinikki-org/OpenWrt-nikki/releases/)

<img src="https://github.com/user-attachments/assets/bd8d0a8c-947f-4f31-82b7-344c8e5e52ee" style="max-width:100%; height:auto;">

<img src="https://github.com/user-attachments/assets/d06accb6-144a-4ed1-8318-12d92f9fe390" style="max-width:100%; height:auto;">


!!! tip
    提示：
    图片看不清楚请对图片右键-`在新标签页中打开图像`


!!! note
    **声明事项：**
    
    - wiki设置主要面向使用`openwrt主路由拨号`的使用方式，因此wiki的设置仅供参考，实际的设置请以自身的需求出发来更改
    - wiki设置仅为个人经验的总结性示例，不具权威性，并非 `nikki` 的唯一使用方式。
    - wiki设置为自用目的，且个人时间有限，只能随缘更新，且鉴于`mihomo内核`更新迭代很快，更多的仍然是去参考`mihomo内核`的wiki:[wiki](https://wiki.metacubex.one/)。


!!! warning
    **使用须知：同[⚠️ 特别声明](https://github.com/Aethersailor/Custom_OpenClash_Rules?tab=readme-ov-file#%EF%B8%8F-%E7%89%B9%E5%88%AB%E5%A3%B0%E6%98%8E)**


<h2>📘 教程索引</h2>
<table>
  <thead>
    <tr><th>章节</th><th>内容简介</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>OpenWrt-nikki 设置方案</td>
      <td><a href="https://levi882.github.io/Custom_OpenWrt-nikki_Rules/1.Openwrt-nikki/">查看详细内容</a></td>
</table>
