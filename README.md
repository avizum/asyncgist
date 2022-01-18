# asyncgist
An asynchronous wrapper for the GitHub Gist Rest API.\
This project is a work in progress (WIP), so methods can be changes, removed, or added.\
***
## Installing asyncgist
```sh
pip install git+https://github.com/avizum/asyncgist
```
### Examples 
* [Posting a gist](https://github.com/avizum/asyncgist/blob/master/examples/create_gist.py)
* [Deleting a gist](https://github.com/avizum/asyncgist/blob/master/examples/delete_gist.py)
* [Editing a gist](https://github.com/avizum/asyncgist/blob/master/examples/edit_gist.py)

### Getting a GitHub API token
1. Go to [personal access tokens](https://github.com/settings/tokens)
2. Click generate new token, enter your password
3. Add a note and set the token to never expire (You can revoke the token later.)
4. Check the "Gist" checkbox.
5. Click on "Generate Token"
6. Keep your token safe and keep it somewhere, you won't be able to see the token again if you lose it. If you do lose it, it's okay, just delete the token and create a new one.

### Todo
* Comments
    * List comments on a gist
    * Post a comment
    * Get a comment
    * Edit/Update a comment
    * Delete a comment
* List authenticated user's gists
* List public gists
