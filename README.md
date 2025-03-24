# MariaDB Crash When Accessing `information_schema.users`

A dockerized Flask app that uses MariaDB and makes it crash when trying to access the `information_schema.users`.

## How to run

Build the docker image:

```bash
docker compose build --no-cache
```

Run the docker container:

```bash
docker compose up
```

## How to reproduce

Check that everything is running:

```bash
curl "http://0.0.0.0:5000/query?query=SELECT+*+FROM+user"
```

Should return:

```html
<table class="table table-striped">
    <thead>
        <tr>
            <th>id</th>
            <th>username</th>
            <th>password</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>admin</td>
            <td>password</td>
        </tr>
    </tbody>
</table>
```

Make the app crash by accessing `information_schema.users`:

```bash
curl "http://0.0.0.0:5000/query?query=SELECT+*+FROM+information_schema.users"
```

Restart the container if you want to keep using the app (it does not recover from the crash):

```bash
docker compose restart
```
