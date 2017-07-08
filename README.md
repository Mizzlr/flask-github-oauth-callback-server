# flask-github-oauth-callback-server

Endpoint to save Github callback
http://139.59.60.222:5050/save

Endpoint to find Github OAuth code
http://139.59.60.222:5050/load

Endpoint to get `repos`, `branches` and `commits`
http://139.59.60.222:5050/github

Example
```sh
# List all Github repos for user Mizzlr
$ curl http://139.59.60.222:5050/github\?name=Mizzlr
# List all branches in aurea-understand
$ curl http://139.59.60.222:5050/github\?name=Mizzlr\&repo=aurea-understand
# List all commits in aurea-understand 
$ curl http://139.59.60.222:5050/github\?name=Mizzlr\&repo=aurea-understantd\&type=commits
```
