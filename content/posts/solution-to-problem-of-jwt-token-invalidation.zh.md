---
date: "2019-03-26T18:52:00+00:00"
title: "JWT 避坑指南：nbf 验签失效问题的解决"
categories:
  - Tech
---

### 现象

刚签发的 JWT，在下一个请求使用时候会失效，请求会报 422 错误。

```json
{
  "msg": "The token is not yet valid (nbf)"
}
```

如果隔几秒再请求（例如使用 Chrome 开发者工具中的 Replay XHR），就会成功。

<!-- more -->

![](/images/20190326_01.png)

### nbf 字段的原理

查看上面的报错信息，会发现有一个 nbf，nbf 是 JWT 协议中的一个字段，是 Not Before 的缩写，表示 JWT Token 在这个时间之前是无效的，一般来讲会设置成签发的时间。这里产生了一个猜想，多服务器环境时候，服务器之间时间如果不一致，一台服务器签发的 token 如果立刻被发往另一台服务器验证，就很容易产生 nbf 字段验证不通过的问题。其实 JWT 协议已经考虑到了这类问题，所以协议中在 nbf 这一节专门提到了可以使用一个 small leeway 来解决这个问题。

> 4.1.5. "nbf" (Not Before) Claim

The "nbf" (not before) claim identifies the time before which the JWT
MUST NOT be accepted for processing. The processing of the "nbf"
claim requires that the current date/time MUST be after or equal to
the not-before date/time listed in the "nbf" claim. Implementers MAY
provide for some small leeway, usually no more than a few minutes, to
account for clock skew. Its value MUST be a number containing a
NumericDate value. Use of this claim is OPTIONAL.

既然文档考虑到了这个问题，我们再来看一下代码是怎么实现的，我们使用的是 flask-jwt-extended 这个库来实现 JWT 的签发和验签，flask-jwt-extended 依赖的是 PyJWT 这个库，所以在 PyJWT 源码中查找一下这个错误。

```python
def _validate_nbf(self, payload, now, leeway):
    try:
        nbf = int(payload['nbf'])
    except ValueError:
        raise DecodeError('Not Before claim (nbf) must be an integer.')

    if nbf > (now + leeway):
        raise ImmatureSignatureError('The token is not yet valid (nbf)')
```

可以看出，这个报错的确是在验证 nbf 字段时候出现的，如果 nbf 的时间晚于当前的时间加上一个 leeway，就会抛出错误，而从 flask_jwt_extended 源码中可以看到，这个 leeway 字段是用户设置的，而我们设置为了 0，也就是说不存在余量时间，这就要求服务器之间的时间同步，才能不出现 nbf 字段验证不通过的问题。

### 验证问题

后端应用跑在多个节点中，使用 ansible 来同时获取多台机器的时间。

```bash
ansible machine_group -m command -a 'date'
```

需要注意的是，ansible 默认的并发数是 5，机器多的情况下需要修改 ansible.cfg 中的 forks，这样能保证获取时间的操作尽可能在同一时间发起。

```config
[defaults]
host_key_checking = False
forks = 10
```

![](/images/20190326_02.png)

可以看到，不同的机器上的时间并没有同步，并且差异比较大，甚至达到了 2 分钟，这样无疑会造成 nbf 字段验签不通过。

### 解决问题：配置 Linux 自动时间同步

因为多个服务器节点之间时间差太大，所以首先解决服务器之间时间不同步的问题，以 Ubuntu 为例，步骤如下：

安装 Chrony。

```bash
sudo apt install chrony
```

安装后 chrony 就会和默认 ntp 服务器进行同步，各个云环境都有自己的 ntp 服务器，在 `/etc/chrony/chrony.conf` 中可以配置首选 ntp 服务器，例如 aws 环境，需要在所有服务器前增加如下服务器。实测 aws 环境中并不能使用其他的 ntp 服务器（包括国家授时中心、阿里云 ntp 服务器）。

```conf
server 169.254.169.123 prefer iburst
```

重启 chrony 服务。

```bash
sudo systemctl restart chrony
```

查看是否生效。

```bash
sudo chronyc tracking
```

如果状态中有如下语句表示正常

```bash
Leap status : Normal
```

将所有节点同步过时间后，再次测试，发现问题消失。

> 上面过程是所有服务器节点都与时间服务器的时间进行同步，如果在网络隔离的环境中，可以选择一台节点作为授时服务器，其他节点与这台服务器进行时间同步。

### 更进一步：增加 leeway

虽然同步时间过后问题已经消失，但是服务器之间仍然可能会产生微小的时间差，可以通过增加 leeway 来覆盖这种偶发的场景，但是 leeway 也不能无限加长，时间太长会造成安全性下降。

### 参考资料

[RFC7519](https://tools.ietf.org/html/rfc7519)
[flask-jwt-extended](https://github.com/vimalloc/flask-jwt-extended)
[PyJWT](https://github.com/jpadilla/pyjwt)
[为 Linux 实例设置时间](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html)
