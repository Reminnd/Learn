# 企业服务化

**Track:** Advanced Track

## 与已提前学习的FastAPI基础的分工

FastAPI最小路由/Pydantic/基础依赖注入/pytest已作为[Stage01/04→05桥接单元](../stage-01/fastapi-backend-bridge.md)提前学习；数据库CRUD与事务入门可在Stage02后结合LangGraph渐进实践，基础JWT、SSE、Redis与Docker可随Stage07–09按真实需求引入。

**Stage13保持Advanced Track章节顺序与验收**：本阶段不重复“创建第一个GET接口”，而重点深入**并发请求、连接池、缓存一致性、多租户隔离、分布式Worker/Queue、幂等与可靠性、Docker/Kubernetes部署策略**。提前接触API或Docker不构成Stage13章节掌握证据，也不绕过Core完成才进入Advanced的规则。

## 本阶段章节

- [`01-fastapi-storage.md`](01-fastapi-storage.md) — FastAPI、PostgreSQL、Redis 与存储边界
- [`02-distributed-runtime.md`](02-distributed-runtime.md) — Distributed Runtime：Worker、Queue、幂等
- [`03-docker-kubernetes.md`](03-docker-kubernetes.md) — Docker 与 Kubernetes

## 阶段完成标准

本阶段所有章节 Q&A 达到 `mastered` 后，本阶段完成。

[返回课程索引](../index.md)
