# AI 辅助开发前后端项目工作流

> 后端 Spring Boot + 前端 React 在 AI 环境下的协作方案

---

## 一、核心思路

**前后端解耦 + API 契约先行 + AI 提示词模板化**

| 原则 | 说明 |
|------|------|
| API 契约先行 | 先定义接口文档，再开发代码 |
| AI 提示词模板化 | 统一 AI 的输出格式，保证代码风格一致 |
| 前后端独立修改 | 每次只修改一个模块，避免冲突 |
| 版本号管理 | 明确记录 API 变更，便于追踪 |
| 自动化部署 | Docker + CI/CD，减少人工操作 |

---

## 二、项目结构规范

```
project-root/
├── backend/                          # Spring Boot 后端
│   ├── src/main/java/
│   │   └── com/example/app/
│   │       ├── controller/           # API 控制器
│   │       ├── service/              # 业务逻辑
│   │       └── repository/           # 数据访问
│   └── pom.xml
│
├── frontend/                         # React 前端
│   ├── src/
│   │   ├── components/               # UI 组件
│   │   ├── api/                      # API 调用封装
│   │   └── pages/                    # 页面
│   └── package.json
│
├── docs/                             # 文档
│   ├── api-contract.md               # API 契约文档（重要！）
│   └──-prompts/                      # AI 提示词模板
│       ├── backend-prompt.md
│       └── frontend-prompt.md
│
└── docker-compose.yml                # 一键部署配置
```

---

## 三、建立 API 契约（核心！）

**这是保证前后端不冲突的关键！**

创建 `docs/api-contract.md`：

```markdown
# API 契约

## 用户模块

### 1. 获取用户列表
- **Method**: GET
- **Endpoint**: `/api/users`
- **Response**:
```json
[
  {
    "id": Long,
    "name": String,
    "email": String,
    "createdAt": DateTime
  }
]
```

### 2. 创建用户
- **Method**: POST
- **Endpoint**: `/api/users`
- **Request Body**:
```json
{
  "name": String,      // 必填
  "email": String      // 必填，邮箱格式
}
```
- **Response**:
```json
{
  "id": Long,
  "name": String,
  "email": String,
  "createdAt": DateTime
}
```

## 接口版本管理
- 当前版本: v1
- 破坏性变更: 新增版本号 (如 `/api/v2/users`)
```

### 版本号规则

```
版本号格式：MAJOR.MINOR.PATCH

- MAJOR: 破坏性变更（如删除接口、修改数据结构）
- MINOR: 新增功能（如新增接口）
- PATCH: 修复 bug

示例：
- 1.0.0 → 初始版本
- 1.1.0 → 新增用户列表分页
- 1.1.1 → 修复用户创建的 bug
- 2.0.0 → 修改用户数据结构（破坏性变更）
```

---

## 四、AI 提示词模板

### 后端开发提示词

创建 `docs/ai-prompts/backend-prompt.md`：

```markdown
# 后端开发提示词模板

你是一个 Spring Boot 专家。请根据以下 API 契约开发后端代码。

## 要求
1. 严格遵循 API 契约文档中的接口定义
2. 使用 RESTful 风格
3. 添加适当的异常处理
4. 代码注释使用中文
5. 遵循项目现有代码风格

## 技术栈
- Java 17
- Spring Boot 3.2
- Spring Data JPA
- MySQL 8.0

## 代码模板

### Controller 层
```java
@RestController
@RequestMapping("/api/{module}")
public class {Module}Controller {
    
    @GetMapping
    public ResponseEntity<?> list() {
        // 实现逻辑
    }
    
    @PostMapping
    public ResponseEntity<?> create(@RequestBody {DTO} dto) {
        // 实现逻辑
    }
}
```

### Service 层
```java
@Service
public class {Module}Service {
    
    public {Entity} save({DTO} dto) {
        // 业务逻辑
    }
}
```

### DTO 层（数据传输对象）
```java
public record {Module}DTO(
    String name,
    String email
) {}
```
```

### 前端开发提示词

创建 `docs/ai-prompts/frontend-prompt.md`：

```markdown
# 前端开发提示词模板

你是一个 React + TypeScript 专家。请根据以下 API 契约开发前端代码。

## 要求
1. 严格遵循 API 契约文档中的接口定义
2. 使用 TypeScript 定义类型
3. 使用 fetch/axios 调用 API
4. 添加适当的错误处理和加载状态
5. 组件化开发，遵循 React Hooks 规范

## 技术栈
- React 18
- TypeScript 5
- Ant Design 5
- Axios

## 代码模板

### API 调用封装
```typescript
// src/api/{module}.ts
import axios from 'axios';

const API_BASE = '/api';

export interface {Entity} {
  id: number;
  name: string;
  email: string;
  createdAt: string;
}

export async function fetch{Entities}(): Promise<{Entity}[]> {
  const response = await axios.get(`${API_BASE}/{module}`);
  return response.data;
}

export async function create{Entity}(data: Omit<{Entity}, 'id' | 'createdAt'>): Promise<{Entity}> {
  const response = await axios.post(`${API_BASE}/{module}`, data);
  return response.data;
}
```

### 组件模板
```typescript
// src/components/{Module}List.tsx
import { useEffect, useState } from 'react';
import { fetch{Entities}, {Entity} } from '../api/{module}';

export function {Module}List() {
  const [items, setItems] = useState<{Entity}[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const data = await fetch{Entities}();
        setItems(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : '加载失败');
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <div>加载中...</div>;
  if (error) return <div>错误: {error}</div>;

  return (
    <div>
      {/* 渲染列表 */}
    </div>
  );
}
```
```

---

## 五、AI 辅助开发工作流

### 场景 1：新增 API

**给 AI 的指令**：

```
请根据 docs/api-contract.md 中的定义，开发用户模块的新增接口：

接口定义：
- POST /api/users
- Request: { "name": String, "email": String }
- Response: { "id": Long, "name": String, "email": String, "createdAt": DateTime }

要求：
1. 在 backend/src/main/java/com/example/app/controller/ 创建 UserController.java
2. 在 backend/src/main/java/com/example/app/service/ 创建 UserService.java
3. 在 frontend/src/api/ 创建 user.ts
4. 使用 docs/ai-prompts/ 中的代码模板
5. 代码注释使用中文
```

### 场景 2：修改 API（添加分页）

**给 AI 的指令**：

```
请修改用户模块的获取列表接口，添加分页支持。

原接口：GET /api/users
新接口：GET /api/users?page=1&size=10

Response 变为：
{
  "content": [...],
  "totalElements": Long,
  "totalPages": Int,
  "number": Int,
  "size": Int
}

要求：
1. 同步修改 API 契约文档
2. 后端添加分页参数和返回结构
3. 前端添加分页参数和类型定义
4. 确保前后端一致
5. 这是 MINOR 变更，版本号升级为 1.1.0
```

### 场景 3：联调检查

**给 AI 的指令**：

```
请检查前后端代码是否一致：

后端定义的 API：
- GET /api/users → 返回 [{id: Long, name: String}]

前端调用的 API：
- src/api/user.ts 中的 fetchUsers()

请检查：
1. URL 是否一致
2. 请求方法是否一致
3. 数据结构是否一致
4. TypeScript 类型是否正确
5. 如果发现不一致，请给出修复建议
```

### 场景 4：破坏性变更

**给 AI 的指令**：

```
用户模块需要进行破坏性变更：

原 Response：{ "id": Long, "name": String, "email": String }
新 Response：{ "userId": String, "fullName": String, "emailAddress": String }

要求：
1. 创建新版本 API：/api/v2/users
2. 保持旧版本 API：/api/v1/users 不变
3. 前端添加对新旧版本的支持
4. 更新 API 契约文档，标记为 MAJOR 变更
5. 版本号升级为 2.0.0
6. 添加迁移指南
```

---

## 六、部署保障

### Docker Compose 一键部署

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - DB_HOST=db
      - DB_USERNAME=root
      - DB_PASSWORD=root
      - DB_NAME=myapp
    depends_on:
      - db
    networks:
      - app-network

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - app-network

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: myapp
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - app-network

volumes:
  mysql-data:

networks:
  app-network:
    driver: bridge
```

### GitHub Actions CI/CD

创建 `.github/workflows/deploy.yml`：

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # 构建后端
      - name: Build Backend
        run: |
          cd backend
          mvn clean package -DskipTests
          
      # 构建前端
      - name: Build Frontend
        run: |
          cd frontend
          npm ci
          npm run build
      
      # 部署
      - name: Deploy with Docker
        run: |
          docker-compose down
          docker-compose up -d --build
      
      # 健康检查
      - name: Health Check
        run: |
          sleep 10
          curl -f http://localhost:8080/api/health || exit 1
          echo "Backend is running!"
```

### 环境配置

创建 `.env.example`：

```bash
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=root
DB_NAME=myapp

# 后端配置
BACKEND_PORT=8080
SPRING_PROFILES_ACTIVE=dev

# 前端配置
FRONTEND_PORT=3000
API_BASE_URL=http://localhost:8080/api
```

---

## 七、最佳实践总结

| 实践 | 说明 | 示例 |
|------|------|------|
| **API 契约先行** | 先定义接口文档，再开发代码 | 先写 `api-contract.md` |
| **AI 提示词模板化** | 统一的提示词，保证代码风格一致 | 使用 `backend-prompt.md` |
| **前后端独立修改** | 每次只修改一个模块，避免冲突 | 先改后端，再改前端 |
| **版本号管理** | 明确记录 API 变更，便于追踪 | 1.0.0 → 1.1.0 |
| **自动化部署** | Docker + CI/CD，减少人工操作 | `docker-compose up -d` |
| **代码审查** | AI 生成的代码必须人工审核 | 检查 AI 生成的代码 |
| **小步快跑** | 每次只改一个功能，便于排查问题 | 一个 PR 一个功能 |

---

## 八、避免的坑

| 坑 | 原因 | 解决方案 |
|------|------|----------|
| **同时修改前后端** | 容易出错，难以定位问题 | 一个一个来，每次只改一个模块 |
| **忽略 API 契约** | 前后端不一致，联调困难 | API 契约是唯一的真相来源 |
| **忘记更新文档** | 代码改了，文档没改，后续维护困难 | 代码和文档必须同步更新 |
| **盲目信任 AI** | AI 可能生成不一致的代码 | 必须人工审核 AI 生成的代码 |
| **不做版本管理** | 难以追踪变更历史 | 使用语义化版本号 |
| **不考虑兼容性** | 破坏现有接口，影响已有客户端 | 破坏性变更使用新版本 API |

---

## 九、快速上手 Checklist

- [ ] 1. 创建项目目录结构
- [ ] 2. 编写 API 契约文档 (`docs/api-contract.md`)
- [ ] 3. 创建 AI 提示词模板 (`docs/ai-prompts/`)
- [ ] 4. 初始化 Spring Boot 后端项目
- [ ] 5. 初始化 React 前端项目
- [ ] 6. 配置 Docker Compose
- [ ] 7. 配置 CI/CD
- [ ] 8. 使用 AI 辅助开发第一个功能
- [ ] 9. 前后端联调测试
- [ ] 10. 部署到生产环境

---

## 十、示例场景完整流程

### 场景：新增「用户登录」功能

**第 1 步：更新 API 契约**

```markdown
### 3. 用户登录
- **Method**: POST
- **Endpoint**: `/api/users/login`
- **Request Body**:
```json
{
  "email": String,
  "password": String
}
```
- **Response**:
```json
{
  "token": String,
  "expiresIn": Long,
  "user": {
    "id": Long,
    "name": String,
    "email": String
  }
}
```
```

**第 2 步：开发后端**

给 AI 的指令：
```
请根据 docs/api-contract.md 中的登录接口定义，开发后端代码。

要求：
1. 创建 LoginController.java
2. 创建 LoginService.java，实现 JWT 认证
3. 添加适当的异常处理（邮箱或密码错误）
4. 使用 docs/ai-prompts/backend-prompt.md 中的代码模板
```

**第 3 步：开发前端**

给 AI 的指令：
```
请根据 docs/api-contract.md 中的登录接口定义，开发前端代码。

要求：
1. 创建 src/api/auth.ts，封装登录 API
2. 创建 src/components/LoginForm.tsx，登录表单组件
3. 添加登录状态管理（React Context）
4. 使用 docs/ai-prompts/frontend-prompt.md 中的代码模板
```

**第 4 步：联调测试**

给 AI 的指令：
```
请检查登录功能的前后端一致性：

1. 检查前端调用的 URL 是否和后端定义的一致
2. 检查请求体结构是否匹配
3. 检查响应结构是否匹配
4. 检查错误处理是否完善
```

**第 5 步：部署**

```bash
# 本地测试
docker-compose up -d

# 查看日志
docker-compose logs -f

# 测试接口
curl -X POST http://localhost:8080/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "123456"}'
```

---

## 💡 总结

这套工作流的核心是：

1. **API 契约先行** → 保证前后端沟通一致
2. **AI 提示词模板化** → 保证代码风格统一
3. **分模块开发** → 避免冲突，便于排查问题
4. **自动化部署** → 减少人工操作风险
5. **版本管理** → 便于追踪变更历史

掌握这套方法，你就能在 AI 环境下高效开发前后端项目，同时保证部署不受影响！