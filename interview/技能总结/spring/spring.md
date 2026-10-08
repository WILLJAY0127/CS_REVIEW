# Spring 使用层面需要掌握的内容（**使用者视角，不是源码开发者**，也就是你写业务代码时要会的，不涉及三级缓存、doCreateBean 这些内部实现）

> 定位：对应前面分层里的「Spring 应用层」，只讲**怎么用、有什么行为、踩什么坑**，不钻底层实现。

## 一、IOC 容器（核心）

### 1. Bean 的定义方式

1. 注解方式（日常主力）

- `@Component / @Service / @Repository / @Controller`：标记类为 Bean
- `@Bean`：在配置类`@Configuration`里手动定义 Bean（第三方类、复杂对象）
- `@Configuration`：配置类，用来装配 Bean

1. Bean 扫描规则

- `@ComponentScan`：包扫描，SpringBoot 默认自动扫描当前包及子包

> 理解：Spring 会扫描这些类，把它们交给容器管理。

### 2. 依赖注入 DI（三种注入方式）

1. 构造器注入（**推荐**，Spring 官方推荐，强制依赖、不可空）
2. Setter 注入（可选依赖）
3. 字段注入`@Autowired`（简单，但有缺点，单元测试麻烦）

重点：

- `@Autowired`：按类型装配；`@Qualifier`按名字区分同类型多个 Bean
- `@Value`：注入普通字符串、配置文件的值
- `@Resource`：JSR 规范，默认按名称，备选按类型

### 3. Bean 作用域 `@Scope`

- singleton（默认，单例：容器里只创建 1 个 Bean，**最常考**）
- prototype（多例：每次获取新建对象）
- request /session（web 场景）

> 坑：**单例 Bean 里如果放非线程安全成员变量，会并发问题**

### 4. Bean 生命周期（使用者需要记住的**行为契约**，不用背 doCreateBean）

1. 实例化对象（new）
2. 填充属性（@Autowired 注入）
3. 初始化回调：`@PostConstruct` → InitializingBean → xml init-method
4. 正常使用
5. 销毁回调：`@PreDestroy` / DisposableBean

> 使用者只需要知道：**@PostConstruct 在依赖注入完成之后执行**，适合初始化资源。

### 5. 条件、导入、导入资源

- `@Conditional` 系列：满足条件才创建 Bean（SpringBoot 大量使用）

## 二、AOP 面向切面（使用者层面）

1. 核心概念：切面、连接点、切点、通知

   &#x20;通知类型：

- @Before 前置
- @AfterReturning 正常返回后
- @AfterThrowing 异常时
- @After 最终通知
- @Around 环绕（最强，可以控制目标方法执行）

1. 使用场景：日志、埋点、权限校验、事务底层
2. **高频大坑（必须掌握）**

> 同类内方法调用，AOP 不生效！原因：AOP 依靠代理对象，this 调用不走代理。

## 三、声明式事务 Spring TX（`@Transactional`，业务最常用）

1. 生效前提：**必须是代理对象调用**（和 AOP 同一个坑）
2. 核心属性（使用者必须懂）

- propagation 传播行为（REQUIRED、REQUIRES\_NEW、SUPPORTS… 最核心）
- isolation 隔离级别
- rollbackFor：**默认只在 RuntimeException/Error 回滚，受检异常默认不回滚**（超级高频踩坑）
- readOnly、timeout

1. 常见坑：

- 方法 private，事务无效
- try-catch 捕获异常不抛出，事务不回滚

## 四、事件机制（ApplicationEvent）

简单发布订阅，解耦，业务解耦场景用。知道基本用法即可。

## 五、SpringBoot 相关（Spring 之上封装，日常开发必用）

1. `@SpringBootApplication` 复合注解
2. application.yml/properties 配置读取
3. starter 自动装配思想
4. `@ConfigurationProperties` 批量读取配置

## 六、Spring 常用扩展接口（使用者级别，简单了解）

> 区分：BeanPostProcessor 是**内部实现层**，业务代码一般不写；
>
> &#x20;业务开发常用扩展：

- ApplicationRunner / CommandLineRunner：容器启动完成后执行代码
- InitializingBean、DisposableBean：bean 初始化销毁回调

# ✅ 使用者需要掌握的【避坑清单】（面试高频，业务天天遇到）

1. @Transactional 什么时候失效（4 个核心场景）
2. AOP 什么时候失效（同类内调用、private 方法）
3. Bean 单例，成员变量非线程安全
4. @PostConstruct 执行时机（注入完成之后）
5. 循环依赖契约：单例 setter 注入支持循环依赖；构造注入不支持
6. @Autowired 多个同类型 Bean 怎么处理

# ❌ 使用阶段不需要学（底层实现，业务开发不用）

doCreateBean、三级缓存、BeanFactory 底层、代理生成源码细节。这些是**Core 内部实现层**，只有深挖面试才看。

# 极简一句话总结

使用 Spring，你要掌握：**怎么定义 Bean、怎么注入依赖、Bean 生命周期行为、AOP 切面写法、@Transactional 事务规则与失效场景，外加 SpringBoot 自动装配与配置读取；重点记住各种注解生效的前提和坑。**

你想，我把这部分整理成精简的面试口述要点吗？
