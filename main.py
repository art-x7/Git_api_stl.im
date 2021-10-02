import requests

from log.logger import logger
from datetime import datetime, timedelta
from endpoints import GitHubEndpoints
from flask import Flask
from flask_restful import abort, Api, Resource

app = Flask(__name__)
api = Api(app)
app.config.from_object("config.Config")

headers = {"Authorization": 'token %s' % app.config.get("GIT_API_TOKEN")}

url = GitHubEndpoints.repo_url.value % (app.config.get("USER"), app.config.get("REPO_NAME"))

pulls_url = url + GitHubEndpoints.pulls.value
issues_url = url + GitHubEndpoints.issues.value
forks_url = url + GitHubEndpoints.forks.value


@app.route("/")
def hello():
    return f"Github for user: {app.config.get('USER')}"


def abort_if_keys_doenst_exist(key, data):
    if isinstance(data, list):
        for item in data:
            if key not in item.keys():
                abort(404, message=f"GitHub {key} doesn't exist.")
    else:
        if key not in data.keys():
            abort(404, message=f"GitHub {key} doesn't exist.")


class Git_id(Resource):
    def get(self, key):
        r = requests.get(url=url, headers=headers)
        data = r.json()
        abort_if_keys_doenst_exist(key, data)
        keys_list = []
        if isinstance(data, list):
            for item in data:
                keys_list.append(item[key])
            return keys_list
        else:
            return data[key]


class Git_list(Resource):
    def get(self):
        r = requests.get(url=url, headers=headers)
        data = r.json()
        return data


class Git_pulls(Resource):
    def get(self):
        r = requests.get(url=pulls_url, headers=headers)
        data = r.json()
        logger.debug(data)
        return data


class Git_pulls_week(Resource):
    def get(self):
        r = requests.get(url=pulls_url, headers=headers)
        data = r.json()
        pulls_above_two_weeks = []
        for item in data:
            last_update = datetime.fromisoformat(item["updated_at"][:-1])
            two_weeks_date = datetime.now() - timedelta(weeks=2)
            if last_update < two_weeks_date:
                pulls_above_two_weeks.append(item)

        return pulls_above_two_weeks


class Git_issues(Resource):
    def get(self):
        r = requests.get(url=issues_url, headers=headers)
        data = r.json()
        return data


class Git_forks(Resource):
    def get(self):
        r = requests.get(url=forks_url, headers=headers)
        data = r.json()
        return data


api.add_resource(Git_id, '/api/<key>')
api.add_resource(Git_list, '/api')
api.add_resource(Git_pulls, '/api/pulls')
api.add_resource(Git_pulls_week, '/api/pulls_w')
api.add_resource(Git_issues, '/api/issues')
api.add_resource(Git_forks, '/api/forks')

if __name__ == '__main__':
    app.run(debug=True)
