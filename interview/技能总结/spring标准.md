# Spring 模块｜资深后端面试学习方案

对齐前面统一范式：**官方文档为基准 + 知识范围 + 掌握程度 + 实操清单 + 避坑（网上面试题常见错误）**

> 区分：Spring Core（IOC/AOP/ 事务）是核心；SpringBoot 是基于 Spring 的快速开发封装。
>
> &#x20;官方文档：[https://docs.spring.io/spring-framework/reference/](https://link.wtturl.cn/?target=https%3A%2F%2Fdocs.spring.io%2Fspring-framework%2Freference%2F\&scene=im\&aid=582478\&lang=zh "autolink")
>
> &#x20;SpringBoot 官方文档：[https://docs.spring.io/spring-boot/reference/](https://link.wtturl.cn/?target=https%3A%2F%2Fdocs.spring.io%2Fspring-boot%2Freference%2F\&scene=im\&aid=582478\&lang=zh "autolink")

> 阅读策略：文档不用全通读。**文档用来校准定义，书籍搭建骨架，demo 验证，最后场景题检验**
>
> &#x20;推荐配套书籍：《Spring 实战》、《Spring 源码深度解析》（仅做骨架，歧义回官方文档核对）

## 🔴 核心模块清单（资深面试深挖）

## 1. IOC 容器（Inversion of Control 控制反转）

### 核心知识点

1. IoC 思想：**控制反转**，把对象创建、依赖管理交给容器，不是自己 new；DI 依赖注入是 IoC 的实现手段。
2. Bean 定义、Bean 的作用域：singleton、prototype、request、session、application
   - singleton：容器创建时实例化（默认）；lazy 懒加载则第一次获取才创建
3. Bean 完整生命周期（高频）

   &#x20;实例化 → 属性填充 populateBean → 初始化（各种后置处理器）→ 销毁
   - 回调接口：`InitializingBean`、`DisposableBean`、`@PostConstruct`、`@PreDestroy`
   - BeanPostProcessor（Bean 后置处理器，AOP 的基石）
4. **循环依赖（重中之重）**
   - 什么场景会产生循环依赖
   - Spring 三级缓存设计：`singletonObjects`、`earlySingletonObjects`、`singletonFactories`
   - 为什么需要三级缓存，二级缓存行不行？
   - 哪些场景**无法解决循环依赖**：prototype 作用域、构造器注入循环依赖

> 官方文档原文：只描述行为，**三级缓存属于 Spring 内部实现细节，不是规范**。网上很多简化解释容易出错。

✅ 掌握程度：

&#x20;口述完整生命周期；画图解释三级缓存，讲清楚限制边界，回答 “为什么构造注入不能解决循环依赖”。

&#x20;✅ 实操 Demo：

- 写`@Component`循环依赖（setter 注入，可以解决）
- 修改为构造器注入，直接复现循环依赖报错，对比两者差异
- 加上`@Lazy`看效果

## 2. AOP 面向切面编程

### 核心知识点

1. AOP 概念：连接点 JoinPoint、切点 Pointcut、通知 Advice（前置 / 后置 / 异常 / 最终 / 环绕）、切面 Aspect、目标对象 Target、代理对象 Proxy
2. 两种动态代理：
   - JDK 动态代理：**目标必须实现接口**，代理接口方法
   - CGLIB 代理：继承目标类，类代理，不需要接口；无法代理 final 类 /final 方法
3. Spring 什么时候选 JDK、什么时候 CGLIB（SpringBoot2.x 默认 CGLIB）
4. **AOP 失效场景【面试高频大坑】**
   > 根源：AOP 是代理对象生效；**同类内方法自调用，不走代理，切面失效**
   >
   > &#x20;举例：A 方法（加 @Around）内部直接调用本类 B 方法（有切面），B 的切面不会执行。
   >
   > &#x20;其他失效：private/final/static 方法不能被拦截；目标对象没有被 Spring 容器管理。

✅ 掌握程度：

&#x20;讲清代理选择规则，能说出全部 AOP 失效场景，解释底层原因。

&#x20;✅ 实操 Demo：

&#x20;写切面，复现**同类方法自调用导致 AOP 失效**；用`ApplicationContext`拿到代理对象解决这个问题。

## 3. Spring 事务（PlatformTransactionManager，最高频）

### 核心知识点

1. 事务底层接口：`PlatformTransactionManager`、`TransactionDefinition`、`TransactionStatus`
2. 隔离级别（Isolation）：和数据库隔离级别一一对应，Spring 只是封装，**最终由数据库控制**
3. 传播行为 Propagation（7 种，重点理解 REQUIRED、REQUIRES\_NEW、NESTED、SUPPORTS）
   - REQUIRED：当前有事务就加入，没有新建（默认）
   - REQUIRES\_NEW：新建独立事务，挂起原有
   - NESTED：嵌套事务，保存点 savepoint，依赖外层事务提交 / 回滚
   > 高频追问：NESTED 和 REQUIRES\_NEW 的本质区别
4. @Transactional 事务失效场景（必背，资深连环追问）
   1. 方法不是 public
   2. 同类内方法自调用（AOP 代理失效）
   3. 异常不是 RuntimeException/Error；捕获异常不抛出
   4. 多线程：新开线程抛出异常，不会回滚主线程事务
   5. 数据库本身不支持事务（MyISAM）
   6. 传播行为配置不当
5. 事务超时、只读、回滚规则

✅ 掌握程度：

&#x20;7 种传播行为适用场景；完整列举事务失效场景 + 底层原理；嵌套事务场景题分析。

&#x20;✅ 实操 Demo：

&#x20;逐个复现事务失效场景：

- 同类方法调用，事务不回滚
- try-catch 捕获异常不抛出，事务不回滚
- REQUIRES\_NEW / NESTED 嵌套事务对比，观察回滚差异

## 4. SpringBoot （属于 Spring 生态封装，和 SpringCore 绑定考察）

### 核心知识点

1. 自动装配 `@EnableAutoConfiguration`：`META-INF/spring.factories` / SpringBoot2.7+ META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
2. Starter：场景启动器，不是代码，是依赖 + 自动配置类集合
3. 配置加载优先级（application.yml、bootstrap.yml、环境变量、命令行参数）
4. 条件注解 `@ConditionalOnClass`、`@ConditionalOnMissingBean`

✅ 掌握程度：理解自动装配流程，知道新旧版本配置文件改动；能回答 starter 的设计思想。

&#x20;✅ 实操：自定义一个 starter。

# 📌 Spring 高频坑（网上面试题经常错误，以官方文档为准）

1. ❌ 错误：三级缓存是 Spring 规范定义

   &#x20;✅ 三级缓存是**Spring 内部实现**，官方文档不会写这个；只是为了解决单例 setter 循环依赖而做的工程优化。
2. ❌ 错误：AOP 可以拦截 private 方法

   &#x20;✅ 不管 JDK/CGLIB，private 方法无法被代理，AOP 无法生效
3. ❌ 错误：Spring 事务隔离级别是 Spring 自己实现

   &#x20;✅ Spring 只是设置 SQL 的隔离级别，**隔离能力完全由数据库引擎 InnoDB 提供**
4. ❌ 混淆 NESTED 和 REQUIRES\_NEW：

   &#x20;REQUIRES\_NEW 是独立事务，外层回滚不影响内层；

   &#x20;NESTED 是保存点，外层事务回滚，嵌套事务一起回滚。

# 🧪 Spring 整套学习步骤（沿用之前统一流程）

1. 阅读 Spring 官方文档 Core 部分（IoC / AOP / Transaction），建立定义
2. 配套书籍梳理源码骨架（Bean 生命周期、三级缓存）
3. 动手写上面列出的 Demo，**复现失效场景是重中之重**
4. 梳理：原理、优点、局限、适用边界、场景
5. 场景模拟面试题：
   - 场景 1：service 内部方法调用，@Transactional 不生效，排查原因和修复方案
   - 场景 2：两个事务嵌套，REQUIRED / REQUIRES\_NEW / NESTED 分别会发生什么
   - 场景 3：循环依赖什么情况会报错，如何解决

## 两个选择，继续推进

A：先从 **IOC + Bean 生命周期** 开始，梳理知识点 + 配套 demo 代码

&#x20;B：直接先啃 **Spring 事务**（面试问的最多，场景题多）
