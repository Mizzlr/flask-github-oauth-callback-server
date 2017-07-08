import json
from flask import Flask, request, jsonify
from github import Github, GithubError

app = Flask(__name__)
dumpfile = 'data.json'

@app.route('/save')
def save():
    code = request.args.get('code', None)
    state = request.args.get('state', None)
    if not code or not state:
        return "Please provide `code` and `state` query parameter.", 400

    jdata = json.load(open(dumpfile, 'r'))
    jdata.append({
        'code': code,
        'state': state,
    })
    json.dump(jdata, open(dumpfile, 'w'), indent=4)

    return "Saved code: {} state: {}".format(code, state), 200

@app.route('/load')
def load():
    state = request.args.get('state', None)
    jdata = json.load(open(dumpfile, 'r'))
    if not state:
        return jsonify(jdata)

    for jdatum in jdata:
        if jdatum['state'] == state:
            return jsonify(jdatum)

    return 'No data found for state: {}'.format(state), 404

@app.route('/clear')
def clear():
    state = request.args.get('state', None)
    jdata = json.load(open(dumpfile, 'r'))
    if not state:
        open(dumpfile, 'w').write('[ ]')
        return 'Cleared everything', 200

    jdata2 = []
    for jdatum in jdata:
        if jdatum['state'] != state:
            jdata2.append(jdatum)

    json.dump(jdata2, open(dumpfile, 'w'), indent=4)
    return "Cleared data for state: {}".format(state), 200

@app.route('/github')
def github():
    name = request.args.get('name', None)
    if not name:
        return 'Please provide Github username `name` query param', 400

    access_token = request.args.get('access_token', None)
    github = Github(name, access_token)

    try:
        repo = request.args.get('repo', None)
        if not repo:
            return jsonify(github.repos())

        typ = request.args.get('type', 'branches') # or commits
        if typ == 'branches':
            return jsonify(github.branches(repo))
        elif typ == 'commits':
            return jsonify(github.commits(repo))
        else:
            return 'Please provide `type` query params. Optional are `branches`, `commits`', 400
    except GithubError as exc:
        return 'Invalid params passed. ' + str(exc), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
