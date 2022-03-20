### Project Introduce
Use Python+ database to make a simple "tree message" website.Messages can be replied, and unlimited levels.

### Tech Stacks
- Python Flask
- Sqlalchemy
- unittest
- Mysql
- Vue
- Vuex
- Docker Compose

### How to run

#### Environment Required
- docker
- docker-compose
- Node v14+
- localhost port 8090 is available

#### The command to run
##### If your computer is arm architecture
`docker-compose -f docker-compose.arm64.yml up -d && cd ./views/mbweb && npm i && npm run serve`
##### If your computer is x86 architecture
`docker-compose -f docker-compose.yml up -d && cd ./views/mbweb && npm i && npm run serve`
##### Note: It takes a little time to start, and it may take a short time after the webpage is opened before it can be used

#### Others
##### Run unit tests
- `docker exec -i mb_flaskapp bash -c "flask test"`
##### Stop and Remove
- `docker-compose down --volumes --remove-orphans`
