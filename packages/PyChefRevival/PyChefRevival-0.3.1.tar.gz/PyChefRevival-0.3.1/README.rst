PyChefRevival
=============

A revival of https://github.com/coderanger/pychef

A Python API for interacting with a Chef server.

Example
-------

::

    from chef import autoconfigure, Node
    
    api = autoconfigure()
    n = Node('web1')
    print n['fqdn']
    n['myapp']['version'] = '1.0'
    n.save()

Further Reading
---------------

Current Documentation:
For more information check out http://pychef.readthedocs.org/en/latest/index.html
