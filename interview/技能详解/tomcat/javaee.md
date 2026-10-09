# 一句话先讲清楚：Jakarta EE（原Java EE）规范到底是什么
**它不是代码、不是jar包，是一套书面契约集合**。
定义：企业Java里各个组件**必须具备什么行为、接口长什么样、异常怎么抛、生命周期规则**。
任何容器（Tomcat、WildFly、TomEE）想要宣称自己兼容这个规范，就必须遵守文档写的全部规则，并且跑通官方的TCK兼容性测试套件。

> 类比你之前学的：
> JLS = Java语言语法契约；JVMS = JVM运行契约
> **Jakarta EE = 企业级组件契约（Servlet、事务、持久化等）**

每一条独立规范，都固定包含3样东西：
1. Specification PDF：文字描述行为规则（核心契约文档）
2. API / Javadoc：接口定义（`jakarta.servlet.*`这类包）
3. TCK 测试套件：用来验证实现是否符合规范（Tomcat就要跑Servlet的TCK）

## 官方总入口（你要的参考资料，权威基准）
👉 总规范页面：https://jakarta.ee/specifications/
这里列出全部独立规范，可直接打开PDF / HTML文档、API文档

### 对你当前学习（Tomcat、面试）最重要的2个
1. **Jakarta Servlet 规范（重中之重，Tomcat只实现这一个主规范）**
地址：https://jakarta.ee/specifications/servlet/
> 规定：Servlet生命周期、request/response、filter、listener、web.xml、异步AsyncContext、session规则。**Tomcat的全部web能力，都必须遵守这份文档**。你读Tomcat架构/源码，都以这份文档作为真理标准。

2. Jakarta EE Platform 平台总规范
是一个“总纲”，定义整套Jakarta EE平台需要包含哪些子规范，适合宏观了解，日常深挖Tomcat不用精读。

其他高频子规范（后面面试会碰到）
- Jakarta Transactions（JTA，分布式事务）
- Jakarta CDI（依赖注入，类似Spring IOC的原生规范）
- Jakarta Persistence（JPA，ORM规范，Hibernate是它的实现）
- Jakarta Validation（参数校验，Hibernate Validator实现）

## 分层放到你已有的模型里
```
Java SE（JLS + JVM规范）
        ↓
Jakarta EE 【契约层】（一堆独立spec：Servlet/JTA/JPA/CDI，接口+行为规则）
        ↓
实现产品层：
    Tomcat：只实现Servlet、WebSocket等Web子集（不是完整Jakarta EE服务器）
    TomEE / WildFly / GlassFish：完整实现全套Jakarta EE规范
        ↓
业务应用层：SpringBoot Web项目（底层使用Servlet这套契约）
```

## 阅读策略（非常关键，避免啃不动大PDF）
> 规范文档英文、文字枯燥，**不要从头到尾通读全书**，和JVMS一样：按需查阅。
1. 现阶段目标：**Jakarta Servlet规范**，只看这一份
2. 阅读方式：**带着问题检索**
比如：
- Servlet什么时候初始化？
- Filter执行顺序规则是什么？
- HttpSession什么时候失效？
- async异步请求的流转规则？
去文档里直接搜对应的章节，**用来验证书上/博客说法是否正确**（这就是你想要的“官方基准”，不再只看面试题总结）
3. 配套官方教程（相对友好，带demo）
https://jakarta.ee/learn/docs/jakartaee-tutorial/current/

## 历史小背景（面试偶尔问到）
早年叫Java EE，由Oracle维护；版权移交Eclipse基金会之后，改名 **Jakarta EE**，包名从`javax.*` → `jakarta.*`。
- javax.servlet：Java EE时代
- jakarta.servlet：Jakarta EE9+

## 实操建议（和你“触摸JVM”思路对齐）
1. 打开Servlet规范PDF，找到Servlet生命周期章节；
2. 写一个简单Servlet，添加`init() / destroy()`，打日志；
3. 在Tomcat里部署，启动/停止，**验证行为是否和规范文档描述一致**。
> 这就是亲手验证契约，而不是只看书本二手总结。

如果你想，我们直接打开Servlet规范，优先看**Servlet生命周期**这一章。