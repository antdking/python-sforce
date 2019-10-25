
class RefBuilderBackend:
    def __init__(self, ref_name):
        self.ref_name = ref_name

    def resolve_attr(self, attr):
        return getattr(RefBuilder(self.ref_name), attr)
    
    def resolve_item(self, item):
        return RefBuilder(self.ref_name)[item]


class DataBackend:
    def __init__(self, data):
        self.data = data
    
    def resolve_attr(self, attr):
        try:
            return self.data[attr]
        except KeyError:
            raise AttributeError

    def resolve_item(self, item):
        return self.data[item]


class LazyResource:
    def __init__(self, ref_name):
        self.__backend = RefBuilderBackend(ref_name)

    def __getattr__(self, attr: str):
        return self.__backend.resolve_attr(attr)

    def __getitem__(self, item):
        return self.__backend.resolve_item(item)

    def load_data(self, data):
        self.__backend = DataBackend(data)


class RefBuilder(str):
    _inner: str

    def __new__(cls, content):
        instance = str.__new__(cls, '@{%s}' % content)
        instance._inner = content
        return instance

    def __getattr__(self, attr):
        return RefBuilder('.'.join((self._inner, attr)))

    def __getitem__(self, key):
        return RefBuilder('{}[{}]'.format(self._inner, key))

class Client:
    api_base = '/services/data/v38.0'


class CompositeClient:
    def __init__(self, client=Client):
        self.client = client
        self.request_queue = {}

    def get(self, resource_name, id):
        ref = '{}{}'.format(resource_name, len(self.request_queue))
        resource = LazyResource(ref)
        self.request_queue[ref] = dict(
            resource=resource,
            payload=dict(
                method='GET',
                url=self.client.api_base + f'/sobjects/{resource_name}/{id}',
                referenceId=ref,
            )
        )
        return resource

    def create(self, resource_name, payload):
        ref = '{}{}'.format(resource_name, len(self.request_queue))
        resource = LazyResource(ref)
        self.request_queue[ref] = dict(
            resource=resource,
            payload=dict(
                method='POST',
                url=self.client.api_base + f'/sobjects/{resource_name}/',
                referenceId=ref,
                body=payload,
            )
        )
        return resource
    
    def build_payload(self): 
        return {
            'compositeRequest': [req['payload'] for req in self.request_queue.values()]
        }

    def load_data(self, data):
        for response in data['compositeResponse']:
            resource = self.request_queue.pop(response['referenceId'])['resource']
            resource.load_data(response['body'])
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        return


composite = CompositeClient

"""
with CompositeClient() as client:
    account = client.get('Account', '00123983903')
    opportunity = client.get('Opportunity', account.OpportunityId)
    proposal = client.create('Proposal', dict(
        OpportunityId=opportunity.Id,
        Name=f"{account.Name} - {opportunity.Commission}",
    ))


import pprint
pprint.pprint(client.build_payload())

fixture = {
    'compositeResponse': [{
        'referenceId': 'Account0',
        'body': {
            'Id': '00123983903',
            'OpportunityId': '34534556234',
            'Name': 'Salesforce Dave!',
        }
    }, {
        'referenceId': 'Opportunity1',
        'body': {
            'Id': '34534556234',
            'Commission': 5000000,
        }
    }, {
        'referenceId': 'Proposal2',
        'body': {
            'Id': '02059305356',
        }
    }]
}

print(account.Id)

client.load_data(fixture)


assert account.Id == '00123983903'
assert account['Name'] == 'Salesforce Dave!'
assert account.Name == 'Salesforce Dave!'
"""
