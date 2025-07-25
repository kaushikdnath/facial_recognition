apt update 
apt install curl
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl -o /etc/apt/sources.list.d/mssql-release.list https://packages.microsoft.com/config/ubuntu/22.04/prod.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 \
    && pip install psycopg2-binary pyodbc