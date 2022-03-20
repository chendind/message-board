### 项目介绍 / Project Introduce
使用Python+数据库，做一个简单的“树形留言”网站。留言可以回复，且无限层级。
Use Python+ database to make a simple "tree message" website.Messages can be replied, and unlimited levels.

### 项目使用技术栈 / Tech Stacks
- Python Flask
- Sqlalchemy
- unittest
- Mysql
- Vue
- Vuex
- Docker Compose

### 运行 / How to run

#### 一、环境要求 / Environment Required
- docker
- docker-compose
- Node v14+
- 端口8090可用 / localhost port 8090 is available

#### 二、安装步骤 / The command to run
##### 如果您的电脑是arm架构 / If your computer is arm architecture
`docker-compose -f docker-compose.arm64.yml up -d && cd ./views/mbweb && npm i && npm run serve`
##### 如果您的电脑是x86架构 / If your computer is x86 architecture
`docker-compose -f docker-compose.yml up -d && cd ./views/mbweb && npm i && npm run serve`
##### 注意：启动需要稍微花点时间，网页打开后可能需要等待一小段时间后方可使用 / Note: It takes a little time to start, and it may take a short time after the webpage is opened before it can be used

#### 三、其他 / Others
##### 运行单元测试 / Run unit tests
- `docker exec -i mb_flaskapp bash -c "flask test"`
##### 移除程序 / Stop and Remove
- `docker-compose down --volumes --remove-orphans`
