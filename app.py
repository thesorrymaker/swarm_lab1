from flask import Flask, render_template
import redis
import os

app = Flask(__name__)

# 从环境变量获取Redis连接信息
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

# 创建Redis连接
redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    db=0,
    socket_connect_timeout=2,
    socket_timeout=2
)


@app.route('/')
def index():
    try:
        # 增加计数器
        count = redis_client.incr('page_visits')

        # 获取当前主机名（用于展示哪个容器在服务）
        hostname = os.environ.get('HOSTNAME', 'localhost')

        return render_template(
            'index.html',
            count=count,
            hostname=hostname,
            status='connected'
        )
    except redis.ConnectionError:
        # Redis连接失败时
        return render_template(
            'index.html',
            count='N/A',
            hostname=os.environ.get('HOSTNAME', 'localhost'),
            status='disconnected',
            error='Cannot connect to Redis'
        )


if __name__ == '__main__':
    # 获取端口，默认为5000
    port = int(os.environ.get('PORT', 5000))
    # 监听所有网络接口（重要！）
    app.run(host='0.0.0.0', port=port, debug=True)
