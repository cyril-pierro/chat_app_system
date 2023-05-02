# Account Service

This service is responsible for the authentication and authorization of users of the chat application. It also supports user operations like change password, email, etc


## It uses the following to start it up

- Bash script (.sh file)
- Command line option with poetry


**Note** Always migrate your database before running the application

## For Bash

```bash
   $ bash scripts/startup.sh
```

## For Poetry command line

```bash
   $ poetry run account migrate && poetry run account run
```

