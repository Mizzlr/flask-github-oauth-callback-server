import json
import requests

class GithubError(Exception): pass

class Github:
    def __init__(self, name, access_token=None):
        self.name = name
        self.access_token = access_token
        self.base_url = 'https://api.github.com/'

    def repos(self):
        url = self.base_url + 'users/' + self.name + '/repos'
        if self.access_token:
            url += '?access_token=' + self.access_token
        print(url)
        response = requests.get(url)

        repos = []
        try:
            for repo in response.json():
                repos.append(repo['name'])
        except Exception as exc:
            raise GithubError(response.content)

        return repos

    def branches(self, repo):
        url = self.base_url + 'repos/' + self.name + '/' + repo + '/branches'
        if self.access_token:
            url += '?access_token=' + self.access_token
        print(url)
        response = requests.get(url)

        branches = []
        try:
            for branch in response.json():
                branches.append(branch['name'])
        except Exception as exc:
            raise GithubError(response.content)

        return branches

    def commits(self, repo):
        url = self.base_url + 'repos/' + self.name + '/' + repo + '/commits'
        if self.access_token:
            url += '?access_token=' + self.access_token
        print(url)
        response = requests.get(url)

        commits = []
        try:
            for commit in response.json():
                commits.append({
                    'sha': commit['sha'],
                    'message': commit['commit']['message'],
                    'parents': [x['sha'] for x in commit['parents']],
                    'author': commit['commit']['author']['name'],
                    'date': commit['commit']['author']['date']
                })
        except Exception as exc:
            raise GithubError(response.content)

        return commits

def test():
    github = Github('Mizzlr')
    repos = github.repos()
    print(json.dumps(repos, indent=4))
    for repo in repos[0]:
        print('Repo: ', repo)
        branches = github.branches(repo)
        print(json.dumps(branches, indent=4))
        commits = github.commits(repo)
        print(json.dumps(commits, indent=4))


if __name__ == '__main__':
    test()