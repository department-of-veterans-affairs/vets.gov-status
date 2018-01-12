FROM python:3

WORKDIR /application

ENV DATA_DIR="/data" \
    CONFIG_DIR="/application" \
    GA_SERVICEACCOUNT="/application/serviceaccount.json"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/application/updates.sh"]
