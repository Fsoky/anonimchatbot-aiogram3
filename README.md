<h1 align="center">🤖 Anonymous ChatBot for Telegram 📱</h1>

<p align="center">
  <a href="https://t.me/fsoky_community">
    <img src="https://img.shields.io/badge/We're in telegram-blue?style=for-the-badge&logo=Telegram" alt="Telegram">
  </a>
</p>

* Python 3.10^
* AIOgram 3.x
* MongoDB (motor)

#### Installation
```bash
git clone https://github.com/Fsoky/anonimchatbot-aiogram3.git
```
#### Change directory
```bash
cd anonimchatbot-aiogram3
```
#### Use [poetry](https://python-poetry.org/docs/) for install dependencies (`pip install poetry`)
```bash
poetry install
```
#### Run
```bash
python src/__main__.py
```

> [!TIP]
> Make sure you modify the .env file before running this script!


#### Installation in Docker
```bash
docker compose up
```
**This will output the logs of your docker containers:**
1) anonchat-telegram
2) mongo
3) mongo-express

**To access admin panel of your database go to `localhost:8081` in your browser and enter your credentials in the prompt**

#### Set containers to run as daemons

After checking that everything works as expected, you can set those containers to run as daemons by stopping previous docker command with ctrl + c and running it again with:
```bash
docker compose up -d
```