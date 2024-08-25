# CloudFlare 笔记

## CloudFlare Argo Tunnel 内网穿透

github下载：https://github.com/cloudflare/cloudflared/releases

官方文档：https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/

macOS 安装

```bash
brew install cloudflared
```

其他系统下载方式：https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/

### 登录

```bash
cloudflared tunnel login
```

### 创建隧道

```bash
cloudflared tunnel create 隧道名
```

### 删除隧道

```SH
cloudflared tunnel delete 隧道名
```

### 列出隧道

```bash
cloudflared tunnel list
```

### 配置隧道

将域名绑定到隧道，cloudflare 会自动创建 CNAME 记录将域名指向隧道

```bash
cloudflared tunnel route dns 隧道名 域名
```

示例

```bash
cloudflared tunnel route dns tool file.yym68686.top
```

创建文件 ~/.cloudflared/config.yml

```yaml
tunnel: f75cbf56-cd65-45ed-80c5-2f055bb5c9f6
credentials-file: /Users/yanyuming/.cloudflared/f75cbf56-cd65-45ed-80c5-2f055bb5c9f6.json
protocol: http2
originRequest:
  connectTimeout: 30s
  noTLSVerify: false

ingress:
  - hostname: file.yym68686.top
    service: http://localhost:8080
  - service: http_status:404
```

### 运行隧道

运行隧道下所有服务，需要读取配置文件

```bash
cloudflared --config <config-File> tunnel run <Tunnel-NAME>
```

示例

```bash
cloudflared --config ～/.cloudflared/config.yml tunnel run tool
```

运行隧道下单个服务，不需要配置文件。

- 使用自己的域名

```bash
cloudflared tunnel run --url localhost:port 隧道名字
```

- 使用 cloudflare 的域名

```bash
cloudflared tunnel --url http://127.0.0.1:8080
```

启动文件目录共享

```bash
python -m http.server 8080
```

### 体验隧道

由官方提供测试域名，不需要自己有域名，也不需要配置文件

```bash
cloudflared tunnel --url localhost:port
```

### Docker 镜像

下载

```bash
docker pull cloudflare/cloudflared
```

