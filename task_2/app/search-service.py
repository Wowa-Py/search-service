from fastapi import FastAPI, HTTPException
import requests
import redis
import clickhouse_driver

app = FastAPI()

# Подключение к Redis
r = redis.Redis(host='redis', port=6379, db=0)

# Подключение к ClickHouse
client = clickhouse_driver.Client(host='clickhouse', port=9000, database='default')

# Функция для отправки результата поиска во внешний сервис
def send_result(url, result):
    requests.post(url, json=result)

# Функция для поиска учетной записи в ClickHouse
def search_account(username, ipv4, mac):
    query = f"SELECT * FROM accounts WHERE username='{username}' AND ipv4='{ipv4}' AND mac='{mac}'"
    result = client.execute(query)
    if result:
        return result[0]
    else:
        return None

# API-эндпоинт для получения задачи на поиск учетной записи из очереди Redis
@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    # Задача на поиск учетной записи из очереди Redis
    task = r.get(task_id)
    if task:
        # Разбиваем задачу на поля
        fields = task.decode('utf-8').split(',')
        username, ipv4, mac, url = fields
        # Поиск учетной записи в ClickHouse
        account = search_account(username, ipv4, mac)
        if account:
            # Если учетная запись найдена, отправляем результат во внешний сервис
            send_result(url, account)
            # Сохраняем url на результат успешного поиска в файл success_urls.txt
            with open('/app/data/success_urls.txt', 'a') as f:
                f.write(url + '\n')
            # Удаляем задачу из очереди Redis
            r.delete(task_id)
            return {'message': 'Account found'}
        else:
            # Если учетная запись не найдена, возвращаем ошибку
            raise HTTPException(status_code=404, detail='Account not found')
    else:
        # Если задача не найдена, возвращаем ошибку
        raise HTTPException(status_code=404, detail='Task not found')
