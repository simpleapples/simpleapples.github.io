---
date: "2019-03-26T18:52:00+00:00"
title: "JWT Pitfalls Guide: Solving the nbf Verification Failure Issue"
categories:
  - Tech
---

### Phenomenon

A freshly issued JWT becomes invalid when used in the next request, resulting in a 422 error.

```json
{
  "msg": "The token is not yet valid (nbf)"
}
```

If you wait a few seconds before making the request again (for example, using Chrome Developer Tools' Replay XHR), it succeeds.

<!-- more -->

![](/images/20190326_01.png)

### Principle of the nbf Field

Looking at the error message above, you will notice an `nbf`, which is a field in the JWT protocol. It stands for Not Before, indicating that the JWT Token is invalid before this time, and is generally set to the issuance time. This raises a hypothesis: in a multi-server environment, if the servers' times are not synchronized, a token issued by one server might fail verification on another server due to the nbf field. The JWT protocol has already considered such issues, and it specifically mentions using a small leeway to address this in the nbf section.

> 4.1.5. "nbf" (Not Before) Claim

The "nbf" (not before) claim identifies the time before which the JWT
MUST NOT be accepted for processing. The processing of the "nbf"
claim requires that the current date/time MUST be after or equal to
the not-before date/time listed in the "nbf" claim. Implementers MAY
provide for some small leeway, usually no more than a few minutes, to
account for clock skew. Its value MUST be a number containing a
NumericDate value. Use of this claim is OPTIONAL.

Since the documentation has considered this issue, let's look at how the code is implemented. We use the flask-jwt-extended library to issue and verify JWTs, which relies on the PyJWT library. Let's check the PyJWT source code for this error.

```python
def _validate_nbf(self, payload, now, leeway):
    try:
        nbf = int(payload['nbf'])
    except ValueError:
        raise DecodeError('Not Before claim (nbf) must be an integer.')

    if nbf > (now + leeway):
        raise ImmatureSignatureError('The token is not yet valid (nbf)')
```

It is evident that this error occurs during the validation of the nbf field. If the nbf time is later than the current time plus a leeway, an error is thrown. From the flask_jwt_extended source code, we can see that this leeway is user-configurable, and we set it to 0, meaning there is no leeway time. This requires time synchronization between servers to avoid nbf field verification failures.

### Verifying the Issue

The backend application runs on multiple nodes, using Ansible to simultaneously fetch the time from multiple machines.

```bash
ansible machine_group -m command -a 'date'
```

Note that Ansible's default concurrency is 5, so if there are many machines, you need to modify the forks in ansible.cfg to ensure the time-fetching operation is initiated as simultaneously as possible.

```config
[defaults]
host_key_checking = False
forks = 10
```

![](/images/20190326_02.png)

As seen, the times on different machines are not synchronized, with significant differences, even up to 2 minutes, which undoubtedly causes nbf field verification failures.

### Solving the Issue: Configuring Linux for Automatic Time Synchronization

Due to the large time differences between server nodes, the first step is to resolve the time desynchronization issue. Taking Ubuntu as an example, the steps are as follows:

Install Chrony.

```bash
sudo apt install chrony
```

Once installed, Chrony will synchronize with the default NTP server. Each cloud environment has its own NTP server, which can be configured as the preferred NTP server in `/etc/chrony/chrony.conf`. For example, in an AWS environment, add the following server to all servers. In practice, other NTP servers (including the National Time Service Center, Alibaba Cloud NTP server) cannot be used in the AWS environment.

```conf
server 169.254.169.123 prefer iburst
```

Restart the Chrony service.

```bash
sudo systemctl restart chrony
```

Check if it is effective.

```bash
sudo chronyc tracking
```

If the status includes the following statement, it is normal:

```bash
Leap status : Normal
```

After synchronizing the time across all nodes, testing again shows the issue has disappeared.

> The above process synchronizes all server nodes with the time server. In a network-isolated environment, you can choose one node as the time server, with other nodes synchronizing time with this server.

### Further Steps: Increasing Leeway

Although the issue has disappeared after time synchronization, there might still be minor time differences between servers. Increasing the leeway can cover such occasional scenarios, but it should not be extended indefinitely, as too long a leeway can reduce security.

### References

[RFC7519](https://tools.ietf.org/html/rfc7519)  
[flask-jwt-extended](https://github.com/vimalloc/flask-jwt-extended)  
[PyJWT](https://github.com/jpadilla/pyjwt)  
[Setting Time for Linux Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html)