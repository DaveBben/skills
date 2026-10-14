# Gitea

* **Blocking relation:** issue dependencies, `POST /repos/{o}/{r}/issues/{n}/dependencies`; issue `n` is blocked by the issue in the body.
* **Board placement:** a separate container. Check the swagger for a projects endpoint (added in v28.0.0). Where it exists: `POST /repos/{o}/{r}/projects/{id}/columns/{col}/issues/{issue_id}`, where `issue_id` is the issue's global `id`, not its `#` index. Where it does not: tell the user to tick the issues in the Issues tab, then Project, then the board's name.
