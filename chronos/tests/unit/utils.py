from chronos.openstack.common import wsgi

TASK_UUID1 = 'c80a1a6c-bd1f-41c5-90ee-81afedb1d58d'
TASK_UUID2 = '971ec09a-8067-4bc8-a91f-ae3557f1c4c7'

SERVER_UUID1 = 'ba3f1c5d-89a0-34c1-b44d-ef78d46b90a3'

TENANT1 = '6838eb7b-6ded-434a-882c-b344c77fe8df'
TENANT2 = '2c014f32-55eb-467d-8fcb-4bd706012f81'

USER1 = '54492ba0-f4df-4e4e-be62-27f4d76b29cf'
USER2 = '0b3b3006-cb76-4517-ae32-51397e22c754'
USER3 = '2hss8dkl-d8jh-88yd-uhs9-879sdjsd8skd'


def get_fake_request(path='', method='GET'):
    req = wsgi.Request.blank(path)
    req.method = method

    return req


def get_task(id=None, serverRef=SERVER_UUID1):
    task = {
        'task':
        {
            'id': id,
            'serverRef': serverRef
        }
    }
    return task