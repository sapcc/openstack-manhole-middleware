# openstack-manhole-middleware
OpenStack middleware enables manhole python socket for every wsgi process. This re-creates the backdoor_socket behaviour of oslo.service when used for example with external web server like uWSGI or Apache.

### Configuration Options
* [DEFAULT] backdoor_socket = <path_to_socket>

path_to_socket can be a format string, where `pid` is being interpolated, e.g.
```ini
[DEFAULT]
backdoor_socket=/tmp/backdoor-{pid}.socket
```

### Usage
`pip install openstack-manhole-middleware` and add as a middleware to you paste config.


#### api-paste.ini
```ini
...
keystone = cors ... manhole neutronapiapp_v2_0

[filter:manhole]
paste.filter_factory = manhole_middleware:Manhole.factory
```
