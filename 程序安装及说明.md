#### 一、环境要求
- docker
- docker-compose
- Node版本号14以上
- 端口8090可用

#### 二、安装步骤
##### 如果您的电脑是arm架构
`docker-compose -f docker-compose.arm64.yml up -d && cd ./views/mbweb && npm i && npm run serve`
##### 如果您的电脑是x86架构
`docker-compose -f docker-compose.yml up -d && cd ./views/mbweb && npm i && npm run serve`
##### 注意：启动需要稍微花点时间，网页打开后可能需要等待一小段时间后方可使用

#### 三、说明
##### 运行单元测试
- `docker exec -i mb_flaskapp bash -c "flask test"`
##### 移除程序
- `docker-compose down --volumes --remove-orphans`
