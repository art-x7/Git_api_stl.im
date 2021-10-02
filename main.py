import requests
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

print(app.config.get("GIT_API_TOKEN"))

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
    r = requests.get(url=url, headers=headers)
    data = r.json()

    def get(self, key):
        abort_if_keys_doenst_exist(key, self.data)
        keys_list = []
        if isinstance(self.data, list):
            for item in self.data:
                keys_list.append(item[key])
            return keys_list
        else:
            return self.data[key]


class Git_list(Resource):
    r = requests.get(url=url, headers=headers)
    data = r.json()

    def get(self):
        return self.data


class Git_pulls(Resource):
    r = requests.get(url=pulls_url, headers=headers)
    data = r.json()

    def get(self):
        return self.data


class Git_pulls_week(Resource):
    r = requests.get(url=pulls_url, headers=headers)
    data = r.json()

    def get(self):
        pulls_above_two_weeks = []
        for item in self.data:
            last_update = datetime.fromisoformat(item["updated_at"][:-1])
            two_weeks_date = datetime.now() - timedelta(weeks=2)
            if last_update < two_weeks_date:
                pulls_above_two_weeks.append(item)

        return pulls_above_two_weeks


class Git_issues(Resource):
    r = requests.get(url=issues_url, headers=headers)
    data = r.json()

    def get(self):
        return self.data


class Git_forks(Resource):
    r = requests.get(url=forks_url, headers=headers)
    data = r.json()

    def get(self):
        return self.data


api.add_resource(Git_id, '/api/<key>')
api.add_resource(Git_list, '/api')
api.add_resource(Git_pulls, '/api/pulls')
api.add_resource(Git_pulls_week, '/api/pulls_w')
api.add_resource(Git_issues, '/api/issues')
api.add_resource(Git_forks, '/api/forks')


if __name__ == '__main__':
    app.run(debug=True)
