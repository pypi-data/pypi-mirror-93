`rst file editor <http://rst.ninjs.org>`_

mwsdk


maxwin 团队常用的服务，包括 kong，rightmanage等,直接从 consul 中读取服务信息

Kong 的使用

.. code-block:: python

    from mwsdk import Kong
    # 创建kong 服务
    k = Kong()
    # 向kong注册服务,需jwt认证
    k.reg_service('monitor-srv/api/v1.0','192.168.101.88:8999',auth='jwt',kong_uris='monitor-srv/api')
    # 向kong注册upstream和tagert，增加负载平衡
    k.add_upstream_target('monitor-srv','192.168.101.88:8999',50)
    k.add_upstream_target('monitor-srv','192.168.101.99:8888',50)
    # 把upstream 注册到kong，不需要认证
    k.reg_service('monitor-srv/api/doc','monitor-srv',auth='',kong_uris='monitor-srv/doc')


Rightmanage的使用


.. code-block:: python

    from mwsdk import Rightmanage_inner
    # Rightmanage为内网的 权限服务，不需要认证
    rm = Rightmanage_inner()
    # 获取权限资料
    status_code,rm_json = rm.permissions('maxwin_web','admin.id')

AIORightmanage_inner 的使用

- 支持async，方法同 Rightmanage

安装方法

``pip install mwsdk``


