# [07] Xray文档level-0内容讲解

- 消息数: 12
- 类型: 其他

## 摘要

**Conversation overview**

The person engaged in a technical learning session focused on understanding the Xray proxy tool documentation from a GitHub repository (ricuhkaen/Xray-docs-next), specifically the "level-0" beginner tutorial series titled "小小白白话文" (Plain-language Guide for Beginners). The conversation was entirely in Chinese and centered on building foundational knowledge about self-hosting a VPS-based proxy server.

Claude began by fetching and summarizing all nine chapters of the tutorial, providing a structured overview with a visual SVG roadmap diagram showing the complete learning path: from an introductory analysis of proxy options (Chapter 1), through VPS and domain preparation (Chapter 2), SSH remote login and Linux basics (Chapter 3), security hardening (Chapter 4), website setup with Nginx (Chapter 5), TLS certificate management with acme.sh (Chapter 6), Xray server configuration (Chapter 7), Xray client configuration (Chapter 8), and a reference appendix (Chapter 9). The person then stated they were unfamiliar with much of the knowledge covered, which led to deeper dives into specific chapters.

The person requested detailed explanations of three specific chapters in sequence. For Chapter 4 (security hardening), Claude explained the threat model of automated SSH scanning and walked through the four hardening steps: changing the default SSH port from 22, creating a non-root user with sudo privileges, disabling root remote login, and replacing password authentication with RSA key pairs. An interactive SVG widget with clickable buttons for each step was created. For Chapter 6 (TLS certificate management), Claude explained how Let's Encrypt's domain ownership verification works via the ACME webroot challenge, why testing on the staging server first is critical to avoid rate limiting, and walked through the four-stage acme.sh workflow: installation, test issuance, production issuance, and certificate deployment to the Xray directory. For Chapter 7 (Xray server configuration with VLESS+TLS), Claude explained the five config.json modules in detail: log (warning-level logging), dns (DoH encrypted queries via 1.1.1.1), routing (three blocking rules using geoip and geosite databases for private IPs, Chinese IPs, and ad domains), inbounds (VLESS protocol on port 443 with UUID authentication, TLS certificate paths, and the fallback mechanism redirecting non-VLESS traffic to Nginx on port 80 for anti-detection), and outbounds (freedom and blackhole destinations linked to routing via tag names). Claude also covered UUID generation, BBR TCP congestion control enablement, and systemctl service management commands. Throughout, Claude attempted to use an SVG visualization widget, which experienced intermittent failures, causing Claude to fall back to detailed prose explanations with code blocks.

---

## 完整对话

### 🧑 Jace

https://github.com/ricuhkaen/Xray-docs-next/blob/main/docs/document/level-0 给我讲解一下里面的文章呗 让我有一个总体的认识
https://github.com/ricuhkaen/Xray-docs-next/blob/main/docs/document/level-0 给我讲解一下里面的文章呗 让我有一个总体的认识

### 🤖 Claude

The user wants me to fetch the content from a GitHub URL and explain the articles inside. Let me fetch that URL first.
```
This block is not supported on your current device yet.
```

GitHub doesn't allow automated access. Let me try to access the raw content or the tree URL instead.
```
This block is not supported on your current device yet.
```

Let me search for this URL to find the content.
```
This block is not supported on your current device yet.
```

I found a reference to the actual documentation website. Let me fetch the content from xtls.github.io which seems to be the actual documentation site for Xray.好的，我找到了对应的文档网站，让我进一步获取每个章节的内容。
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now I have a good idea of the content structure. Let me fetch several of the chapters to get more detail.
```
This block is not supported on your current device yet.
```

Now I have a good understanding of the first chapter. Let me fetch a few more chapters to get a better overall picture. I'll fetch chapters 2-8 and the appendix.
```
This block is not supported on your current device yet.
```

Good, I'm getting content for each chapter. Let me fetch the other chapters more efficiently by doing them concurrently or getting the main highlights.
```
This block is not supported on your current device yet.
```

The token limit is too small - I'm only getting the navigation. Let me try to get the raw markdown content instead, or increase the token limit. Let me try to get the raw files from GitHub.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

I now have a good overview of all the chapters. Let me also search for the remaining chapters (5, 6, 9) to get more detail.
```
This block is not supported on your current device yet.
```

Now I have enough information about all the chapters. Let me write a comprehensive summary of all 9 chapters and their content.

Here's a summary of what I know:

**Chapter 1 (前言)** - Introduction
- Target audience: zero-experience users wanting to build their own VPS
- Discusses the pros/cons of using "airport" proxy services vs self-building
- Explains why self-building is challenging (requires Linux knowledge, networking protocols, VPS/domain management, TLS certificates)
- Advises on responsible use of the internet after bypassing GFW
**Chapter 2 (原料准备)** - Preparation
- Acquiring a VPS with Debian and registering a domain with proper DNS configuration
- Installing essential tools like SSH clients, file transfer utilities, and code editors

**Chapter 3 (远程登录)** - Remote Login via SSH
- Connecting to the VPS through SSH using platform-specific clients
- Learning fundamental Linux commands for system interaction

**Chapter 4 (安全防护)** - Security
- Hardening the VPS by changing the default SSH port, creating unprivileged user accounts, and switching to key-based authentication instead of passwords

**Chapter 5 (网站建设)** - Website Setup
- Installing Nginx and configuring a basic HTML site that acts as a legitimate front-end to mask the proxy traffic underneath

**Chapter 6 (证书管理)** - Certificate Management
- Using acme.sh to request TLS certificates from Let's Encrypt, which are essential for HTTPS and Xray's security requirements

**Chapter 7 (Xray 服务器)** - Xray Server Configuration
- Setting up Xray with its five core configuration sections: logging, DNS resolution, traffic routing rules, inbound connections, and outbound connections, including rules to filter private IPs and domestic Chinese traffic

**Chapter 8 (Xray 客户端)** - Xray Client Configuration
- Configuring the client-side Xray instance with similar structure, routing foreign domains through foreign DNS servers and domestic domains through domestic DNS, completing the end-to-end setup using VLESS + TLS

**Chapter 9 (附录)** - Appendix
- Reviewing the main concepts from the entire tutorial

Now I'm putting together a visual overview of how all these chapters connect.我已经读取了足够的内容，现在给你做一个完整的讲解。
```
This block is not supported on your current device yet.
```

Now I have the instructions for the visualizer. Let me create a visual overview of all 9 chapters from the "小小白白话文" tutorial. I'll create a clear flow diagram showing the progression from chapter 1 to chapter 9 with a brief description of each.

Let me plan the diagram layout:
- It's a sequential tutorial with 9 chapters (1-9)
- I'll create a vertical flowchart showing the progression
- Each chapter should have a name and a short subtitle
- I'll use colors to group related chapters:
  - Chapter 1 (Intro) in gray
  - Chapter 2 (Preparation) in blue
  - Chapters 3-4 (Linux/SSH/Security) in teal
  - Chapters 5-6 (Website & Certificates) in purple
  - Chapters 7-8 (Xray Server & Client) in amber/coral
  - Chapter 9 (Appendix) in green

I'll design a vertical layout with boxes centered at 100px from the left with 480px width and 60px height for each chapter, with 10px gaps between them and connecting arrows.

Building the SVG diagram... Now I'm laying out the chapters vertically with precise positioning—each box is 56 pixels tall with 20-pixel gaps between them, starting from y=40 and stacking down to a total canvas height of 744 pixels. I'll color-code them by phase: gray for the intro chapter, blue for preparation, and different colors for each subsequent section. Now I'm calculating the actual y-positions for each chapter box with the connecting arrows between them, but the total height is exceeding the viewBox dimensions—I need to compress the spacing to fit everything properly.

Let me try a more compact approach with smaller boxes and tighter gaps, which brings the total down to around 730 pixels. Actually, I think a two-column layout would work better here—I can place chapters 1-5 on the left side and chapters 6-9 on the right side to reduce the overall height.

Wait, that might make the flow confusing. Let me stick with a single column but organize it by phases instead. I'll group the chapters into four main phases—Foundation, Server Setup, Infrastructure, and Xray—plus a Reference section, each with its own color coding. Then I'll create a clean vertical layout with colored boxes that are about 56 pixels tall with 20-pixel gaps between them.

For each box, I'm placing a chapter badge on the left side, the title in the middle, and a subtitle below it. Actually, let me simplify this further—just a straightforward vertical flow with chapter boxes connected by arrows. I'm setting the width to 480 pixels starting at x=100, with each box 52 pixels tall and 18-pixel gaps between them. The chapters will be positioned at regular intervals down the page, ending around y=600 for the last chapter, which gives me a total canvas height of about 692 pixels.

Now I'm checking whether the Chinese text will fit within these constraints. The chapter badges are straightforward, but the titles and subtitles need careful measurement since Chinese characters render wider than Latin text. I'm thinking I should drop the subtitles to keep things clean and avoid overflow issues, focusing just on the chapter number and title for each box. Adding the remaining chapters and simplifying the titles to focus on the main topic, then creating short Chinese subtitles for each section.

Now I'm planning the visual layout with boxes containing badges and text — positioning the numbered circles on the left, titles in a larger font, and subtitles below in a smaller size, accounting for how Chinese characters render at different font sizes.

I'm also organizing the content into five phases with color-coded labels: basic understanding, server preparation, infrastructure setup, Xray deployment, and a final phase.

Now I'm setting up the SVG layout with specific positioning for each chapter, calculating the vertical spacing with gaps between them to create a clear visual flow. I'll set the arrow x-center at 340, then organize the phases with their vertical ranges and midpoints. Rather than adding phase bracket lines which could clutter the diagram, I'm simplifying by using distinct colors to naturally group the chapters together—grays and blues for the first two chapters, teals for chapters three and four, and continuing that color scheme through the remaining sections. Writing SVG code... Writing SVG markup... Writing SVG layout... Calculating the spacing more carefully with a 22px gap between boxes to give the arrows room to breathe, working through the y-positions for all nine chapters to ensure they fit within the 700px viewBox height. Calculating SVG positioning... Simplifying the layout approach...

I'll structure each box with the chapter number on the left, the title centered, and a category tag on the right. The categories map to each chapter—入门 for the intro, 准备 for setup, Linux, 安全, 网站, 证书, 服务端, 客户端, and 总结 for the conclusion. This is getting complicated though, so I'm going to strip it back to something cleaner and more straightforward.

Writing SVG layout... Calculating the SVG viewBox dimensions and positioning the text labels within each box, accounting for the two-line layout with proper vertical centering. For the left badge, I'm placing the chapter number centered in a 40px area with a thin vertical separator, then positioning the title and subtitle to the right starting at x=158 with proper vertical centering using dominant-baseline.

Now I'm checking the text widths to make sure everything fits within the box boundaries—the subtitle with its mix of Chinese characters and punctuation comes to about 195px, the title variations range from 70px to 90px depending on the character mix, so there's plenty of room. Time to write out the full SVG with a medium gray arrow color that'll work across both light and dark modes.

Writing SVG code... Writing SVG markup... I'm reconsidering the layout since adding phase brackets on the right would extend beyond the current diagram width. Rather than cramping everything or adding brackets, I'll use color coding alone to show the phase groupings—it's cleaner and communicates the structure just as effectively. I should also add a legend to explain what the colors represent. I'm refining the chapter subtitles to be punchier and more concise. Each one captures the core concept without extra words, and I'm checking that even the longest ones fit well within the layout constraints.

Writing SVG code... Writing SVG diagram... Writing SVG diagram... Writing SVG code... Writing SVG diagram... Writing SVG diagram... Writing SVG code... Adjusting text positioning within the box using dominant-baseline="central" — placing the title around y=53 and subtitle around y=72 gives roughly 19px spacing between them, which works better than cramming them too close together. I'm verifying the badge positioning at y=62 sits nicely between the title and subtitle, and checking that the separator line from y=46 to y=78 respects the box boundaries with proper padding on both ends. I'm adjusting the spacing between chapters to give the connecting arrows more room—increasing the gap to 22 pixels so the arrowheads don't look cramped, which pushes the total canvas height to 700 pixels and shifts all the subsequent chapter positions accordingly. Verifying the text positioning within each box—the badge sits at the vertical center, the separator line has proper padding, and the title and subtitle are spaced to avoid overlap. Now moving on to the header section. I'm reconsidering the layout approach—skipping the legend to keep things clean, and instead placing chapter numbers as distinct elements on the left side of each box that inherit the box's color styling. I'm also verifying that the CSS variable syntax works properly for subtle separator lines, though I might simplify by removing the line separator altogether for better visual clarity.

Writing SVG layout... I'm running into the limitation that nested color classes lose their styling due to how the direct-child selectors work in SVG. Instead of trying to reference CSS variables for the badge fill, I'll keep it simple by using a semi-transparent white overlay with reduced opacity, or just rely on text weight to make the chapter number stand out without adding a background rect.

Actually, stepping back—the core information I need to convey is the chapter number, title, and what it teaches, with the color groups showing the progression. I can simplify this by placing the chapter number prominently on the left in a heavier weight, followed by the title and subtitle with just spacing between them. No badge box, no separator line—just clean spacing and typography to create visual hierarchy.

I should also think about whether using the same color for adjacent chapters creates confusion about the phase boundaries.

I'm going to use a color scheme where paired chapters share the same color to visually group them—gray for chapter 1 standalone, blue for chapter 2 standalone, then teal for chapters 3 and 4 together, purple for 5 and 6, coral for 7 and 8, and green for chapter 9 standalone. This creates natural visual clustering that shows which chapters are related.

Now I'm building the final SVG and need to check how the Chinese text will render—I'm calculating the width of the longest subtitle to make sure it fits within the layout bounds. I'm working through the vertical positioning for the two-line text blocks inside the boxes. With dominant-baseline set to "central", the text renders from its optical center at the specified y coordinate. For the two-line layout, I need to calculate where each line should sit so the block appears centered within the 52px box height—accounting for the font sizes and spacing between lines. I'm settling on Y+18 and Y+38 for the line centers, which gives nice padding around the text block. Now I'm deciding between using the color ramp classes like c-teal for automatic dark mode support versus raw hex colors—the ramp classes are better since they handle both themes, and using the same color for adjacent boxes like Ch3 and Ch4 creates a visual grouping that makes sense. I also need to make these boxes clickable to trigger sendPrompt.

Writing SVG code... Writing SVG markup... Writing SVG code... Writing SVG markup... Writing SVG diagram... Writing SVG code... Adjusting the text positioning to ensure the two-line block sits properly centered within each box, accounting for the gap between title and subtitle and verifying the spacing stays within bounds. The badge positioning looks right, and I'm verifying the subtitle placement sits properly within each chapter box. Now I'm calculating the total viewBox height based on the last box extending to 664 pixels, plus a 20-pixel margin, giving me 684 for the full height. I want to add a subtle divider between the chapter number and chapter name to improve the visual hierarchy. Writing SVG code... Adding phase labels to boxes... Writing SVG code... I'm recalculating the vertical positions to center everything at the box midpoint instead. By placing the title at box_y+16 and subtitle at box_y+36 with a 20px gap between them, both text elements align around the same center point as the badge. For the first chapter, this puts the title at y=52 and subtitle at y=72, which fits comfortably within the box bounds.

Now I'm finalizing the SVG layout with the viewBox dimensions and positioning all elements—the boxes are spaced 72 pixels apart starting at y=36, arrows connect them at the appropriate transitions, and each box contains the badge, separator line, and centered text labels.

I need to handle the stroke styling for the vertical separator line carefully since the color ramp classes don't explicitly target line elements, so I'll need to set the stroke color directly using a CSS variable.

Actually, thinking about this more—the separator might not be necessary at all. The spacing between the number and text is already substantial enough to create visual separation, so I can just remove the line entirely and rely on that gap.

Now I'm laying out the final structure: nine boxes arranged vertically with consistent spacing, each 52 pixels tall with 20-pixel gaps between them. The boxes use a color scheme that groups related chapters together—gray for the first one, then pairs of blue, teal, purple, and coral, finishing with green. I'm positioning the badges and titles within each box at specific vertical offsets to keep everything aligned.

I'm also adding a subtitle beneath the main title to give context about the tutorial being a complete beginner-to-advanced journey, then adjusting the first box position downward to make room for this additional text element.

Now I've recalculated all the box positions and arrow connections to accommodate the new layout, with the viewBox height set to 700 to give proper spacing. Time to write out the complete SVG. Writing SVG markup... Writing SVG markup... Writing SVG code... Writing SVG nodes... Writing SVG code... Finishing the SVG diagram... I'm considering adding phase labels to the right of each arrow, but they'd be redundant since the arrows already connect same-colored boxes. I'll stick with the clean version without extra annotations.

Let me verify the text follows the style guide—no title case or all caps—and my Chinese titles are fine. Now I'm ready to write the final SVG with loading messages for the widget.

I'm reconsidering how the `<line>` elements interact with the color ramp classes. Lines don't receive ramp fills like rectangles do, so they'll just use default SVG stroke styling. The color ramp classes are really meant for shapes like rectangles and circles, not paths or lines. Writing the SVG widget... Writing SVG text elements... Verifying the vertical positioning for the remaining chapters...

all the coordinates align properly, with the last subtitle ending well within the viewBox bounds. Now I'm ready to implement the widget and add clickable interactions for each chapter—I'll set up sendPrompt calls in Chinese so users can request detailed information about specific sections.

Writing prompt messages... Writing SVG code...
```
This block is not supported on your current device yet.
```

Now let me write a comprehensive text summary of all 9 chapters. The user asked for an overview, so I'll provide a detailed but well-organized explanation of each chapter.这份文档是作者 @ricuhkaen（被粉丝昵称"🍉老师"）专门为**完全零基础**新人写的 Xray 自建教程，号称"互联网上最详细、最有耐心的从 0 开始教程"。共 9 章，每章解决一个具体问题，串联成一条完整的部署路线。

---

**第 1 章 · 前言罗嗦篇**

先帮你做一个最重要的决定：到底用机场还是自建？ 作者没有简单劝你自建，而是认真分析了机场的优势（便宜省事、节点多）和风险（隐私泄露、随时跑路），以及自建需要学习的门槛（Linux、域名、TLS 证书等）。如果你决定使用机场，就关闭本文；决定自建，才往后读。

**第 2 章 · 原料准备篇**

列出开工前的所有材料清单：一台安装好 Debian 系统的 VPS（记录好 IP、端口、用户名密码）、一个域名并添加指向 VPS 的 A 记录、本地安装 SSH 工具（PuTTY / Terminal）、文件传输工具和 VSCode 文本编辑器。

**第 3 章 · 远程登录篇**

教你第一次用 SSH 登进服务器，并带你认识最基础的 Linux 操作——一切后续操作的起点。

**第 4 章 · 安全防护篇**

这章非常重要。默认配置下，SSH 默认端口是 22，默认用户是 root，剩下唯一不确定的就是密码；恶意扫描脚本会自动尝试这些默认值。作者的解法是：改 SSH 端口（非 22）、新建非 root 用户并禁止 root 远程登录、改用 RSA 密钥验证并关掉密码登录。

**第 5 章 · 网站建设篇**

用 Nginx + 一个最简单的静态 HTML 页面搭建伪装站，目的是让服务器在被探测时呈现出一个"正常网站"，而非裸露的代理服务器。作者用的是最简示例，但你完全可以把它做成真实的博客或网站。

**第 6 章 · 证书管理篇**

用 `acme.sh` 工具为域名申请真实的 TLS 证书，让网站具备 HTTPS 访问能力——这是 Xray 流量充分加密的核心基础设施。作者特别强调先用测试命令验证可行性，避免超过 Let's Encrypt 的申请频率限制。

**第 7 章 · Xray 服务器篇**

服务端的 Xray 配置文件分为五大模块：日志（log）、DNS 设置、分流路由（routing）、入站（inbounds）、出站（outbounds）。路由规则会屏蔽本地 IP 回环、阻止服务器直连国内 IP，还可以过滤广告流量。

**第 8 章 · Xray 客户端篇**

客户端配置结构与服务端相同，也分五大模块。DNS 配置上，国外域名走国外 DNS（1.1.1.1），国内域名走国内 DNS（114.114.114.114），实现精准的境内外分流。 到此你已经从零完成了 VPS 服务器部署并成功在客户端配置使用 Xray，是一个巨大的胜利！

**第 9 章 · 附录**

命令速查表和全教程的知识点回顾，相当于"考前复习资料"。

---

**整体感受：** 这套教程的核心价值在于它不跳步骤——每一个"为什么"都有解释，每一条命令都截图示范。读完不只会复制粘贴，还能理解背后的逻辑：为什么需要域名、TLS 证书和 Nginx 伪装，三者共同构成了让代理流量看起来像"正常 HTTPS 网站访问"的完整伪装链。

点击图中任意章节，可以让我深入讲解那一章的具体内容 👆
 

> [tool_use: web_fetch] {"url": "https://github.com/ricuhkaen/Xray-docs-next/blob/main/docs/document/level-0", "html_extraction_method": "markdown"}

> [tool_result] {"error_type": "ROBOTS_DISALLOWED", "error_message": "Site disallows automated access. Use the search-result snippet, or find an alternative source."}

> [tool_use: web_fetch] {"html_extraction_method": "markdown", "url": "https://github.com/ricuhkaen/Xray-docs-next/tree/main/docs/document/level-0"}

> [tool_result] {"error_type": "PERMISSIONS_ERROR", "error_message": "This URL was not in any prior search or fetch result. web_search for it first, then fetch the result link."}

> [tool_use: web_search] {"query": "Xray-docs-next level-0 document ricuhkaen github"}

> [tool_result] { &quot;outbounds&quot;: [ { &quot;tag&quot;: &quot;proxy-out-vless&quot;, &quot;protocol&quot;: &quot;vless&quot;, &quot;settings&quot;: { &quot;vnext&quot;: [ { &quot;address&quot;: &quot;a-name.yourdomain.com&quot;, &quot;port&quot;: 443, &quot;users&quot;: [ { &quot;id&quot;: &quot;uuiduuid-uuid-uuid-uuid-uuiduuiduuid&quot;, &quot;flow&quot;: &quot;xtls-rprx-vision&quot;, &quot;encryption&quot
好的，我找到了对应的文档网站，让我进一步获取每个章节的内容。

> [tool_use: web_fetch] {"html_extraction_method": "markdown", "url": "https://xtls.github.io/Xray-docs-next/document/level-0/"}

> [tool_result] {"error_type": "CLIENT_ERROR", "error_message": "There was an error while fetching: The page returned a 404 client error"}

> [tool_use: web_fetch] {"html_extraction_method": "markdown", "url": "https://xtls.github.io/document/level-0/"}

> [tool_result] {"error_type": "PERMISSIONS_ERROR", "error_message": "This URL was not in any prior search or fetch result. web_search for it first, then fetch the result link."}

> [tool_use: web_search] {"query": "小小白白话文 Xray 第1章到第8章 site:xtls.github.io"}

> [tool_result] 为 Project X 的文档贡献 · 【第 1 章】 小小白白话文

如果你决定自建，那就请继续阅读后面的章节吧！！ · 我相信，有耐心看到这里的同学，都是兼具好奇心和行动力的学习派！我现在要郑重的恭喜你，因为到了这里，你已经完完整整的【从第一条命令开始，完成了 VPS 服务器部署，并成功的在客户端配置使用 Xray】了！这毫无疑问是一个巨大的胜利！ · 我相信，你现在一定对Linux不再恐惧，对Xray不再陌生了吧！ · 至此，小小白白话文圆满结束！ · ⬛⬛⬛⬛⬛⬛⬛⬛ 100% 但现在你看到的，远远不是 Xray 的全貌。 · Xray是一个强大而丰富的网络工具集合，平台化的提供了众多模块，可以像瑞士军刀一样，通过灵活的配置组合解决各种不同的问题。而本文，仅仅蜻蜓点水的用了最简单、最直观的配置来做基础演示。 · 如果你觉得现在已经完全够用了，那就好好的享受它给你带来的信息自由。但如

> [tool_use: web_fetch] {"html_extraction_method": "markdown", "url": "https://xtls.github.io/document/level-0/ch01-preface.html"}

> [tool_result] 【第 1 章】 小小白白话文 | Project X



[Skip to content](#VPContent)

[![](https://xtls.github.io/logo-dark.svg)![](https://xtls.github.io/logo-light.svg)Project X](https://xtls.github.io/)

搜索`⌘``Ctrl``K`

 Main Navigation [首页](https://xtls.github.io/)

配置指南

[特性详解](https://xtls.github.io/config/features/)

[基础配置](https://xtls.github.io/config/)

[入站协议](https://xtls.github.io/config/inbounds/)

[出站协议](htt

> [tool_use: web_fetch] {"html_extraction_method": "markdown", "url": "https://xtls.github.io/document/level-0/ch02-preparation.html", "text_content_token_limit": 3000}

> [tool_result] ---
meta-description: Xray-core
meta-generator: VitePress v2.0.0-alpha.17
meta-viewport: width=device-width,initial-scale=1
title: 【第 2 章】原料准备篇 | Project X
---


[Skip to content](#VPContent)

[![](https://xtls.github.io/logo-dark.svg)![](https://xtls.github.io/logo-light.svg)Project X](https://xtls.github.io/)

搜索`⌘``Ctrl``K`

 Main Navigation [首页](https://xtls.github.io/)

配置指南

[特性详解](https://x

> [tool_use: web_fetch] {"html_extraction_method": "markdown", "text_content_token_limit": 2000, "url": "https://xtls.github.io/document/level-0/ch03-ssh.html"}

> [tool_result] ---
meta-description: Xray-core
meta-generator: VitePress v2.0.0-alpha.17
meta-viewport: width=device-width,initial-scale=1
title: 【第 3 章】远程登录篇 | Project X
---


[Skip to content](#VPContent)

[![](https://xtls.github.io/logo-dark.svg)![](https://xtls.github.io/logo-light.svg)Project X](https://xtls.github.io/)

搜索`⌘``Ctrl``K`

 Main Navigation [首页](https://xtls.github.io/)

配置指南

[特性详解](https://x

> [tool_use: web_fetch] {"html_extraction_method": "markdown", "url": "https://raw.githubusercontent.com/XTLS/Xray-docs-next/main/docs/document/level-0/ch03-ssh.md"}

> [tool_result] {"error_type": "PERMISSIONS_ERROR", "error_message": "This URL was not in any prior search or fetch result. web_search for it first, then fetch the result link."}

> [tool_use: web_search] {"query": "小小白白话文 第3章远程登录 第4章安全 第5章网站建设 Xray site:xtls.github.io"}

> [tool_result] 【第 3 章】 远程登录篇 - 一桥飞架南北，天堑变通途 · 【第 4 章】 安全防护篇 - 安全不注意，亲人两行泪 · 【第 5 章】 网站建设篇 - 秀出你的美 · 【第 6 章】 证书管理篇 - 领证的才是合法的 · 【第 7 章】 Xray 服务器篇 - 终于等到你 · 【第 8 章】 Xray 客户端篇 - 新的开始 · 【第 9 章】 附录 - 考点都在这里 · 贡献者 (2) JimhHan· 2 次提交 · @JimhHan · Meow· 1 次提交 ·

【第 3 章】 远程登录篇 - 一桥飞架南北，天堑变通途 · 【第 4 章】 安全防护篇 - 安全不注意，亲人两行泪 · 【第 5 章】 网站建设篇 - 秀出你的美 · 【第 6 章】 证书管理篇 - 领证的才是合法的 · 【第 7 章】 Xray 服务器篇 - 终于等到你 · 【第 8 章】 Xray 客户端篇 - 

> [tool_use: web_search] {"query": "小小白白话文 第5章网站建设 Nginx 第6章证书管理 acme.sh Xray xtls"}

> [tool_result] 在 &quot;4.7 使用RSA密钥登录并禁用密码登录&quot; 中 除了 authorized_keys 文件权限设置为 600 以外 .ssh 文件夹权限也应设置为 700 这点应该要提醒一下读者 &quot;ls -al ~/&quot;检查文件夹权限,不然可能一些ssh客户端无法通过密钥验证 这个章节是【从零开始】的基础课，新来的同学好好看好好学哦

这个章节是【从零开始】的基础课，新来的同学好好看好好学哦 接下来我们要做的，是为我们的域名申请一个真实的 TLS 证书，使网站具备标准 TLS 加密的能力及 HTTPS 访问的能力。这就是 Xray 等现阶段安全代理工具确保流量充分加密最重要的工具。 ... 请不要轻易使用自签证书。它并没有让操作简单太多，但增加了无谓的风险（如中间人攻击）。 · 这里我会使用一个叫做 acme.sh 的证书管理工具，它简单、轻量、高效，并可完成证
我已经读取了足够的内容，现在给你做一个完整的讲解。

> [tool_use: visualize:read_me] {"modules": ["diagram"], "platform": "desktop"}

> [tool_result] # Imagine — Visual Creation Suite

## Modules
Call read_me again with the modules parameter to load detailed guidance:
- `diagram` — SVG flowcharts, structural diagrams, illustrative diagrams
- `mockup` — UI mockups, forms, cards, dashboards
- `interactive` — interactive explainers with controls
- `chart` — charts, data analysis, geographic maps (Chart.js, D3 choropleth)
- `art` — illustration and

> [tool_use: visualize:show_widget] {"title": "xray_level0_roadmap", "loading_messages": ["绘制章节路线图...", "整理九大模块..."], "widget_code": "<svg width=\"100%\" viewBox=\"0 0 680 700\" role=\"img\">\n  <title>小小白白话文完整章节概览</title>\n  <desc>9章节从零开始学习路线：从入门分析到完成Xray自建服务器</desc>\n  <defs>\n    <marker id=\"arrow\" viewBox=\"0 0 10 10\" refX=\"8\" refY=\"5\" markerWidth=\"6\" markerHeight=\"6\" orient=\"auto-start-reverse\"><path d=\"M2 1L8 5L2

> [tool_result] Content rendered and shown to the user. Please do not duplicate the shown content in text because it's already visually represented. [This tool call rendered an interactive widget in the chat. The user can already see the result — do not repeat it in text or with another visualization tool.]
这份文档是作者 @ricuhkaen（被粉丝昵称"🍉老师"）专门为**完全零基础**新人写的 Xray 自建教程，号称"互联网上最详细、最有耐心的从 0 开始教程"。共 9 章，每章解决一个具体问题，串联成一条完整的部署路线。

---

**第 1 章 · 前言罗嗦篇**

先帮你做一个最重要的决定：到底用机场还是自建？ 作者没有简单劝你自建，而是认真分析了机场的优势（便宜省事、节点多）和风险（隐私泄露、随时跑路），以及自建需要学习的门槛（Linux、域名、TLS 证书等）。如果你决定使用机场，就关闭本文；决定自建，才往后读。

**第 2 章 · 原料准备篇**

列出开工前的所有材料清单：一台安装好 Debian 系统的 VPS（记录好 IP、端口、用户名密码）、一个域名并添加指向 VPS 的 A 记录、本地安装 SSH 工具（PuTTY / Terminal）、文件传输工具和 VSCode 文本编辑器。

**第 3 章 · 远程登录篇**

教你第一次用 SSH 登进服务器，并带你认识最基础的 Linux 操作——一切后续操作的起点。

**第 4 章 · 安全防护篇**

这章非常重要。默认配置下，SSH 默认端口是 22，默认用户是 root，剩下唯一不确定的就是密码；恶意扫描脚本会自动尝试这些默认值。作者的解法是：改 SSH 端口（非 22）、新建非 root 用户并禁止 root 远程登录、改用 RSA 密钥验证并关掉密码登录。

**第 5 章 · 网站建设篇**

用 Nginx + 一个最简单的静态 HTML 页面搭建伪装站，目的是让服务器在被探测时呈现出一个"正常网站"，而非裸露的代理服务器。作者用的是最简示例，但你完全可以把它做成真实的博客或网站。

**第 6 章 · 证书管理篇**

用 `acme.sh` 工具为域名申请真实的 TLS 证书，让网站具备 HTTPS 访问能力——这是 Xray 流量充分加密的核心基础设施。作者特别强调先用测试命令验证可行性，避免超过 Let's Encrypt 的申请频率限制。

**第 7 章 · Xray 服务器篇**

服务端的 Xray 配置文件分为五大模块：日志（log）、DNS 设置、分流路由（routing）、入站（inbounds）、出站（outbounds）。路由规则会屏蔽本地 IP 回环、阻止服务器直连国内 IP，还可以过滤广告流量。

**第 8 章 · Xray 客户端篇**

客户端配置结构与服务端相同，也分五大模块。DNS 配置上，国外域名走国外 DNS（1.1.1.1），国内域名走国内 DNS（114.114.114.114），实现精准的境内外分流。 到此你已经从零完成了 VPS 服务器部署并成功在客户端配置使用 Xray，是一个巨大的胜利！

**第 9 章 · 附录**

命令速查表和全教程的知识点回顾，相当于"考前复习资料"。

---

**整体感受：** 这套教程的核心价值在于它不跳步骤——每一个"为什么"都有解释，每一条命令都截图示范。读完不只会复制粘贴，还能理解背后的逻辑：为什么需要域名、TLS 证书和 Nginx 伪装，三者共同构成了让代理流量看起来像"正常 HTTPS 网站访问"的完整伪装链。

点击图中任意章节，可以让我深入讲解那一章的具体内容 👆

### 🧑 Jace

这里面很多知识我都是不懂的
这里面很多知识我都是不懂的

### 🤖 Claude

The user is saying they don't understand a lot of the knowledge mentioned in the tutorial. They want me to help them understand the fundamentals. Let me think about what would be most helpful here.

I should ask them what they specifically don't understand, or offer to explain the key concepts in a beginner-friendly way. The user seems to be a complete beginner (零基础), which is exactly who this tutorial is written for.

Let me think about what key concepts might be confusing:
1. VPS - what is it?
2. Domain name / DNS
3. SSH
4. Linux basics
5. TLS/HTTPS certificates
6. Nginx and how it serves as a reverse proxy
7. Xray and proxy protocols
8. How all these pieces connect together architecturally

Since they mentioned not understanding many things, I think the best approach is to ask what they'd like to focus on first, or offer a structured overview of the foundational concepts. I want to reassure them that this is normal for beginners and that I can break it down into digestible pieces. I'll create a visual architecture diagram showing how all the pieces connect—the client, encrypted traffic, VPS, and the actual internet—and then break down each component like VPS, domain names, TLS encryption, Nginx, Xray, and SSH in straightforward terms so they understand the complete system before we dive into specifics. The GFW only sees encrypted traffic to your domain, so it can't identify it as a proxy. I'm explaining the key components: a VPS is essentially a rented computer outside China that can freely access any website, a domain name maps to your VPS's IP address, TLS certificates enable HTTPS encryption to prevent traffic interception, and Nginx serves as the web server that displays legitimate content when visitors access your domain.

Now I'm thinking through how to present this clearly to someone unfamiliar with these concepts. Rather than asking clarifying questions, I should jump straight into a visual diagram showing how the entire system works together—the user needs a concrete mental model of the architecture.

I'm sketching out a horizontal flow diagram that shows the user's computer on the left, the Great Firewall as a barrier in the middle, the overseas VPS on the right with its components, and the open internet beyond. The arrows between these elements will show how encrypted traffic flows through the system, disguised as normal HTTPS website visits. Writing SVG layout... Writing component styles...

Actually, I'm realizing the complexity here might be too much with all the styling constraints. Let me simplify and just use a basic SVG diagram instead.

I'm planning out a straightforward layout with three boxes arranged horizontally—your computer on the left, a VPS in the middle, and the free internet on the right—with the GFW wall as a vertical barrier between them. Each box will have a title and a couple of descriptive lines, and I'll connect them with arrows to show the flow.

I'm adding labels to the arrows to explain what's happening at each stage: encrypted HTTPS traffic leaving your computer, the GFW allowing it through because it looks like normal HTTPS, and then regular requests reaching the internet. I'll also include a note inside or below the GFW wall explaining what the firewall sees and why it lets the traffic pass.

Now I'm thinking about the best way to present this to the user—a clean SVG diagram with three zones showing domestic, the GFW barrier, and foreign networks, along with clear explanatory text for each concept. Adding diagram labels...

### 🧑 Jace

详细讲解第4章安全防护:如何修改端口、新建用户、设置密钥登录
详细讲解第4章安全防护:如何修改端口、新建用户、设置密钥登录

### 🤖 Claude

The user wants me to explain Chapter 4 of the tutorial in detail - about security: modifying SSH port, creating new users, and setting up key-based login. Let me fetch the actual content from the website first to get the specific details.
```
This block is not supported on your current device yet.
```

I now have a very detailed understanding of Chapter 4. Let me now create a visual explanation and write a comprehensive but easy-to-understand guide.

The key topics are:
1. Why security matters (4.1-4.2)
2. The three things to fix: Port 22, root user, password
3. Step 1: Change SSH port (4.4)
4. Step 2: Create non-root user + sudo (4.5)
5. Step 3: Disable root SSH login (4.6)
6. Step 4: RSA key authentication + disable password (4.7)
I'm going to use a door lock metaphor to visualize how SSH security works—showing the four tumblers that need to align: IP address, port number, username, and authentication method. This will illustrate how the default configuration leaves you vulnerable and how each hardening step closes another gap.

Building the SVG layout... I'm laying out a side-by-side comparison showing the before and after states of SSH security, with the vulnerable configuration on the left (IP discoverable, port 22, root user, password-only auth) and the hardened version on the right (unknown port, different username, RSA key authentication). Now I'm thinking through how to structure this visually as an HTML widget with two panels. Filling in the remaining rows with the comparison data for ports, usernames, and authentication methods across the two panels.

I'm realizing this table layout is getting complicated, so I'll switch to building an HTML widget instead where I can use CSS grid and flexbox to handle the layout more cleanly.

Writing component styles... Still writing styles... Writing component markup... Writing component markup... Writing component markup... I need to verify the semantic color variables work across light and dark modes, and the background colors should use the lighter palette stops. For the step buttons layout, I'm considering a fixed width for the center column to keep things readable on mobile, though the widget's ~680px width should handle the three-column grid fine on desktop. I'm also double-checking whether the Tabler icon classes I'm using are valid options from the spec.

I'm reconsidering the icon approach—rather than relying on specific Tabler icon variants that might not exist, I'll use simple Unicode text symbols with CSS color styling instead. This gives me "✕" for bad states in red, "—" for neutral in gray, and "✓" for good in green, which is more reliable and straightforward.

Now I'm structuring the widget layout with a three-column grid design, secondary background panels with rounded corners and padding, and rows that display items with proper spacing and borders between them.

Writing widget styles... Still writing styles... Writing the security assessment interface... Writing the security comparison layout... I need to widen the center column to 120px and adjust the button width to 94px so they fit better. Then I'm planning the structure for explaining the four steps—showing the widget first, followed by concise text descriptions of each step, with the buttons linking to more detailed explanations.

Now I'm drafting the step explanations in Chinese. Step 1 covers modifying the SSH port in the config file and restarting the service. Step 2 walks through creating a new user and granting sudo privileges without requiring a password. Step 3 disables root login by changing the SSH configuration setting.

For Step 4, I'm explaining how to set up key-based authentication using PuTTYgen to generate a public-private key pair, then uploading the public key to the VPS and disabling password login in the SSH config. I'm also noting that there appear to be additional steps (4.8 and 4.9) in the original document that I should verify I've covered.

Now I'm planning how to structure my response to the user: I'll start with a brief introduction about the security threat model, then display a visual comparison widget, followed by detailed explanations of each of the four hardening steps with concrete commands, and finally highlight any important warnings from the source material. The loading messages I'll use are "绘制安全对比图..." and "整理四项加固步骤...". I need to keep the widget clean and minimal, then explain each hardening step in the text below with the actual commands. I'm also noting the critical warnings—changing the port and username from the published examples, doing steps in order to avoid lockout, and acknowledging the sudo NOPASSWD trade-off that's discussed in the documentation.

For the key pair concept, I want to explain it intuitively for beginners: the public key is like a padlock you install on the VPS that anyone can use to lock things, but only your private key can unlock them. The private key stays on your local machine and never gets shared—this is the core of RSA asymmetric encryption explained simply.

I should also mention that Ed25519 is preferred over RSA if the devices support it, and I'll include the essential commands for modifying SSH configuration, restarting the service, and creating new users.

For the complete response, I'll structure it with an introduction about why security matters, a before/after comparison widget, and then walk through the four main steps. I need to emphasize the critical warnings: follow the steps in order to avoid locking yourself out, use your own port number and username instead of the published examples, and explain the config file edits as text rather than just showing raw commands. I need to decide on formatting for the technical steps—keeping them prose-like with explanations rather than bare commands, and making sure the widget comes before the step breakdown to set up the threat model first.好，这一章很关键，我来从头讲透。

你的 VPS 从上线那一刻起，互联网上的恶意扫描脚本就已经在 24 小时不间断地尝试登录它了。它们不需要人坐在那里手动操作，全是自动化的。SSH 登录需要四个条件——IP、端口、用户名、认证方式——而默认状态下，前三个其实已经"送"给攻击者了：
```
This block is not supported on your current device yet.
```

Good, the widget is shown. Now let me write the detailed explanation of the four steps.点击图中的步骤按钮可以深入讲解，这里先给你把四步都讲清楚：

---

**① 修改 SSH 端口（改掉默认的 22）**

默认 SSH 端口是 22，攻击脚本会优先扫描这个端口。改成其他端口可以让大部分无差别扫描脚本直接跳过你的服务器。

用 `nano` 编辑器打开 SSH 的配置文件：
```bash
nano /etc/ssh/sshd_config
```
进入编辑器后，按 `Ctrl+W` 搜索 `Port 22`，把 22 改成你自己选的数字（比如 `9753`，但文档强调**要换成你自己想的**，因为教程里的例子端口本身已经是"特征"了）。保存用 `Ctrl+O` 再回车，退出用 `Ctrl+X`，然后重启 SSH 服务：
```bash
systemctl restart ssh
```
之后 PuTTY 连接时要在端口栏填你新设的端口号。

---

**② 新建一个普通用户**

Linux 的 `root` 不只是管理员，它是整个系统的主宰，一旦 root 账户出现问题，整个系统都只能任人鱼肉。所以我们新建一个普通用户来日常使用，给它起个自己想的名字（不要照抄教程里的 `vpsadmin`，原因同上）：

```bash
adduser 你的用户名
```
系统会让你设密码，设一个强密码。然后安装 `sudo` 工具，让这个用户在需要时能临时借用 root 权限：
```bash
apt update && apt install sudo
```
再运行 `visudo` 打开权限配置，在合适位置加上一行：
```
你的用户名 ALL=(ALL) NOPASSWD: ALL
```
这样普通用户就能用 `sudo 命令` 的方式执行需要管理员权限的操作了。

---

**③ 禁止 root 用户远程 SSH 登录**

还是打开那个配置文件，找到 `PermitRootLogin yes` 这一行，把 `yes` 改成 `no`，保存，再重启 SSH。从此 root 账户彻底无法从外部远程登录——即使攻击者猜到了用户名是 root，也是白搭。以后你用步骤②新建的普通用户名来登录，需要 root 权限时加 `sudo`。

---

**④ 密钥登录，彻底丢掉密码**

这是安全性提升最大的一步。理解它的关键是搞清楚"密钥对"是什么：

公钥就像你给 VPS 装了一把专属的锁，谁都可以看到这把锁，但只有拿着对应钥匙的人才能开。私钥就是那把钥匙，只存在你自己的电脑里，永远不上传给任何人。登录时 SSH 自动用"锁"和"钥匙"配对验证，而不是问你密码——所以攻击者就算有密码表也没用，因为根本没有密码让他撞。

用 PuTTYgen 工具生成密钥对：运行 PuTTYgen → 点 Generate → 保存公钥（`id_rsa.pub`）和私钥（`id_rsa.ppk`）→ 把公钥的文本内容保存为 `authorized_keys` 文件并上传到 VPS 的 `~/.ssh/` 目录下。上传后在 SSH 配置里把密码登录关掉，密钥登录开启，再重启 SSH。

---

**一个非常重要的提醒**：这四步一定要按顺序来，不然可能把自己锁在门外。尤其是第④步——务必先确认密钥登录能成功，再去关掉密码登录。如果顺序反了，密钥没配好就先关密码，你就再也进不去服务器了。

想深入了解哪个步骤，点图里的按钮或者直接问我。
 

> [tool_use: web_fetch] {"html_extraction_method": "markdown", "text_content_token_limit": 8000, "url": "https://xtls.github.io/document/level-0/ch04-security.html"}

> [tool_result] ---
meta-description: Xray-core
meta-generator: VitePress v2.0.0-alpha.17
meta-viewport: width=device-width,initial-scale=1
title: 【第 4 章】安全防护篇 | Project X
---


[Skip to content](#VPContent)

[![](https://xtls.github.io/logo-dark.svg)![](https://xtls.github.io/logo-light.svg)Project X](https://xtls.github.io/)

搜索`⌘``Ctrl``K`

 Main Navigation [首页](https://xtls.github.io/)

配置指南

[特性详解](https://x
好，这一章很关键，我来从头讲透。

你的 VPS 从上线那一刻起，互联网上的恶意扫描脚本就已经在 24 小时不间断地尝试登录它了。它们不需要人坐在那里手动操作，全是自动化的。SSH 登录需要四个条件——IP、端口、用户名、认证方式——而默认状态下，前三个其实已经"送"给攻击者了：

> [tool_use: visualize:show_widget] {"loading_messages": ["绘制安全对比图...", "整理四项加固步骤..."], "title": "ssh_security_before_after", "widget_code": "<style>\n.s{display:grid;grid-template-columns:1fr 120px 1fr;gap:0;}\n.p{background:var(--color-background-secondary);border-radius:var(--border-radius-lg);padding:16px;}\n.pt{font-size:13px;font-weight:500;margin-bottom:12px;color:var(--color-text-primary);}\n.row{display:flex;align-items:fle

> [tool_result] Content rendered and shown to the user. Please do not duplicate the shown content in text because it's already visually represented. [This tool call rendered an interactive widget in the chat. The user can already see the result — do not repeat it in text or with another visualization tool.]
点击图中的步骤按钮可以深入讲解，这里先给你把四步都讲清楚：

---

**① 修改 SSH 端口（改掉默认的 22）**

默认 SSH 端口是 22，攻击脚本会优先扫描这个端口。改成其他端口可以让大部分无差别扫描脚本直接跳过你的服务器。

用 `nano` 编辑器打开 SSH 的配置文件：
```bash
nano /etc/ssh/sshd_config
```
进入编辑器后，按 `Ctrl+W` 搜索 `Port 22`，把 22 改成你自己选的数字（比如 `9753`，但文档强调**要换成你自己想的**，因为教程里的例子端口本身已经是"特征"了）。保存用 `Ctrl+O` 再回车，退出用 `Ctrl+X`，然后重启 SSH 服务：
```bash
systemctl restart ssh
```
之后 PuTTY 连接时要在端口栏填你新设的端口号。

---

**② 新建一个普通用户**

Linux 的 `root` 不只是管理员，它是整个系统的主宰，一旦 root 账户出现问题，整个系统都只能任人鱼肉。所以我们新建一个普通用户来日常使用，给它起个自己想的名字（不要照抄教程里的 `vpsadmin`，原因同上）：

```bash
adduser 你的用户名
```
系统会让你设密码，设一个强密码。然后安装 `sudo` 工具，让这个用户在需要时能临时借用 root 权限：
```bash
apt update && apt install sudo
```
再运行 `visudo` 打开权限配置，在合适位置加上一行：
```
你的用户名 ALL=(ALL) NOPASSWD: ALL
```
这样普通用户就能用 `sudo 命令` 的方式执行需要管理员权限的操作了。

---

**③ 禁止 root 用户远程 SSH 登录**

还是打开那个配置文件，找到 `PermitRootLogin yes` 这一行，把 `yes` 改成 `no`，保存，再重启 SSH。从此 root 账户彻底无法从外部远程登录——即使攻击者猜到了用户名是 root，也是白搭。以后你用步骤②新建的普通用户名来登录，需要 root 权限时加 `sudo`。

---

**④ 密钥登录，彻底丢掉密码**

这是安全性提升最大的一步。理解它的关键是搞清楚"密钥对"是什么：

公钥就像你给 VPS 装了一把专属的锁，谁都可以看到这把锁，但只有拿着对应钥匙的人才能开。私钥就是那把钥匙，只存在你自己的电脑里，永远不上传给任何人。登录时 SSH 自动用"锁"和"钥匙"配对验证，而不是问你密码——所以攻击者就算有密码表也没用，因为根本没有密码让他撞。

用 PuTTYgen 工具生成密钥对：运行 PuTTYgen → 点 Generate → 保存公钥（`id_rsa.pub`）和私钥（`id_rsa.ppk`）→ 把公钥的文本内容保存为 `authorized_keys` 文件并上传到 VPS 的 `~/.ssh/` 目录下。上传后在 SSH 配置里把密码登录关掉，密钥登录开启，再重启 SSH。

---

**一个非常重要的提醒**：这四步一定要按顺序来，不然可能把自己锁在门外。尤其是第④步——务必先确认密钥登录能成功，再去关掉密码登录。如果顺序反了，密钥没配好就先关密码，你就再也进不去服务器了。

想深入了解哪个步骤，点图里的按钮或者直接问我。

### 🧑 Jace

详细讲解第6章证书管理：acme.sh申请TLS证书完整流程
详细讲解第6章证书管理：acme.sh申请TLS证书完整流程

### 🧑 Jace

详细讲解第6章证书管理:acme.sh申请TLS证书完整流程
详细讲解第6章证书管理:acme.sh申请TLS证书完整流程

### 🤖 Claude

The user wants me to explain Chapter 6 of the tutorial in detail - about certificate management using acme.sh. Let me fetch the actual content from the website first.
```
This block is not supported on your current device yet.
```

I now have the full content of Chapter 6. Let me plan my explanation:

1. First explain WHAT is TLS/HTTPS and WHY we need it (conceptually, for beginners)
2. Explain what acme.sh is and how the certificate system works
3. Show the 4-step process visually
4. Explain each command in detail
5. Show the final directory structure

Key concepts to explain:
1. **What is TLS/HTTPS?** - It encrypts web traffic. When your browser visits https://google.com, TLS encrypts the data. For Xray, we need TLS to make proxy traffic look like normal HTTPS web browsing.
2. **What is a TLS certificate?** - A certificate is like an "ID card" for your website. It proves the domain belongs to you and that traffic is encrypted.
3. **Why can't we just self-sign?** - Self-signed certificates are like fake IDs that clients and browsers reject, introducing security risks like MITM attacks.
4. **Who issues certificates?** - Certificate Authorities like Let's Encrypt provide free certificates.
5. **The HTTP challenge (webroot method)** - Let's Encrypt verifies domain ownership by checking for a specific file on your web server.
6. **acme.sh** - A shell script that automates certificate issuance and renewal.
7. **ECC vs RSA** - The tutorial uses ECC (ec-256) because it's smaller and faster than RSA.

The process involves four main steps: installing acme.sh, running a test certificate request, requesting the real certificate, and installing it to the correct location. I'm planning to create a diagram showing how Let's Encrypt verifies domain ownership through the challenge-response flow.

When you request a certificate, acme.sh contacts Let's Encrypt, which responds with a challenge file to place in your web server's directory. acme.sh puts the file in your Nginx root (the `-w` flag points to where Nginx serves files), Let's Encrypt fetches it from the internet to confirm you own the domain, and then issues the certificate. This is the webroot verification method.

Creating a visual flowchart... Building an interactive widget with two sections: the verification flow showing how acme.sh requests a certificate, Let's Encrypt validates domain ownership by checking a proof file in the Nginx directory, and then issues the cert — plus a display of the resulting certificate files (the cert, private key, and full chain) that Xray will use. Writing SVG diagram... Building the widget layout... Writing SVG layout... I'll structure this as a 4-step process flow diagram showing the acme.sh workflow: installation, test run, formal certificate request, and installation to the target directory. Each step will include the corresponding command. Below the flow, I'll display the three output files (certificate, private key, and full chain) that get used by Xray. The surrounding text will cover the conceptual background on why certificates are needed and how the webroot verification mechanism works.

Now I'm designing the SVG for the flow diagram... Writing SVG code... I'm recalculating the box positions with narrower widths to create better spacing between elements, ensuring there's at least 25 pixels of gap between each box and proper margins from the edges.

Now checking that all the text labels fit within their boxes—the mixed Chinese and English text at various font sizes all appear to have enough room without overflow.

For positioning the SVG text elements, I'm setting the title and subtitle within each box using vertical centering, with the title at y=79 and subtitle at y=99 relative to each box's starting position. I'm also planning to add a results section below showing the certificate files that get generated after a successful request.

Now I'm laying out three file pills for the certificate outputs, expanding the viewBox to accommodate everything, and positioning them evenly across the width with proper spacing and labels for each file type.

Writing SVG code... Writing SVG diagram... Writing SVG diagram... Writing SVG elements... Verifying the SVG layout spacing... The text and subtitle block centers out to about 67.5, which is nearly aligned with the box center at 66. Now checking the horizontal spacing between the boxes—there's a 20px gap between them, and the box centers are positioned at 85, 235, 390, and 570 with 150px spacing between each.

For the file pills, I'm verifying their positions and gaps. Pill 1 centers around 122, Pill 2 at 340, and Pill 3 at 556, all fitting within the 680px width. The gaps between consecutive pills are consistent at 42px each.

Now I'm checking the text sizing—"fullchain.crt" at 14px should fit comfortably in the 175px pill width. I'm also reconsidering the viewBox height; the pills end at y=183, so I'll bump it to 205 for better breathing room. For the Chinese text "Let's Encrypt 签发" in box 3, the mixed Latin and CJK characters should fit within the 140px box width even with padding accounted for.

Writing the widget code... want a cert for a-name.yourdomain.com, so Let's Encrypt asks me to place a verification file at a specific path in my web root, then checks if it can fetch that file from the internet to confirm domain ownership. This is why Nginx needs to be running first—without a working web server, the verification fails and I hit Let's Encrypt's rate limits, so testing with their staging environment first prevents wasting attempts.

The `--force` flag overrides the normal skip-if-already-valid behavior since the test certificate is technically still valid. I'm also setting up auto-renewal with `--upgrade --auto-upgrade` so acme.sh renews the certificate automatically about 30 days before the 90-day expiry. The process generates three key files—the certificate itself, the private key (which must stay secret), and the full chain—that get installed to the Xray directory.先理解为什么需要证书，再看命令就清晰多了。

TLS 证书是网站的"官方身份证"。浏览器访问 `https://` 开头的网站时，会验证这张证书——只有被权威机构（Certificate Authority，简称 CA）签发的证书才被认可。对 Xray 来说，用真实证书让流量"看起来像正规 HTTPS 网站访问"，是整个伪装方案成立的基础。**这也是为什么第 5 章要先建好 Nginx 网站，再申请证书——申请过程中 Let's Encrypt 会来你的网站取一个验证文件，你得先有个能正常访问的网站。**
```
This block is not supported on your current device yet.
```

Good. Now let me explain the domain ownership verification concept and then walk through each command in detail.---

**关键前置概念：Let's Encrypt 怎么确认你真的拥有这个域名？**

acme.sh 用的是"网站根目录验证法"（webroot 方式）：

你向 Let's Encrypt 说"我要给 `a-name.yourdomain.com` 申请证书"，它会回复"那你在这个地址放一个我指定的文件：`http://a-name.yourdomain.com/.well-known/acme-challenge/随机字符`"。acme.sh 自动把这个文件放进 Nginx 的网站目录（命令里 `-w /home/vpsadmin/www/webpage` 那个路径）。Let's Encrypt 从外网来取这个文件，取到了 → 证明你控制这个域名 → 签发证书。这就是为什么第 5 章必须先装好 Nginx——没有它，这个验证就无法完成。

---

**① 安装 acme.sh**

三条命令，顺序执行：

```bash
wget -O - https://get.acme.sh | sh   # 下载并安装
. .bashrc                             # 让 acme.sh 命令立刻生效
acme.sh --upgrade --auto-upgrade     # 开启自动升级
```

安装完成后 acme.sh 就住在你的 `~/.acme.sh/` 目录里，并且会自动在系统里加入一个定时任务（cron job），60 天左右自动帮你续签证书，完全不用操心。

---

**② 先用测试服申请一次**

先用测试命令验证是否可以成功申请，这样可以避免在本地配置有误时，反复申请证书失败，超过 Let's Encrypt 的频率上限（每小时、每个域名失败最多 5 次），导致后面步骤无法进行。

```bash
acme.sh --issue --server letsencrypt_test \
  -d 二级域名.你的域名.com \
  -w /home/vpsadmin/www/webpage \
  --keylength ec-256
```

参数说明：`--server letsencrypt_test` 是"测试服"，发出的证书不能真正使用，但验证流程完全一样；`-d` 后面填你的完整域名；`-w` 后面是第 5 章建好的 Nginx 网站目录；`--keylength ec-256` 选择 ECC 证书（比传统 RSA 证书更小更快）。

看到输出里出现 `Cert success.` 就是成功了。如果报错，在命令末尾加 `--debug` 参数可以看到详细错误信息。

---

**③ 正式申请**

测试没问题后，切换到"正式服"：

```bash
acme.sh --set-default-ca --server letsencrypt   # 切换默认 CA 为 Let's Encrypt
acme.sh --issue -d 二级域名.你的域名.com \
  -w /home/vpsadmin/www/webpage \
  --keylength ec-256 --force
```

`--force` 的原因：测试证书虽然不能用，但在系统里登记为"尚未过期"，不加 `--force` acme.sh 会认为"证书没到期不需要重新申请"而跳过。看到输出里的 CA 地址是 `acme-v02.api.letsencrypt.org`（注意没有 `staging`）就说明是正式证书了。

---

**④ 把证书安装到 Xray 能读到的位置**

证书申请完只是存在 acme.sh 的内部目录里，需要"安装"（其实是复制）到 Xray 配置里指定的路径：

```bash
acme.sh --installcert -d 二级域名.你的域名.com \
  --cert-file /etc/xray/cert/cert.crt \
  --key-file /etc/xray/cert/cert.key \
  --fullchain-file /etc/xray/cert/fullchain.crt \
  --ecc
```

执行完就大功告成。之后第 7 章写 Xray 服务器配置时，会在配置文件里填上这两个路径：`/etc/xray/cert/cert.crt` 和 `/etc/xray/cert/cert.key`。

---

**两个特别要记住的点：**

`cert.key` 是私钥，相当于你网站的"密码"，泄露了别人就能伪造你的网站、发起中间人攻击。它只在服务器上用，永远不要发给任何人，也不要上传到任何地方。

请不要轻易使用自签证书——它没有让操作简单太多，但增加了中间人攻击的风险。真实证书申请麻烦在前期配置，一旦搞定就是全自动的，值得。
 

> [tool_use: web_fetch] {"html_extraction_method": "markdown", "text_content_token_limit": 10000, "url": "https://xtls.github.io/document/level-0/ch06-certificates.html"}

> [tool_result] ---
meta-description: Xray-core
meta-generator: VitePress v2.0.0-alpha.17
meta-viewport: width=device-width,initial-scale=1
title: 【第 6 章】证书管理篇 | Project X
---


[Skip to content](#VPContent)

[![](https://xtls.github.io/logo-dark.svg)![](https://xtls.github.io/logo-light.svg)Project X](https://xtls.github.io/)

搜索`⌘``Ctrl``K`

 Main Navigation [首页](https://xtls.github.io/)

配置指南

[特性详解](https://x
先理解为什么需要证书，再看命令就清晰多了。

TLS 证书是网站的"官方身份证"。浏览器访问 `https://` 开头的网站时，会验证这张证书——只有被权威机构（Certificate Authority，简称 CA）签发的证书才被认可。对 Xray 来说，用真实证书让流量"看起来像正规 HTTPS 网站访问"，是整个伪装方案成立的基础。**这也是为什么第 5 章要先建好 Nginx 网站，再申请证书——申请过程中 Let's Encrypt 会来你的网站取一个验证文件，你得先有个能正常访问的网站。**

> [tool_use: visualize:show_widget] {"loading_messages": ["绘制证书申请流程...", "整理关键命令..."], "title": "acme_sh_cert_flow", "widget_code": "<svg width=\"100%\" viewBox=\"0 0 680 205\" role=\"img\">\n  <title>acme.sh申请TLS证书完整流程</title>\n  <desc>四个步骤：安装acme.sh、测试申请、正式申请、安装到Xray目录，以及生成的三个文件</desc>\n  <defs>\n    <marker id=\"arrow\" viewBox=\"0 0 10 10\" refX=\"8\" refY=\"5\" markerWidth=\"6\" markerHeight=\"6\" orient=\"auto-start-reverse\">

> [tool_result] Content rendered and shown to the user. Please do not duplicate the shown content in text because it's already visually represented. [This tool call rendered an interactive widget in the chat. The user can already see the result — do not repeat it in text or with another visualization tool.]
---

**关键前置概念：Let's Encrypt 怎么确认你真的拥有这个域名？**

acme.sh 用的是"网站根目录验证法"（webroot 方式）：

你向 Let's Encrypt 说"我要给 `a-name.yourdomain.com` 申请证书"，它会回复"那你在这个地址放一个我指定的文件：`http://a-name.yourdomain.com/.well-known/acme-challenge/随机字符`"。acme.sh 自动把这个文件放进 Nginx 的网站目录（命令里 `-w /home/vpsadmin/www/webpage` 那个路径）。Let's Encrypt 从外网来取这个文件，取到了 → 证明你控制这个域名 → 签发证书。这就是为什么第 5 章必须先装好 Nginx——没有它，这个验证就无法完成。

---

**① 安装 acme.sh**

三条命令，顺序执行：

```bash
wget -O - https://get.acme.sh | sh   # 下载并安装
. .bashrc                             # 让 acme.sh 命令立刻生效
acme.sh --upgrade --auto-upgrade     # 开启自动升级
```

安装完成后 acme.sh 就住在你的 `~/.acme.sh/` 目录里，并且会自动在系统里加入一个定时任务（cron job），60 天左右自动帮你续签证书，完全不用操心。

---

**② 先用测试服申请一次**

先用测试命令验证是否可以成功申请，这样可以避免在本地配置有误时，反复申请证书失败，超过 Let's Encrypt 的频率上限（每小时、每个域名失败最多 5 次），导致后面步骤无法进行。

```bash
acme.sh --issue --server letsencrypt_test \
  -d 二级域名.你的域名.com \
  -w /home/vpsadmin/www/webpage \
  --keylength ec-256
```

参数说明：`--server letsencrypt_test` 是"测试服"，发出的证书不能真正使用，但验证流程完全一样；`-d` 后面填你的完整域名；`-w` 后面是第 5 章建好的 Nginx 网站目录；`--keylength ec-256` 选择 ECC 证书（比传统 RSA 证书更小更快）。

看到输出里出现 `Cert success.` 就是成功了。如果报错，在命令末尾加 `--debug` 参数可以看到详细错误信息。

---

**③ 正式申请**

测试没问题后，切换到"正式服"：

```bash
acme.sh --set-default-ca --server letsencrypt   # 切换默认 CA 为 Let's Encrypt
acme.sh --issue -d 二级域名.你的域名.com \
  -w /home/vpsadmin/www/webpage \
  --keylength ec-256 --force
```

`--force` 的原因：测试证书虽然不能用，但在系统里登记为"尚未过期"，不加 `--force` acme.sh 会认为"证书没到期不需要重新申请"而跳过。看到输出里的 CA 地址是 `acme-v02.api.letsencrypt.org`（注意没有 `staging`）就说明是正式证书了。

---

**④ 把证书安装到 Xray 能读到的位置**

证书申请完只是存在 acme.sh 的内部目录里，需要"安装"（其实是复制）到 Xray 配置里指定的路径：

```bash
acme.sh --installcert -d 二级域名.你的域名.com \
  --cert-file /etc/xray/cert/cert.crt \
  --key-file /etc/xray/cert/cert.key \
  --fullchain-file /etc/xray/cert/fullchain.crt \
  --ecc
```

执行完就大功告成。之后第 7 章写 Xray 服务器配置时，会在配置文件里填上这两个路径：`/etc/xray/cert/cert.crt` 和 `/etc/xray/cert/cert.key`。

---

**两个特别要记住的点：**

`cert.key` 是私钥，相当于你网站的"密码"，泄露了别人就能伪造你的网站、发起中间人攻击。它只在服务器上用，永远不要发给任何人，也不要上传到任何地方。

请不要轻易使用自签证书——它没有让操作简单太多，但增加了中间人攻击的风险。真实证书申请麻烦在前期配置，一旦搞定就是全自动的，值得。

### 🤖 Claude

The user wants to understand Chapter 6 - certificate management using acme.sh. Let me fetch the actual chapter content first.
```
This block is not supported on your current device yet.
```

I have all the content. Now let me create a comprehensive explanation with a visualization.

The key concepts to explain:
1. What is a TLS certificate and why we need it (先讲清楚概念)
2. The overall flow of acme.sh (the ACME protocol, Let's Encrypt, how verification works)
3. The specific steps: install → test → apply real → install cert
4. Where the certificate files end up

Let me plan the visual first. I want to create a diagram that explains:
1. What TLS/HTTPS is and why it matters for Xray
2. The ACME challenge/verification process—how Let's Encrypt confirms domain ownership by having acme.sh place a verification file in your Nginx webroot, then checking if it's accessible at the expected location before issuing the certificate
3. The overall flow of the chapter

Now I'm planning the visual layout for this process. I want to create a diagram showing the back-and-forth between your VPS (running Nginx and acme.sh) and Let's Encrypt's servers, with arrows illustrating each step of the verification handshake. Then I'll outline the chapter's progression: installing acme.sh, testing with a staging certificate, obtaining the real certificate, and placing it in the correct location.

Building the verification flow diagram... Writing SVG diagram...

I should start with a conceptual explanation of what TLS actually is and why certificates matter for this use case, then show the ACME verification flow visually. After that, I'll break down the certificate files that get generated—the certificate itself, the private key, and the full chain—and where they're stored in the Xray configuration.

For the diagram, I'm picturing the back-and-forth between acme.sh, Let's Encrypt, and Nginx: acme.sh requests a certificate, Let's Encrypt challenges it by asking for a verification file, acme.sh tells Nginx to create that file in the webroot, and then Let's Encrypt fetches it over HTTP to confirm ownership. Writing SVG diagram... Writing SVG layout... The arrow from acme.sh to LE needs to start at the right edge of the acme.sh box and extend to the left edge of LE, passing visually over the VPS dashed boundary since it's just a stroke with no physical barrier in the SVG.

Now I'm reconsidering the overall layout to make it cleaner—I'll arrange the VPS sub-boxes vertically with acme.sh on top and Nginx below, then position LE to the right with arrows connecting them in the middle area. Let me set up the viewBox dimensions and define the precise coordinates for each element: the VPS boundary as a dashed rectangle, the acme.sh and Nginx boxes inside it, and the LE box positioned to the right with appropriate spacing.

Now I'm mapping out the four main arrows between these components—the certificate request from acme.sh to LE, the validation code response coming back, the verification file being placed in Nginx, and the domain validation flow from LE. I'm reconsidering the approach entirely—instead of getting bogged down in the technical details of the ACME protocol flow, I should focus on what's actually useful: a simple four-stage progression showing the installation, testing, formal application, and certificate installation steps with their corresponding commands.

Building an HTML timeline widget... Writing the verification flow diagram... Writing SVG diagram... The arrow crossing the VPS boundary at that y-position would work fine for showing traffic leaving the system, but the layout still feels cramped. Let me try a completely different approach with a vertical sequential flow instead—showing the verification steps as a narrative progression from top to bottom, starting with the VPS making a request to Let's Encrypt, then the challenge coming back.

Building the SVG layout with step boxes positioned vertically and arrows connecting them...

Actually, I'm realizing this is getting too detailed. Let me simplify to a horizontal pipeline showing the four main stages: installing acme.sh, testing the request, making the formal request, and installing the certificate to Xray. I'll use small boxes with descriptions underneath each stage, connected by arrows—much cleaner and more practical for someone actually following along.

Now I'm working out the exact positioning: four boxes spaced evenly across the canvas with connecting arrows between them at the midpoint height. Calculating the fourth box position at x=515, which gives a right edge of 635px—well within the 680px limit. The arrows connect between boxes at specific x-coordinates. I'm setting the box height to 90px (from y=50 to y=140) with centered content at y=95, then placing descriptive text below at y=155. Each box will display a stage number, title, and key command, with additional explanation labels underneath.

Now I'm checking whether the text widths fit within the boxes. The title "安装 acme.sh" at 14px is roughly 134px wide, which exceeds the 120px box width. I need to either reduce the text size, widen the boxes, or adjust the spacing. If I increase boxes to 140px with 36px gaps, the total becomes 708px—too wide. Trying 130px boxes with 40px gaps instead. Now I'm checking that the text for each step fits within its box—the step numbers and titles are small enough, and the Chinese characters with their widths at 13px all fit comfortably within the 130px box width. I'm also starting to work out the subtitle text styling. Writing SVG diagram... Writing SVG diagram... Writing SVG diagram... Writing SVG diagram... Adjusting the text styling approach for the step labels and verifying that three lines of text fit within the 90-pixel box height. The arrow dimensions look good at 40px with an 8px arrowhead. Now I'm recalculating the viewBox height—the last text element sits at y=163, so I need at least 183 pixels, but I'll round up to 200 for breathing room. Let me verify the x-axis positions for both boxes and the arrow spacing between them. I'm realizing the second line of text in Box 1 is too long—"wget 安装 + 开启自动续期" at around 144 pixels will overflow the 130-pixel box width, so I need to shorten it. Refining the subtitle text for each box to ensure they fit within the width constraints. Box 1 uses a dot separator between the install and auto-update features, Box 2 combines staging with config validation, Box 3 pairs the CA issuance with the 90-day validity period, and Box 4 needs to accommodate the certificate file names which are taking up significant space. All the subtitle text fits within the 130px width constraints now. I'm also checking the note text below each box to make sure those fit as well. I'll structure the response to explain the concept first before diving into the diagram. I'll start with what TLS is and why Xray needs a real certificate, then explain how Let's Encrypt verifies domain ownership through the challenge process, and finally show the four stages visually so users can click through and learn more details.

For the verification concept, I'm thinking of a relatable analogy—like applying for a business license where the government sends an inspector to verify you actually operate there. Let's Encrypt does the same thing by visiting your domain to check for a specific file that only someone with server control could place there.

I should also cover the key technical details: why the document uses ECC (smaller keys mean faster performance and better security), the importance of testing on the staging server first to avoid rate limiting, what the -w parameter does for serving the verification file, and which certificate files matter for the final setup.

Writing the SVG diagram... Writing SVG code... Writing SVG code... Writing SVG diagram... Writing SVG diagram... Checking the text width calculations for the remaining boxes to ensure they fit without overlapping. Box 3's note spans about 60 pixels of space between it and box 4, which is adequate, and box 1's text elements are within their allocated bounds as well. Checking the remaining boxes and text positioning—Box 4's labels fit within bounds, and the certificate filename note at the bottom barely squeezes in at 671 pixels within the 680-pixel limit.

Now I'm verifying the vertical spacing: the boxes sit at y=28 with a height of 90, ending at y=118, then the notes start at y=136, giving an 18-pixel gap which looks right. I'll set the viewBox height to 185 to give some breathing room.

I'm going to structure the response with a conceptual explanation first, then the SVG diagram, followed by detailed step-by-step commands.

For the explanation, I need to cover why TLS/HTTPS matters specifically for Xray, how Let's Encrypt validates domain ownership through the webroot challenge, and why testing with a staging certificate first is important. Then I'll walk through the installation process, testing against the staging environment, switching to the production Let's Encrypt server, and finally installing the certificate.

The core commands involve installing acme.sh, enabling auto-upgrade, running a test issuance to verify everything works, then issuing the real certificate with ECC for better performance, and installing it to the Xray certificate directory. The key flags are the domain name, the Nginx webroot path where Let's Encrypt will place its validation file, the ECC key length for efficiency, and the force flag to ensure renewal even if a cert already exists. Adjusting the SVG viewBox dimensions to properly space the boxes and note lines, making sure there's adequate padding between elements and enough room at the bottom.

Now I'm structuring the explanation to cover why TLS matters for Xray, how the domain verification process works with acme.sh and Let's Encrypt, then laying out the four-stage diagram followed by the command sections for installation, testing, production deployment, and certificate installation.

I'm considering whether to visualize just the pipeline stages or also show the ACME verification flow itself, and thinking about how to represent the resulting certificate files and their role in the Xray configuration.

Writing SVG code... Writing SVG diagram... Writing SVG diagram... Writing SVG code... Box 2 fits at 207-303px with a 92px gap from Box 1. Box 3 needs about 120px and sits at 365-485px with a 62px gap. Box 4 is the tightest at 518-672px with only a 33px gap, but should still be readable.

Actually, let me reconsider Box 4 with a shorter label like "三个证书文件" (about 72px) positioned at 559-631px instead—that gives more breathing room. For Box 1, I need to recount the character widths more carefully since "wget + .bashrc + 自动升级" is coming out longer than my initial estimate. Verifying the width calculations for each box with their mixed Chinese and digit content, making sure everything fits properly with adequate spacing between elements.

Writing SVG code... Writing SVG diagram... Writing SVG code... Adjusting the viewBox height to account for the text baseline positioning and ensuring proper spacing below the notes.

Now I'm writing out the full response with the 4-stage pipeline diagram and explanatory text.先搞清楚一件事：TLS 证书到底是什么，为什么 Xray 非用不可。

这个证书的作用是让你的 VPS 网站具备标准 TLS 加密能力，也就是 HTTPS 访问能力，这是 Xray 等安全代理工具确保流量充分加密的最重要工具。没有它，你的流量加密是不完整的，而且会被 GFW 识别出来。不要轻易使用自签证书，它虽然省事，但增加了中间人攻击的风险。必须用真正由权威机构颁发的证书。

证书从哪来？从一个叫 **Let's Encrypt** 的免费权威机构申请。但它在给你发证书之前，要先确认这个域名真的是你的。怎么确认？它会说："你在 `http://你的域名/.well-known/acme-challenge/某个文件` 放一个我指定的内容，我去访问一下，能取到就证明你控制这个服务器。" 这就是为什么 Nginx 必须在此之前就启动好——它负责把这个验证文件提供给 Let's Encrypt 来访问，一旦验证通过，证书就发给你了。

这也解释了命令里 `-w /home/vpsadmin/www/webpage` 这个参数的含义：它告诉 `acme.sh` 把验证文件放到 Nginx 的网页根目录，让 Let's Encrypt 能通过你的域名访问到它。

整个流程分四步，点击可深入了解：
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

The visualizer seems to be having issues. Let me just provide the text explanation without the diagram. I'll explain everything clearly in prose with the commands.图表工具暂时有些问题，我直接把四步全讲清楚吧。

---

**第 1 步：安装 acme.sh**

acme.sh 是一个简单、轻量、高效的证书管理工具，可以完成证书自动更新。安装只需三条命令，依次运行：

```bash
# 下载并安装
wget -O - https://get.acme.sh | sh

# 让 acme.sh 命令立刻生效（不用重新登录）
. .bashrc

# 开启自动升级，保持工具本身最新
acme.sh --upgrade --auto-upgrade
```

装好之后 acme.sh 会自动设置一个定时任务，每 60 天检查并续期证书，完全不需要你手动操心。

---

**第 2 步：先做测试申请（这步非常重要，很多人跳过）**

在正式申请之前，先用测试命令验证配置是否正确，可以避免反复申请失败，超过 Let's Encrypt 的频率上限（每小时每个域名失败最多 5 次），导致后面的步骤无法进行。

```bash
acme.sh --issue --server letsencrypt_test \
  -d 你的二级域名.你的域名.com \
  -w /home/vpsadmin/www/webpage \
  --keylength ec-256
```

参数解释：
- `--server letsencrypt_test`：向测试服申请，不消耗正式次数
- `-d`：你的完整域名（第 2 章设置过的那个）
- `-w`：Nginx 的网站根目录，acme.sh 把验证文件放这里
- `--keylength ec-256`：使用 ECC 证书，比 RSA 更小更快

这一步申请的是测试证书，不能直接用，只是用来证明你的域名和配置全部正确。你会看到日志里显示 `acme-staging-v02.api.letsencrypt.org`，这个 staging 就是"测试服"。

---

**第 3 步：正式申请**

测试成功后，换成正式服务器再申请一遍：

```bash
# 先设置默认 CA 为 Let's Encrypt
acme.sh --set-default-ca --server letsencrypt

# 正式申请（--force 是因为测试证书还没过期，强制覆盖）
acme.sh --issue \
  -d 你的二级域名.你的域名.com \
  -w /home/vpsadmin/www/webpage \
  --keylength ec-256 \
  --force
```

成功后日志里会显示 `acme-v02.api.letsencrypt.org`，少了 `staging`，就是正式服了。

---

**第 4 步：把证书安装到 Xray 要用的位置**

证书申请成功只是放在了 acme.sh 的内部目录里，还需要"安装"到 Xray 能读到的地方：

```bash
acme.sh --installcert \
  -d 你的二级域名.你的域名.com \
  --cert-file     /etc/xray/cert/cert.crt \
  --key-file      /etc/xray/cert/cert.key \
  --fullchain-file /etc/xray/cert/fullchain.crt \
  --ecc
```

这条命令执行后，`/etc/xray/cert/` 目录下会出现三个文件：

| 文件 | 用途 |
|---|---|
| `cert.crt` | 证书本体（你域名的"身份证"） |
| `cert.key` | 私钥（放在服务器上，永不外传） |
| `fullchain.crt` | 完整证书链（cert + 中间证书，Xray 引用这个） |

---

**最后一个关键点**：至此，Xray 所需的两个基础设施——网站和证书——已经全部就位。第 7 章的 Xray 服务器配置文件里，`certificateFile` 填 `fullchain.crt` 的路径，`keyFile` 填 `cert.key` 的路径，这就是整个第 6 章干的事情的最终交付成果。

想继续看第 7 章 Xray 服务器怎么配置吗？
 

> [tool_use: web_fetch] {"html_extraction_method": "markdown", "text_content_token_limit": 10000, "url": "https://xtls.github.io/document/level-0/ch06-certificates.html"}

> [tool_result] ---
meta-description: Xray-core
meta-generator: VitePress v2.0.0-alpha.17
meta-viewport: width=device-width,initial-scale=1
title: 【第 6 章】证书管理篇 | Project X
---


[Skip to content](#VPContent)

[![](https://xtls.github.io/logo-dark.svg)![](https://xtls.github.io/logo-light.svg)Project X](https://xtls.github.io/)

搜索`⌘``Ctrl``K`

 Main Navigation [首页](https://xtls.github.io/)

配置指南

[特性详解](https://x
先搞清楚一件事：TLS 证书到底是什么，为什么 Xray 非用不可。

这个证书的作用是让你的 VPS 网站具备标准 TLS 加密能力，也就是 HTTPS 访问能力，这是 Xray 等安全代理工具确保流量充分加密的最重要工具。没有它，你的流量加密是不完整的，而且会被 GFW 识别出来。不要轻易使用自签证书，它虽然省事，但增加了中间人攻击的风险。必须用真正由权威机构颁发的证书。

证书从哪来？从一个叫 **Let's Encrypt** 的免费权威机构申请。但它在给你发证书之前，要先确认这个域名真的是你的。怎么确认？它会说："你在 `http://你的域名/.well-known/acme-challenge/某个文件` 放一个我指定的内容，我去访问一下，能取到就证明你控制这个服务器。" 这就是为什么 Nginx 必须在此之前就启动好——它负责把这个验证文件提供给 Let's Encrypt 来访问，一旦验证通过，证书就发给你了。

这也解释了命令里 `-w /home/vpsadmin/www/webpage` 这个参数的含义：它告诉 `acme.sh` 把验证文件放到 Nginx 的网页根目录，让 Let's Encrypt 能通过你的域名访问到它。

整个流程分四步，点击可深入了解：

> [tool_use: visualize:show_widget] {"loading_messages": ["绘制证书流程图...", "整理四个阶段..."], "title": "acme_sh_cert_pipeline", "widget_code": "<svg width=\"100%\" viewBox=\"0 0 680 158\" role=\"img\">\n  <title>acme.sh 证书申请四阶段流程</title>\n  <desc>安装acme.sh、测试申请、正式申请、安装部署四个完整步骤</desc>\n  <defs>\n    <marker id=\"arrow\" viewBox=\"0 0 10 10\" refX=\"8\" refY=\"5\" markerWidth=\"6\" markerHeight=\"6\" orient=\"auto-start-reverse\">\n      <pat

> [tool_result] No result received from the Claude Desktop app after waiting 4 minutes. The local MCP server providing this tool may be unresponsive, crashed, or not running. Further calls to this tool are likely to time out the same way; consider using an alternative approach or ask the user to restart their local MCP servers.

> [tool_use: visualize:show_widget] {"loading_messages": ["绘制证书流程图..."], "title": "acme_cert_steps", "widget_code": "<svg width=\"100%\" viewBox=\"0 0 680 158\" role=\"img\">\n  <title>acme.sh 四阶段流程</title>\n  <desc>安装、测试申请、正式申请、安装证书四步</desc>\n  <defs><marker id=\"arr\" viewBox=\"0 0 10 10\" refX=\"8\" refY=\"5\" markerWidth=\"6\" markerHeight=\"6\" orient=\"auto-start-reverse\"><path d=\"M2 1L8 5L2 9\" fill=\"none\" stroke=\"contex

> [tool_result] No result received from the Claude Desktop app after waiting 4 minutes. The local MCP server providing this tool may be unresponsive, crashed, or not running. Further calls to this tool are likely to time out the same way; consider using an alternative approach or ask the user to restart their local MCP servers.
图表工具暂时有些问题，我直接把四步全讲清楚吧。

---

**第 1 步：安装 acme.sh**

acme.sh 是一个简单、轻量、高效的证书管理工具，可以完成证书自动更新。安装只需三条命令，依次运行：

```bash
# 下载并安装
wget -O - https://get.acme.sh | sh

# 让 acme.sh 命令立刻生效（不用重新登录）
. .bashrc

# 开启自动升级，保持工具本身最新
acme.sh --upgrade --auto-upgrade
```

装好之后 acme.sh 会自动设置一个定时任务，每 60 天检查并续期证书，完全不需要你手动操心。

---

**第 2 步：先做测试申请（这步非常重要，很多人跳过）**

在正式申请之前，先用测试命令验证配置是否正确，可以避免反复申请失败，超过 Let's Encrypt 的频率上限（每小时每个域名失败最多 5 次），导致后面的步骤无法进行。

```bash
acme.sh --issue --server letsencrypt_test \
  -d 你的二级域名.你的域名.com \
  -w /home/vpsadmin/www/webpage \
  --keylength ec-256
```

参数解释：
- `--server letsencrypt_test`：向测试服申请，不消耗正式次数
- `-d`：你的完整域名（第 2 章设置过的那个）
- `-w`：Nginx 的网站根目录，acme.sh 把验证文件放这里
- `--keylength ec-256`：使用 ECC 证书，比 RSA 更小更快

这一步申请的是测试证书，不能直接用，只是用来证明你的域名和配置全部正确。你会看到日志里显示 `acme-staging-v02.api.letsencrypt.org`，这个 staging 就是"测试服"。

---

**第 3 步：正式申请**

测试成功后，换成正式服务器再申请一遍：

```bash
# 先设置默认 CA 为 Let's Encrypt
acme.sh --set-default-ca --server letsencrypt

# 正式申请（--force 是因为测试证书还没过期，强制覆盖）
acme.sh --issue \
  -d 你的二级域名.你的域名.com \
  -w /home/vpsadmin/www/webpage \
  --keylength ec-256 \
  --force
```

成功后日志里会显示 `acme-v02.api.letsencrypt.org`，少了 `staging`，就是正式服了。

---

**第 4 步：把证书安装到 Xray 要用的位置**

证书申请成功只是放在了 acme.sh 的内部目录里，还需要"安装"到 Xray 能读到的地方：

```bash
acme.sh --installcert \
  -d 你的二级域名.你的域名.com \
  --cert-file     /etc/xray/cert/cert.crt \
  --key-file      /etc/xray/cert/cert.key \
  --fullchain-file /etc/xray/cert/fullchain.crt \
  --ecc
```

这条命令执行后，`/etc/xray/cert/` 目录下会出现三个文件：

| 文件 | 用途 |
|---|---|
| `cert.crt` | 证书本体（你域名的"身份证"） |
| `cert.key` | 私钥（放在服务器上，永不外传） |
| `fullchain.crt` | 完整证书链（cert + 中间证书，Xray 引用这个） |

---

**最后一个关键点**：至此，Xray 所需的两个基础设施——网站和证书——已经全部就位。第 7 章的 Xray 服务器配置文件里，`certificateFile` 填 `fullchain.crt` 的路径，`keyFile` 填 `cert.key` 的路径，这就是整个第 6 章干的事情的最终交付成果。

想继续看第 7 章 Xray 服务器怎么配置吗？

### 🧑 Jace

详细讲解第7章Xray服务器配置：VLESS+TLS五大配置模块详解
详细讲解第7章Xray服务器配置：VLESS+TLS五大配置模块详解

### 🤖 Claude

The user wants me to explain Chapter 7 in detail - the Xray server configuration with VLESS+TLS. Let me fetch the actual chapter content first.
```
This block is not supported on your current device yet.
```

Now I have the full content of Chapter 7. Let me plan a comprehensive response.

The chapter covers:
1. Installing Xray (7.2)
2. Configuring TLS certificates for Xray (7.3)
3. Configuring Xray with the config.json (7.4) - the 5 major modules
4. Starting Xray service (7.5)
5. Service management (7.6)
6. Optimization: BBR (7.7)
7. Optimization: HTTP to HTTPS redirect (7.8)

The user asked specifically about the "VLESS+TLS 五大配置模块" (five major configuration modules). So I need to focus on the config.json file and its 5 sections:
1. **log** - logging configuration
2. **dns** - DNS settings
3. **routing** - traffic routing/splitting
4. **inbounds** - incoming traffic configuration (VLESS+TLS)
5. **outbounds** - outgoing traffic configuration

I should explain the key concepts like UUID generation, the VLESS protocol itself, TLS settings in inbounds, the fallback mechanism for port 80, routing rules for blocking private IPs and ads, plus the BBR optimization and HTTP→HTTPS redirect. I'll create a visual showing the 5 modules clearly, then walk through each one in detail.

For the visual, I'm building an SVG diagram that displays the config.json structure with 5 color-coded boxes representing each module, showing how they relate to one another and what each one handles.

I'm thinking the most useful approach would be to visualize the actual traffic flow through the system: a connection arrives at the inbounds listener on port 443 with VLESS+TLS encryption, gets decrypted, then DNS resolves the domain, routing rules evaluate whether to block private/Chinese IPs or ad domains, and finally the request gets forwarded to the appropriate outbound (either direct internet access via "freedom" or dropped into the blackhole). The log module records everything throughout this process. I should also highlight the fallback mechanism where non-VLESS traffic on port 443 gets redirected to port 80.

Designing a flow diagram...

I'm realizing the diagram might get too complex, so I should focus on what actually matters for the user: understanding each of the five modules and what they control, getting a UUID, grasping the fallback mechanism that makes this anti-detection work, how the routing rules filter traffic, and the commands to start and restart the service. Writing SVG visualization... Building the layout... Writing the SVG flowchart... Writing SVG diagram... Refining the SVG layout with precise coordinates for the Freedom box, vertical branches for the Nginx fallback and Block elements, and a DNS annotation above the Routing box, adjusting the viewBox and positioning all elements including the Client box with Chinese text. Adding the remaining routing paths and DNS configuration... Verifying the arrow dimensions and positions across the diagram to ensure everything fits properly within the viewBox constraints.

Now I'm reconsidering whether to label every arrow or just focus on the key decision points to avoid cluttering the diagram. I think I'll simplify by labeling only the main branches and decision nodes. Let me also refine the Inbounds box to display the essential information more clearly, starting with the section header.

Adding the Routing and DNS boxes with their respective labels and content... I'm adding a log box in the top-left corner to track access and error logs, then reconsidering the overall layout positioning since the log module functions as a cross-cutting concern rather than having directional relationships with other components.

Now I need to rethink how the outbounds module is structured—specifically clarifying that "block" and "freedom" are both outbound destinations that the routing rules point to, rather than separate routing concepts.

Adjusting the diagram layout with a clearer viewBox and positioning the zones: Log in the top-left corner, Client on the left side, Inbounds in the center-left, and Routing in the center.

Actually, this is getting too complicated trying to show all the data flows. Let me step back and just visualize the five config modules as a simple vertical list inside a JSON structure frame, with the text explaining how the traffic flows through them.

I'm creating an SVG with a clean layout showing the log, DNS, routing, inbound, and outbound modules stacked vertically, each with a title and brief description of what it does. Now I'm calculating the precise vertical spacing for the five boxes with a 12-pixel gap between them, adjusting the viewBox height to 400 and positioning each element so the text centers align properly within their containers. Writing SVG code... Writing SVG diagram... Writing SVG code... Writing SVG diagram... I realize I can't use HTML entities like `&nbsp;` in SVG text, so I'll swap it out for a bullet separator instead. Using `log · 日志模块` gives me a clean visual separation between the English term and its Chinese translation while keeping the text valid for SVG rendering.

Now I'm checking the text widths to make sure everything fits within the layout bounds. The DNS entry and its description both measure out fine within the available space, so the layout should work without any overflow issues. I'm also reconsidering whether to add JSON bracket visualizations around the boxes—it might make things too cluttered, so I'll leave that out.

I want to add clearer visual indicators for the numbered sections using circled number Unicode characters. The badge positioning needs adjustment—I'm moving the circled number from x=83 to x=75 to better center it within the badge area.

I'm also considering adding a thin vertical separator line at x=92 between the badge and title to create more visual distinction, though I need to verify how SVG stroke rendering works in this context. Writing SVG code... Now I'm structuring the full explanation: starting with a conceptual intro to VLESS+TLS, then walking through each of the five config modules with their specific purposes. For the inbounds section, I need to clarify how VLESS works as a lightweight proxy protocol, explain UUID as the authentication mechanism, reference the TLS certificates from earlier, and describe the fallback mechanism to port 80 for anti-detection. The routing rules block private networks and Chinese IPs, while outbounds handle either allowing traffic through or blocking it entirely.

I should also note the safety measure built into the routing—preventing the VPS from making direct connections to Chinese IPs, which protects against the server being weaponized. The key customization points are the UUID that must match between client and server, the certificate paths, and the optional port 80 fallback for stealth. I'm planning to create a visual diagram showing how these five modules connect together within the config structure. I'll structure this with an intro explaining VLESS+TLS and the config overview, then create an SVG showing the five module cards, followed by detailed explanations of each module and the key commands for managing the service.

Now I'm calculating the SVG dimensions to fit all five boxes with proper spacing and positioning them vertically with a title area at the top. Writing SVG markup... Writing SVG code... Writing SVG diagram... Writing SVG code... Verifying the positions work correctly—the title sits 11px above the box center and the sub sits 12px below, with both glyphs fitting comfortably within the 58px box boundaries. Now I'm calculating the positions for the subsequent boxes, spacing them 12px apart vertically.

Writing SVG code... The full subtitle is overflowing by about 19 pixels, so I need to condense it. I'm trying a shorter version that combines the log paths more efficiently, like "warning 级别 · ~/xray_log/access.log · ~/xray_log/error.log" or abbreviating the file paths to fit within the box constraints.

I'm also checking the routing and inbounds descriptions to make sure they stay within the 350-pixel width limit—things like "屏蔽 geoip:private（私网）· 屏蔽 geoip:cn（国内 IP）· 屏蔽广告域名" for routing and "port 443 · VLESS + TLS · UUID 认证 · 证书路径 · 回落 → port 80" for inbounds.

Now verifying the outbounds and DNS sections fit as well—the outbounds description with freedom and blackhole tags comes to about 380 pixels, and I'm double-checking the DNS configuration text with the DoH encryption details.

I should now write out the clean SVG code. One thing I'm thinking about is whether the circled numbers ①②③④⑤ will render properly across different environments—they're standard Unicode so modern browsers should handle them fine, though I could fall back to regular numbers if needed. I'll stick with the circled versions since they look better. For the font handling, the design system uses Inter for the main text, which should work for CJK characters through browser fallback, though I might want to consider monospace for the code-like paths.

Writing SVG code... Writing SVG markup... Writing SVG code... Writing SVG diagram... Writing SVG code... I'm trying different text combinations to fit within the width constraint. Let me test a more compact version using mixed Chinese and English that keeps the essential information about the port, protocol, encryption, and fallback behavior while staying under the pixel limit. Calculating text width for a shorter version...

Now I'm checking the routing rules for blocking private IPs, Chinese geoip, and ad domains—that comes to around 376 pixels, which fits within the target range. Let me finalize the subtitle texts for each section. I've confirmed the text dimensions for all five sections. Now I'm setting up the SVG layout with precise y-coordinates for each box and its subtitle, positioning them at consistent 70-pixel intervals down the diagram. Writing the SVG now...

I should also cover the installation steps, certificate setup, and the main workflow—installing Xray, configuring the cert files, understanding the five config modules as the core focus, and then running the service.

For the prose, I'll start by explaining what VLESS+TLS actually is conceptually, then show the five-module diagram, and walk through each one: the log module with its three simple settings, the DNS module using encrypted DoH queries through Cloudflare, and continue from there.

Continuing with routing rules: there are three blocking policies that prevent abuse—private IPs get blocked to stop internal network exploitation, Chinese IPs get blocked so the VPS doesn't become a tool for attacking domestic servers, and ad domains get filtered out. Anything that doesn't match these rules flows through the default outbound. Then the inbounds section is where it gets complex, starting with listening on port 443 with the VLESS protocol.

The UUID acts as a password token that must match exactly between server and client, and I'm using the xtls-rprx-vision flow mode for better performance. Since VLESS doesn't add its own encryption layer (TLS handles that), decryption is set to none. The fallbacks mechanism is the anti-detection trick—if incoming traffic doesn't look like VLESS, it gets forwarded to port 80 where Nginx is running, making the proxy look like a regular web server. TLS security is enabled with certificate paths pointing to the files from earlier setup.

For outbounds, there are just two: the freedom outbound for normal internet traffic and the blackhole outbound that discards blocked traffic.

I need to generate a UUID using the xray command and paste it into both server and client configs. The fallback mechanism is crucial—Xray listens on 443, validates VLESS connections, and forwards anything suspicious to Nginx on 80 so probing tools get a normal website response. I'm also enabling BBR, a TCP congestion algorithm that improves throughput, by adding configuration to the sysctl file. I should also cover the anti-detection strategies, the routing rules that filter traffic, and how all five modules interconnect to create a cohesive system.先来建立一个整体印象：Xray 的 `config.json` 无论服务器还是客户端都由同样的 5 个模块组成，就像一条流水线，每个模块负责一件事。常用的 config 文件，不论服务器端还是客户端，都有 5 个部分：log 日志、dns 设置、routing 分流、inbounds 入站、outbounds 出站。
```
This block is not supported on your current device yet.
```

Now I have the design system rules. Let me create the SVG showing the 5 config modules.

Key rules from the spec:
- Use 2-3 colors max per diagram. I should NOT use 5 different colors (one per module). Let me pick 2-3 colors that group the modules by function.
- Box width must fit content
- Text at 14px/12px
- viewBox must be 680 wide

With the color restriction (2-3 colors max), let me think about the grouping:
- Infrastructure/Setup: log (gray), dns (blue), routing (amber) → maybe group as "gray" (neutral/structural)
- The core connection: inbounds + outbounds → maybe "coral" for in and "teal" for out

Actually, I need to reduce this to 3 colors max. Let me group them by function: gray for infrastructure (log, dns), amber for the routing decision-maker, and coral for inbounds as the entry point, with teal for outbounds as the exit. But that's 4 colors, so I'll consolidate—maybe gray for log and dns, amber for routing, and coral for both inbounds and outbounds since they're the data flow endpoints. I'm settling on using 4 colors to balance the spec's guidance with the need to distinguish these functionally different modules—gray for logging, blue for DNS as a system component, amber for routing decisions, and coral and teal to differentiate the entry and exit points.

Now I'm drafting the subtitles for each box, keeping them to 5 words or fewer as specified. I need to make sure the Chinese descriptions are concise while capturing what each module does—access and error logging for the log box, encrypted DNS queries for DNS, blocking rules for routing, the inbound protocol details, and the two outbound paths.

I'm also starting to work through the sizing calculations based on the font calibration data, figuring out how wide each box needs to be given the character counts at the specified font size. All the titles and subtitles fit comfortably within the 600px width, so I'll use that as my standard box width. For the box heights, I need about 56px to accommodate both the title at 14px and subtitle at 12px, with the title centered around Y+18 and the subtitle positioned lower at Y+38.

Now I'm calculating the overall layout: five boxes at 56px each with 12px gaps between them gives me 328px total height, starting from y=40 and ending at y=368, which means my viewBox should be 400px tall. I'm positioning the boxes vertically at y=40, 108, 176, 244, and 312, and I need to figure out the exact text positioning within each box—the title goes at Y+18, the subtitle at Y+40, and the badge centered at Y+28. Positioning the badge at x=68 as the midpoint between the box edge and title start, then adjusting the title to x=95 for a clean 3px gap from the badge area.

I'm realizing the spec requires short subtitles—no more than 5 words each—so I need to trim them down significantly while keeping the key information about what each section covers.

Now I'm hitting a strict constraint on colors: maximum 2 color ramps per diagram. This is quite limiting, so I'm weighing options like using a neutral gray for most boxes and reserving a second color like coral or amber to highlight the most critical component, whether that's the inbounds section or the routing logic. I'm realizing the 2-ramp constraint means I need to group these modules by function rather than treating each as distinct. So I'll use gray for the supporting configuration pieces—logging, DNS, routing, and outbounds—and reserve coral specifically for inbounds since that's the unique Xray-specific entry point that defines the whole system. I'm realizing the 2-color constraint is pretty strict, so let me step back and use structure instead of color variation to make the diagram interesting. I'll keep all 5 modules in gray and show the traffic flow through arrows and positioning, adding a legend to explain the functional groupings if needed. I'm overthinking the color scheme here. Let me just commit to a 2-color approach: c-gray for the configuration modules (log, dns, outbounds) and c-coral for the active traffic handling (routing, inbounds). That respects the spec's constraint and makes semantic sense.

Now I'll build the SVG with a clean vertical stack of these five boxes, adding a flow indicator on the side to show how traffic moves through the system. is to keep colors meaningful rather than purely decorative. For this diagram, I'm splitting the five modules into two semantic groups: infrastructure components like logging and DNS in gray, and traffic-handling modules like routing, inbounds, and outbounds in coral. I'll add a small horizontal legend to clarify this distinction, then lay out the boxes starting from y=50 with the appropriate colors.

Writing SVG code... Writing SVG code... 158, badge=146. Let me verify box ① actually contains these elements: it spans from y=50 to y=106, so the title at y=68 and subtitle at y=90 both fall within those bounds, and the badge at y=78 sits right at the center (50+28). Now I'm double-checking all the positioning across the remaining boxes. The glyph positioning checks out with the title and subtitle centered at their respective y-coordinates, giving me roughly 9-11px padding on all sides within the box. Now I'm setting up a small legend at y=34 with two colored dots and labels for the system configuration and traffic processing categories. Writing SVG legend... I'm reconsidering the legend approach—the full labels are getting too long. I could simplify it to just color names in Chinese, or add a compact legend below the diagram showing which color represents which category. Let me go with a minimal note approach instead of cluttering the SVG with extra text. I'm settling on using two color ramps with a legend to properly distinguish between infrastructure and traffic handling modules, which aligns with the spec's requirement for meaningful color encoding. Now I'll write the SVG code. Writing SVG diagram... Writing SVG code... Writing SVG diagram... Checking the text width calculations for the subtitle elements to ensure they fit properly within the SVG bounds. ending at ~458px. ✓ All the text fits within the bounds. Now checking the NOTE section at y=400, which contains instructions about customizing the UUID and certificate paths. That's roughly 365px wide when centered, extending from about 158 to 522 on the x-axis, so it fits as well. ✓ The note sits 22px below the last box, providing good visual separation. For the viewBox height, I need to account for the note's vertical extent around y=400 plus some padding, so 430 should work well. I'm simplifying the note text to just "需要自定义：UUID 和证书路径" to keep it concise.

Actually, I'm reconsidering whether to include the note at all—maybe it's cleaner to skip it in the diagram and explain those details in accompanying prose instead, letting the SVG focus on showing just the five modules.

Writing SVG code... Writing SVG diagram... Writing SVG code... Writing SVG diagram... Checking the subtitle text widths to ensure they fit within the container bounds—the first subtitle spans about 326 pixels starting at position 96, ending at 422, which is within limits. Moving on to verify the second subtitle's character widths for the mixed Latin and CJK text. Checking the width calculations for the remaining text blocks—the port configuration line comes to about 355px, and the freedom/blackhole definitions are being measured similarly with their Latin and CJK character combinations. The spacing checks out—all the legend items and colored indicators have proper gaps with no overlaps. Now I'm ready to structure the response with an introductory explanation, the visual diagram, detailed breakdowns of each module, and the key commands.

For the subtitle on module ④, I need to trim it down since it's exceeding the 5-word limit. Let me condense the protocol and configuration details into something more concise. The subtitle fits within the width constraints, so I'll stick with it. Now I'm ready to write out the actual SVG widget and accompanying explanation, covering what VLESS and TLS do, how UUID generation works, and the fallback mechanism.

I'll also need to explain the routing rules using geoip and geosite filtering, walk through starting and checking the service, and touch on BBR optimization—keeping it concise since there's a lot of ground to cover.这是整个教程中最核心的章节。前 6 章铺垫的一切——VPS、SSH、Nginx、TLS 证书——到这里才真正派上用场。 安装 Xray 本身只需三条命令，复杂的部分全在 `config.json`。
```
This block is not supported on your current device yet.
```

The visualizer tool keeps timing out. Let me just give a comprehensive text-based explanation without the widget.

I'll explain all 5 modules clearly in prose with code blocks for the key parts of the config.json.图表工具暂时不可用，我直接把五个模块逐一讲透。

---

**安装 Xray（三步完成）**

```bash
wget https://github.com/XTLS/Xray-install/raw/main/install-release.sh
sudo bash install-release.sh
rm ~/install-release.sh
```

安装完成后，先生成一个 UUID 备用：

```bash
xray uuid
```

UUID 可以粗暴理解为像指纹一样几乎不会重复的 ID，它是服务器和客户端之间唯一的"通行证"，后面配置文件里必须填入，客户端也要用同一个。

---

**五大模块逐一解析**

**① log（日志）**

最简单的模块，就三个设置：日志级别用 `warning`（只记录警告和错误，不记录每次连接），访问日志写到 `~/xray_log/access.log`，错误日志写到 `~/xray_log/error.log`。这两个文件要提前用 `touch` 命令创建好，并赋予写入权限。

**② dns（DNS 解析）**

首选 `https+local://1.1.1.1/dns-query`，这是 1.1.1.1 的 DoH 查询方式，牺牲速度但可防止 ISP 偷窥。`https+local://` 的意思是：用 DoH（DNS over HTTPS，加密的 DNS 查询）向 Cloudflare 的 `1.1.1.1` 服务器查询，让 ISP 看不到你在解析什么域名，防止 DNS 污染。

**③ routing（分流路由）——"大脑"**

这是配置里规则最多的部分，有三条屏蔽规则：

第一条：`geoip:private` → `block`。凡是目标是私网/内网 IP 的流量，全部丢进黑洞。防止有人滥用你的服务器攻击内网或造成奇怪的回环。

第二条：`geoip:cn` → `block`。凡是目标是中国大陆 IP 的流量，也丢进黑洞。这不是限制你访问，而是防止你的海外 VPS 被用来直连国内服务器（可能引起不必要的麻烦）。

第三条：`geosite:category-ads-all` → `block`。所有知名广告域名直接屏蔽。

不匹配任何规则的流量，默认走 `direct` 出站（即 freedom，直连互联网）。

`geoip` 和 `geosite` 是 Xray 内置的两个大型地理位置/域名数据库文件，不需要你维护，安装时自带。

**④ inbounds（入站）——整个配置的核心**

这是最复杂也最重要的部分，包含几个关键概念：

**VLESS 协议**：Xray 的核心代理协议，极轻量，本身不加密（加密由外层 TLS 负责），所以速度更快。

**UUID**：这就是你刚才用 `xray uuid` 生成的那串 ID。客户端连接时必须携带同样的 UUID，否则服务器拒绝——这就是"密码"。填在配置的 `"id": ""` 里。

**TLS 证书路径**：certificateFile 填 `~/xray_cert/xray.crt`，keyFile 填 `~/xray_cert/xray.key`，这正是第 6 章安装好的那两个文件。

**回落（fallback）机制**——这是整个安全体系最精妙的地方：Xray 监听 443 端口，如果来的流量是合法 VLESS，正常处理；如果不是 VLESS（比如 GFW 主动探测来试探这个端口上跑的是什么），流量就被转发到 80 端口，Nginx 就在那里等着，返回一个正常的网站页面。探测工具看到的是合法网站，自然不会干扰它。这就是第 5 章必须建网站的根本原因。

**⑤ outbounds（出站）——两个"目的地"**

只有两个出站：

`freedom`（tag 叫 `direct`）：流量直接从 VPS 发出去访问真实目标。这是大多数流量的归宿。

`blackhole`（tag 叫 `block`）：流量进去什么也出不来，直接丢弃。③ routing 里屏蔽的三类流量，就是被送到这里。

**routing 和 outbounds 的关系很关键**：routing 里写 `"outboundTag": "block"`，Xray 就去找 outbounds 里 tag 等于 `"block"` 的那个（blackhole）；写 `"outboundTag": "direct"`，就走 freedom。两者通过 tag 名称对应，名字必须匹配。

---

**让 Xray 跑起来**

```bash
sudo systemctl start xray      # 启动
sudo systemctl status xray     # 看状态（绿色 active running 就成了）
sudo systemctl enable xray     # 设开机自启
```

**顺手开启 BBR（强烈推荐）**

BBR 是一种 TCP 拥塞控制算法，有和没有会有可感知的速度、稳定性差别，所以非常建议开启。但不必纠结 BBR 版本，跟随你的发行版更新内核即可，那些"魔改 BBR"不要用。开启方法：

```bash
sudo nano /etc/sysctl.d/99-bbr.conf
```

写入这两行，保存退出：

```
net.core.default_qdisc=fq
net.ipv4.tcp_congestion_control=bbr
```

```bash
sudo sysctl --system            # 让配置生效
sysctl net.ipv4.tcp_congestion_control  # 确认，返回 bbr 就对了
```

---

到这里服务器端就全部配置完成了。你已经拥有了可以正常科学上网的服务器，同时也有了防止主动探测攻击的伪装网站。第 8 章就是给你本地电脑配置客户端，两端都就位之后就能用了。要继续讲第 8 章吗？
 

> [tool_use: web_fetch] {"html_extraction_method": "markdown", "text_content_token_limit": 12000, "url": "https://xtls.github.io/document/level-0/ch07-xray-server.html"}

> [tool_result] ---
meta-description: Xray-core
meta-generator: VitePress v2.0.0-alpha.17
meta-viewport: width=device-width,initial-scale=1
title: 【第 7 章】Xray 服务器篇 | Project X
---


[Skip to content](#VPContent)

[![](https://xtls.github.io/logo-dark.svg)![](https://xtls.github.io/logo-light.svg)Project X](https://xtls.github.io/)

搜索`⌘``Ctrl``K`

 Main Navigation [首页](https://xtls.github.io/)

配置指南

[特性详解](https
先来建立一个整体印象：Xray 的 `config.json` 无论服务器还是客户端都由同样的 5 个模块组成，就像一条流水线，每个模块负责一件事。常用的 config 文件，不论服务器端还是客户端，都有 5 个部分：log 日志、dns 设置、routing 分流、inbounds 入站、outbounds 出站。

> [tool_use: visualize:read_me] {"modules": ["diagram"], "platform": "desktop"}

> [tool_result] # Imagine — Visual Creation Suite

## Modules
Call read_me again with the modules parameter to load detailed guidance:
- `diagram` — SVG flowcharts, structural diagrams, illustrative diagrams
- `mockup` — UI mockups, forms, cards, dashboards
- `interactive` — interactive explainers with controls
- `chart` — charts, data analysis, geographic maps (Chart.js, D3 choropleth)
- `art` — illustration and
这是整个教程中最核心的章节。前 6 章铺垫的一切——VPS、SSH、Nginx、TLS 证书——到这里才真正派上用场。 安装 Xray 本身只需三条命令，复杂的部分全在 `config.json`。

> [tool_use: visualize:show_widget] {"loading_messages": ["绘制配置模块图...", "整理五大模块..."], "title": "xray_config_five_modules", "widget_code": "<svg width=\"100%\" viewBox=\"0 0 680 400\" role=\"img\">\n  <title>Xray 服务器端 config.json 五大模块</title>\n  <desc>灰色为系统配置（log、dns），橙色为流量处理（routing、inbounds、outbounds），点击各模块了解详情</desc>\n\n  <text class=\"th\" x=\"340\" y=\"18\" text-anchor=\"middle\">服务器端 config.json · 五大模块</text>\n\n  <g class=\"c-

> [tool_result] No result received from the Claude Desktop app after waiting 4 minutes. The local MCP server providing this tool may be unresponsive, crashed, or not running. Further calls to this tool are likely to time out the same way; consider using an alternative approach or ask the user to restart their local MCP servers.
图表工具暂时不可用，我直接把五个模块逐一讲透。

---

**安装 Xray（三步完成）**

```bash
wget https://github.com/XTLS/Xray-install/raw/main/install-release.sh
sudo bash install-release.sh
rm ~/install-release.sh
```

安装完成后，先生成一个 UUID 备用：

```bash
xray uuid
```

UUID 可以粗暴理解为像指纹一样几乎不会重复的 ID，它是服务器和客户端之间唯一的"通行证"，后面配置文件里必须填入，客户端也要用同一个。

---

**五大模块逐一解析**

**① log（日志）**

最简单的模块，就三个设置：日志级别用 `warning`（只记录警告和错误，不记录每次连接），访问日志写到 `~/xray_log/access.log`，错误日志写到 `~/xray_log/error.log`。这两个文件要提前用 `touch` 命令创建好，并赋予写入权限。

**② dns（DNS 解析）**

首选 `https+local://1.1.1.1/dns-query`，这是 1.1.1.1 的 DoH 查询方式，牺牲速度但可防止 ISP 偷窥。`https+local://` 的意思是：用 DoH（DNS over HTTPS，加密的 DNS 查询）向 Cloudflare 的 `1.1.1.1` 服务器查询，让 ISP 看不到你在解析什么域名，防止 DNS 污染。

**③ routing（分流路由）——"大脑"**

这是配置里规则最多的部分，有三条屏蔽规则：

第一条：`geoip:private` → `block`。凡是目标是私网/内网 IP 的流量，全部丢进黑洞。防止有人滥用你的服务器攻击内网或造成奇怪的回环。

第二条：`geoip:cn` → `block`。凡是目标是中国大陆 IP 的流量，也丢进黑洞。这不是限制你访问，而是防止你的海外 VPS 被用来直连国内服务器（可能引起不必要的麻烦）。

第三条：`geosite:category-ads-all` → `block`。所有知名广告域名直接屏蔽。

不匹配任何规则的流量，默认走 `direct` 出站（即 freedom，直连互联网）。

`geoip` 和 `geosite` 是 Xray 内置的两个大型地理位置/域名数据库文件，不需要你维护，安装时自带。

**④ inbounds（入站）——整个配置的核心**

这是最复杂也最重要的部分，包含几个关键概念：

**VLESS 协议**：Xray 的核心代理协议，极轻量，本身不加密（加密由外层 TLS 负责），所以速度更快。

**UUID**：这就是你刚才用 `xray uuid` 生成的那串 ID。客户端连接时必须携带同样的 UUID，否则服务器拒绝——这就是"密码"。填在配置的 `"id": ""` 里。

**TLS 证书路径**：certificateFile 填 `~/xray_cert/xray.crt`，keyFile 填 `~/xray_cert/xray.key`，这正是第 6 章安装好的那两个文件。

**回落（fallback）机制**——这是整个安全体系最精妙的地方：Xray 监听 443 端口，如果来的流量是合法 VLESS，正常处理；如果不是 VLESS（比如 GFW 主动探测来试探这个端口上跑的是什么），流量就被转发到 80 端口，Nginx 就在那里等着，返回一个正常的网站页面。探测工具看到的是合法网站，自然不会干扰它。这就是第 5 章必须建网站的根本原因。

**⑤ outbounds（出站）——两个"目的地"**

只有两个出站：

`freedom`（tag 叫 `direct`）：流量直接从 VPS 发出去访问真实目标。这是大多数流量的归宿。

`blackhole`（tag 叫 `block`）：流量进去什么也出不来，直接丢弃。③ routing 里屏蔽的三类流量，就是被送到这里。

**routing 和 outbounds 的关系很关键**：routing 里写 `"outboundTag": "block"`，Xray 就去找 outbounds 里 tag 等于 `"block"` 的那个（blackhole）；写 `"outboundTag": "direct"`，就走 freedom。两者通过 tag 名称对应，名字必须匹配。

---

**让 Xray 跑起来**

```bash
sudo systemctl start xray      # 启动
sudo systemctl status xray     # 看状态（绿色 active running 就成了）
sudo systemctl enable xray     # 设开机自启
```

**顺手开启 BBR（强烈推荐）**

BBR 是一种 TCP 拥塞控制算法，有和没有会有可感知的速度、稳定性差别，所以非常建议开启。但不必纠结 BBR 版本，跟随你的发行版更新内核即可，那些"魔改 BBR"不要用。开启方法：

```bash
sudo nano /etc/sysctl.d/99-bbr.conf
```

写入这两行，保存退出：

```
net.core.default_qdisc=fq
net.ipv4.tcp_congestion_control=bbr
```

```bash
sudo sysctl --system            # 让配置生效
sysctl net.ipv4.tcp_congestion_control  # 确认，返回 bbr 就对了
```

---

到这里服务器端就全部配置完成了。你已经拥有了可以正常科学上网的服务器，同时也有了防止主动探测攻击的伪装网站。第 8 章就是给你本地电脑配置客户端，两端都就位之后就能用了。要继续讲第 8 章吗？

