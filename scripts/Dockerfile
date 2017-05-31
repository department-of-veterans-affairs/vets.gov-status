FROM python:3

WORKDIR /application

ENV DATA_DIR="/data" \
    GA_SERVICEACCOUNT="/application/serviceaccount.p12"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/application/updates.sh"]
