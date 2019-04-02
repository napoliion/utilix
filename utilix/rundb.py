import os
import requests
import json
import datetime
import logging
from utilix.config import Config

logger = logging.getLogger("utilix")

config = Config()

PREFIX = config.get('RunDB', 'rundb_api_url')
BASE_HEADERS = {'Content-Type': "application/json", 'Cache-Control': "no-cache"}


class Token:
    """
    Object handling tokens for runDB API access.
    
    """
    def __init__(self, path=os.path.join(os.environ['HOME'], ".dbtoken")):
        # if token path exists, read it in. Otherwise make a new one
        if os.path.exists(path):
            with open(path) as f:
                json_in = json.load(f)
                self.string = json_in['string']
                self.creation_time = json_in['creation_time']
        else:
            self.string = self.new_token()
            self.creation_time = datetime.datetime.now().timestamp()
        self.path = path

        # for writing to disk
        self.json = dict(string=self.string, creation_time=self.creation_time)
        # save the token json to disk
        self.write()
        # refresh if needed
        self.refresh()

    def __call__(self):
        return self.string

    def new_token(self):
        path = PREFIX + "/login"
        data=json.dumps({"username": config.get('RunDB', 'rundb_api_user'),
                         "password": config.get('RunDB', 'rundb_api_password')})
        response = requests.post(path, data=data, headers=BASE_HEADERS)
        return json.loads(response.text)['access_token']

    @property
    def is_valid(self):
        # TODO do an API call for this instead?
        return datetime.datetime.now().timestamp() - self.creation_time < 24*60*60

    def refresh(self):
        # if valid, don't do anything
        if self.is_valid:
            logger.debug("Token is valid")
            return
        # update the token string
        url = PREFIX + "/refresh"
        headers = BASE_HEADERS.copy()
        headers['Authorization'] = "Bearer {string}".format(string=self.string)
        response = requests.get(url, headers=headers)
        # if rewew fails, try logging back in
        if response.status_code is None or response.status_code is not 200:
            self.string = self.new_token()
            self.creation_time = datetime.datetime.now().timestamp()
        else:
            self.string = json.loads(response.text)['access_token']
        # write out again
        self.write()
        logger.debug("Token refreshed")

    def write(self):
        with open(self.path, "w") as f:
            json.dump(self.json, f)


class DB:
    """Wrapper around the RunDB API"""

    def __init__(self, token_path=os.path.join(os.environ['HOME'], ".dbtoken")):
        # Takes a path to serialized token object
        token = Token(token_path)

        self.headers = BASE_HEADERS.copy()
        self.headers['Authorization'] = "Bearer {token}".format(token=token())

        #initialize some variables
        self.run_number = None
        self.run_name = None
        self.run_detector = None
        self.set_run = False
        self.selector = 'number'
        self.select = None

    def set_run_number(self, run_number, detector='tpc'):
        # Generalize your number vs. name approach to fix the input
        self.run_number = run_number
        self.run_detector = detector
        self.run_name = self.get_name(self.run_number, detector=detector)
        self.set_run = True
        self._setup()

    def set_run_name(self, run_name, detector='tpc'):
        # Generalize your number vs. name approach to fix the input
        self.run_name = run_name
        self.run_detector = detector
        self.run_number = self.get_number(self.run_name, detector=detector)
        self.set_run = True
        self._setup()

    #Helper:
    def _get(self, url):
        return requests.get(PREFIX + url, headers=self.headers)

    def _put(self, url, data):
        return requests.put(PREFIX + url, data, headers=self.headers)

    def _post(self, url, data):
        return requests.post(PREFIX + url, data, headers=self.headers)

    def _delete(self, url, data):
        return requests.delete(PREFIX + url, data=data, headers=self.headers)

    def _setup(self):
        #This helper function sets your url string later regarding the detector type:
        # xenon1t:
        #         -tpc runs have names and run numbers
        #         -mv runs have names but run number is zero
        # xenonnt:
        #         -Uses a continues increasing run number since all three detectors
        #          are starting at the same time

        if self.run_detector=='mv' or self.run_number == 0:
            self.selector='name'
            self.select=self.run_name
        elif self.run_detector == 'tpc' or self.run_number > 0:
            self.selector='number'
            self.select=self.run_number

    def get_name(self, number=None, detector='tpc'):
        # TODO check against the detector, if necessary
        url = "/runs/number/{number}/filter/detector".format(number=number)
        response = json.loads(self._get(url).text)
        return response['results']['name']

    def get_number(self, name=None, detector='tpc'):
        url = "/runs/name/{name}/filter/detector".format(name=name)
        response = json.loads(self._get(url).text)
        return response['results']['number']

    def get_doc(self):
        # return the whole run doc for this run number
        url = '/runs/{selector}/{num}'.format(selector=self.selector, num=self.select)
        return json.loads(self._get(url).text)['results']

    def get_data(self):
        url = '/runs/{selector}/{num}'.format(selector=self.selector, num=self.select)
        return json.loads(self._get(url).text)['results']['data']

    def get_data1(self):
        url = '/runs/{selector}/{num}/data/dids'.format(selector=self.selector, num=self.select)
        print(self._get(url).text)
        return json.loads(self._get(url).text)['results']

    def update_data(self, datum):
        print(datum)
        url = '/run/{selector}/{num}/data/'.format(selector=self.selector, num=self.select)
        return self._post(url, data=datum)

    def delete_datum(self, datum):
        datum = json.dumps(datum)
        url = '/run/{selector}/{num}/data/'.format(selector=self.selector, num=self.select)
        return self._delete(url, data=datum)


# for testing
def test():
    db = DB()
    db.set_run_number(2000)
    db_data = db.get_data()
    print("------")
    print(db_data)


if __name__ == "__main__":
    test()
