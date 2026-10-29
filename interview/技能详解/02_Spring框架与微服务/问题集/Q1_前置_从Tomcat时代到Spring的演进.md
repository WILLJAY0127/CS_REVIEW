# Q1 前置：从 Tomcat 时代到 Spring 的演进

> 用途：解释"为什么会有 Spring"。理解了这条演进动机链，Q1 里"为什么要拆三步、为什么要有 BeanPostProcessor"才有落脚点。
> 相关：[Q1_Bean生命周期与BeanPostProcessor.md](Q1_Bean生命周期与BeanPostProcessor.md)

---

## 零、一句话

> **Tomcat 负责"把请求交给一个 Servlet"，Spring 负责"这一个 Servlet 怎么把请求交给你的方法"，以及"这些方法依赖的对象谁来造"。**
> 两者不是替代关系，是套娃关系——Spring MVC 本身就跑在 Tomcat 里。

---

## 一、先补两块地基

### 1. Servlet 和 Tomcat 的关系

- **Tomcat**：Servlet 容器 + 轻量 Web 服务器。负责网络通信、线程管理、Servlet 生命周期，默认 8080 端口。
- **Servlet**：一套 Java Web 规范（接口）。你写的类继承 `HttpServlet`、重写 `doGet/doPost`，就是一个 Servlet。
- 分工：Tomcat 收请求 → 找到对应 Servlet → 调它 → 拿结果返回浏览器。

### 2. Servlet 实例是谁 new 的、什么时候 new 的

**你不该也不能手动 new Servlet**，实例由 Tomcat 创建：

| 阶段 | 方法 | 次数 | 谁调用 |
|---|---|---|---|
| 1 实例化 | 构造函数 | 1 次 | Tomcat（反射 `new`） |
| 2 初始化 | `init()` | 1 次 | Tomcat |
| 3 服务 | `service()` → `doGet/doPost` | N 次 | Tomcat（多线程并发） |
| 4 销毁 | `destroy()` | 1 次 | Tomcat（关闭/卸载时） |

默认**懒加载**：第一次访问该 URL 时才 `new` + `init`；配 `@WebServlet(value="/x", loadOnStartup=1)` 则启动时创建。

`@WebServlet` 的作用：替代 `web.xml`，Tomcat 启动时扫描注解，维护一张 `URL → Class` 的映射表。

**核心认知：Tomcat 自己就是容器。** "容器管理对象"不是 Spring 发明的，Spring 只是把这个模式从 Web 层扩展到了整个应用。

---

## 二、第 0 版：最裸的 Servlet（Tomcat 时代原貌）

```xml
<!-- web.xml -->
<servlet>
  <servlet-name>register</servlet-name>
  <servlet-class>com.example.RegisterServlet</servlet-class>
</servlet>
<servlet-mapping>
  <servlet-name>register</servlet-name>
  <url-pattern>/register</url-pattern>
</servlet-mapping>
```

```java
public class RegisterServlet extends HttpServlet {
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws IOException, ServletException {
        req.setCharacterEncoding("UTF-8");
        String name = req.getParameter("name");

        Connection conn = null;
        PreparedStatement ps = null;
        try {
            conn = DriverManager.getConnection(URL, USER, PWD);
            conn.setAutoCommit(false);
            ps = conn.prepareStatement("insert into user(name) values(?)");
            ps.setString(1, name);
            ps.executeUpdate();
            conn.commit();
            resp.getWriter().write("ok");
        } catch (Exception e) {
            if (conn != null) try { conn.rollback(); } catch (Exception ignore) {}
            throw new ServletException(e);
        } finally {
            if (ps != null) try { ps.close(); } catch (Exception ignore) {}
            if (conn != null) try { conn.close(); } catch (Exception ignore) {}
        }
    }
}
```

**真相**：真正属于业务的只有 `insert into user` 一行，其余 90% 是基础设施——取参数、管连接、开事务、回滚、关资源、包异常。

再写一个"查询用户"的 Servlet，这 90% 要原样复制一遍。

---

## 三、第 1 版：抽 DAO，把 SQL 挪走

```java
public class UserDao {
    public void insert(String name) throws SQLException {
        try (Connection c = DriverManager.getConnection(URL, USER, PWD);
             PreparedStatement ps = c.prepareStatement("insert into user(name) values(?)")) {
            ps.setString(1, name);
            ps.executeUpdate();
        }
    }
}
```

Servlet 里变成 `new UserDao().insert(name)`。

**新问题**：每个 Servlet 各 `new` 一个 `UserDao`，而 `DriverManager.getConnection` 每次都新建物理连接——没有连接池，性能直接崩。

---

## 四、第 2 版：工厂 + 连接池（你手写了一个迷你容器）

```java
public class DaoFactory {
    private static final DataSource DS = new HikariDataSource();   // 全应用一个池
    private static final UserDao USER_DAO = new UserDao(DS);

    public static UserDao userDao() { return USER_DAO; }
}
```

Servlet 里改成 `DaoFactory.userDao().insert(name)`。

这一步解决了"重复创建"和"创建逻辑散落"，但**依赖顺序仍要人肉维护**：`DS` 必须在 `USER_DAO` 前面；每加一个 Bean，都得想清楚插在哪一行。

---

## 五、第 3 版：重构到头了，撞上五个问题

| 问题 | 为什么重构救不了 |
|---|---|
| 每个 Servlet 都重复写参数解析、乱码设置、异常包装 | 这是"所有 Servlet 都一样"的代码，但你只能复制 |
| 事务模板在每个业务方法里 | 业务方法没法自己"长出"事务能力 |
| 想换 `UserDao` 实现，得改工厂代码 | 工厂是硬编码的，换实现就是改代码 |
| 配置散落在 `DriverManager` 调用里 | 没有统一配置入口 |
| 没法单测 | 依赖 Servlet API 和真实数据库 |

**关键洞察**：这五条的共同点是——**它们不是"这个项目的问题"，是"所有 Web 项目的问题"**。

凡是"所有项目都一样"的重复劳动，迟早会被抽成框架。Spring 的出现是必然，不需要谁去"发明"，只需要有人先做出来。

---

## 六、第 4 版：Spring 把这五笔债一个个接走

| Tomcat 时代的痛点 | Spring 的解法 |
|---|---|
| 手工 `new` 整条依赖链 | IoC / DI |
| 工厂硬编码、换实现要改代码 | 容器扫描 + 注入（换实现只改注解） |
| 每个方法写事务模板 | AOP + `@Transactional` |
| 每个功能写一个 Servlet、重复解析参数 | Spring MVC 的 `DispatcherServlet` 统一分发 |
| 配置散落 | 统一配置 + `@Value` |
| 无法单测 | 纯 POJO + 构造器注入 |

---

## 七、关键连接点：`DispatcherServlet` 本身就是一个 Servlet

很多人以为 Spring MVC 取代了 Servlet，其实不是：

- Tomcat 仍然是 Servlet 容器，负责网络、线程、生命周期。
- Spring MVC 只是在 `web.xml` 里注册了**一个** Servlet —— `DispatcherServlet`。
- 之后所有请求都进这一个 Servlet，它再按 URL 分发给你的 `@Controller` 方法。

```xml
<servlet>
  <servlet-name>dispatcher</servlet-name>
  <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
</servlet>
<servlet-mapping>
  <servlet-name>dispatcher</servlet-name>
  <url-pattern>/</url-pattern>       <!-- 接管所有路径 -->
</servlet-mapping>
```

演变本质：

```
Tomcat 时代：N 个 URL → N 个 Servlet（每个都重复那 90%）
Spring 时代：N 个 URL → 1 个 DispatcherServlet → N 个 Controller 方法
```

**"从 N 个 Servlet 变成 1 个 Servlet"**，这才是 Spring MVC 真正的贡献。`@Controller` 不需要继承 `HttpServlet`，也不需要 `web.xml`。

补充：传统 SSM 里 `DispatcherServlet` 会创建**子容器**（`WebApplicationContext`），`Controller` 在子容器、`Service/Dao` 通常在父容器（RootContext），子能取父、父取不到子。Spring Boot 只有一个容器。

---

## 八、时间线（只讲 Tomcat 这条线）

| 时间 | 发生了什么 |
|---|---|
| 1999 | Tomcat 3.x 发布，Servlet/JSP 成为主流 |
| 2000–2005 | Servlet + JSP + JDBC + DAO 模式，Web 层普遍用 Struts |
| 2003 | Servlet 2.4；2004 年 Spring 1.0 发布（先解决"对象管理"） |
| 2006 | Spring 2.0 引入 Spring MVC，开始替代 Struts |
| 2007 | Spring 2.5 支持注解（`@Controller` / `@Autowired`），配置量骤降 |
| 2009 | Servlet 3.0 引入 `@WebServlet`，`web.xml` 开始退场 |
| 2014 | Spring Boot 1.0，连 XML 都省了 |

---

## 九、因果链（6 行）

```
Servlet 里什么都自己 new
  → 重复创建、连接池浪费        → 抽工厂/单例
工厂越写越大、依赖顺序人肉维护
  → 需要通用容器                → IoC
事务/日志模板在每个方法里复制
  → 需要不改业务代码就能加逻辑   → AOP
每个功能一个 Servlet、参数解析重复
  → 需要统一入口                → DispatcherServlet + Spring MVC
XML 配置爆炸
  → 需要约定优于配置            → Spring Boot
```

---

## 十、三个高频疑问

### 1. DAO 能不能当 Servlet 的成员变量？

能，而且是标准写法。因为 Servlet 是单例、多线程共享，判断标准只有一条：**这个对象有没有可变状态**。

- DAO 通常**无状态**（只有方法，参数靠入参传）→ 可以当成员变量，安全。
- `int count`、`String currentUser` 这类**请求数据** → 绝对不能当成员变量，会串数据。

### 2. 为什么"单例模式"听得多、写得少？

因为**单例的创建权被容器接管了**。`@Service` 就是一句"请给我一个单例"，Tomcat 管 Servlet 也是同一个道理。书上的 `getInstance()` + 私有构造 + 双重检查，是**没有容器时代**的产物，现在手写单例在 Spring 项目里是坏味道（隐藏依赖、难测试、绕开代理）。

必须手写单例的场景只剩三类：纯 Java SE / 工具库、JVM 级全局资源、框架自身基础设施。最推荐的写法是**枚举单例**（天然防反射、防序列化破坏）。

### 3. 不用 Spring Boot，只用 Spring MVC 行不行？

行。Spring MVC 是 Spring Framework 的模块，Bean 管理机制完全一样，只是"谁触发注册"不同：Boot 靠自动配置 + 扫描，传统 SSM 靠 `web.xml` + `component-scan` 或 `<bean>`。

但**只把 Spring MVC 当普通类库、不启动容器**，则不行——`@Controller`、`@Autowired` 全部失效，注解本身没有魔力，是容器启动时解析它们才生效的。

---

## 十一、收口

> Spring 做的所有事，本质都是把"**每个项目都要重写一遍的基础设施**"收进框架，把"**每个项目都不同的业务逻辑**"还给开发者。
>
> 判断一个对象归不归容器管，别看它被谁注入了，看**它是怎么进注册表的**。
