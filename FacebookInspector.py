import requests
import json

class FacebookLogin(object):

    ping_url = 'https://www.facebook.com/connect/ping?client_id=308029732682024&domain=localhost&origin=1&redirect_uri=http%3A%2F%2Fstatic.ak.facebook.com%2Fconnect%2Fxd_arbiter%2FLEdxGgtB9cN.js%3Fversion%3D40%23cb%3Df4420681c%26domain%3Dlocalhost%26origin%3Dhttp%253A%252F%252Flocalhost%253A8000%252Ff3779d5c64%26relation%3Dparent&response_type=token%2Csigned_request%2Ccode&sdk=joey'
    login_url = 'https://www.facebook.com/login.php?skip_api_login=1&api_key=308029732682024&signed_next=1&next=https%3A%2F%2Fwww.facebook.com%2Fdialog%2Foauth%3Fredirect_uri%3Dhttp%253A%252F%252Fstatic.ak.facebook.com%252Fconnect%252Fxd_arbiter%252FLEdxGgtB9cN.js%253Fversion%253D40%2523cb%253Df39f1401bc%2526domain%253Dlocalhost%2526origin%253Dhttp%25253A%25252F%25252Flocalhost%25253A8000%25252Ff1ad64e4e%2526relation%253Dopener%2526frame%253Df2e67479a%26display%3Dpopup%26response_type%3Dtoken%252Csigned_request%26domain%3Dlocalhost%26client_id%3D308029732682024%26ret%3Dlogin%26sdk%3Djoey&cancel_uri=http%3A%2F%2Fstatic.ak.facebook.com%2Fconnect%2Fxd_arbiter%2FLEdxGgtB9cN.js%3Fversion%3D40%23cb%3Df39f1401bc%26domain%3Dlocalhost%26origin%3Dhttp%253A%252F%252Flocalhost%253A8000%252Ff1ad64e4e%26relation%3Dopener%26frame%3Df2e67479a%26error%3Daccess_denied%26error_code%3D200%26error_description%3DPermissions%2Berror%26error_reason%3Duser_denied%26e2e%3D%257B%257D'

    def query(self):
        res = requests.get(self.ping_url)
        print 'cookies', requests.utils.dict_from_cookiejar(res.cookies)


class FacebookInspector(object):

    result = ''
    error = ''

    selector = ''
    origin = ''
    condition = ''
    limit = ''
    offset = ''

    query = ''

    fb_url = 'https://graph.facebook.com/fql?q={}&access_token={}&format=json'
    access_token = 'CAAEYJsLLZBSgBADyagOFYp2iXeeQyhFYz8TjIVRDOy6D23ZCBmOUJy12kpax8iWpfBKEUYaRzKR4oGzNd6kdkyypVYUYlfZCHF2dRZAxYgzFPTCVWc6Kfmp3jOZAgd7pvSwCuprYHsBPWmUjt9G8ucjrK0s3ZBmP8VqSLFFRJsQIChg0gZARkrL'

    def _process_query(self):
        if self.query == '':
            self._make_query()

        r = requests.get(self.fb_url.format(self.query, self.access_token))
        result = json.loads(r.text)

        if 'error' in result:
            self.error = result['error']['message']
            raise Exception(self.error)

        self.result = json.loads(r.text)['data']
        return self

    def _make_query(self):
        self.query = ''
        if self.selector == '':
            self.selector = self._get_all_columns(self.origin)
        self.query = 'SELECT %s FROM %s WHERE %s' % (self.selector, self.origin,
                                                self.condition)

        if self.limit != '':
            limit = 'LIMIT %s' % self.limit
            self.query = ' '.join([self.query, limit])

        if self.offset != '':
            offset = 'OFFSET %s' % self.offset
            self.query = ' '.join([self.query, offset])

        return self


    def _get_all_columns(self, table):
        res = self.get_columns_for_table(table).all()
        return ', '.join([col['column_name'] for col in res])

    def _gac(self, table):
        return self._get_all_columns(table)

    def get_columns_for_table(self, table):
        self.query = 'SELECT column_name FROM column WHERE table_name="%s"' % table
        return self

    def find_by_name(self, name):
        self.origin = 'user'
        self.condition = 'contains("%s")' % name
        return self

    def find_by_uid(self, uid):
        self.origin = 'user'
        self.condition = 'uid="%s"' % uid
        return self

    def execute(self, query):
        self.query = query

    def columns(self, cols, default=None):
        self.selector = ', '.join(cols)
        return self

    def begin_at(self, offset):
        self.offset = offset
        return self

    def all(self):
        self._process_query()
        return self.result

    def __getitem__(self, limit):
        if isinstance(limit, int):
            self.limit = limit
        if isinstance(limit, slice):
            self.limit = ','.join(map(str, [limit.start, limit.stop]))

        self._process_query()
        return self.result
