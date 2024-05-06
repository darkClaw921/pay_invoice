from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Проверяем, что запрос пришел от GitHub и событие - push
    if request.headers.get('X-GitHub-Event') == 'push':
        payload = request.json
        ref = payload['ref']
        headCommit = payload['head_commit']
        modified = headCommit['modified']


        # Проверяем, что событие - push в ветку master
        if ref == 'refs/heads/master' and "pay_invoice/" in modified:
        
            # Запускаем скрипт для обработки события
            cwd = '/pay_invoice'  # Укажите путь к вашей папке
            pwd = os.getcwd()
            path=pwd+cwd
            print(path)
            
            #NOTE
            #COPY poetry.lock pyproject.toml to /testdrone
            subprocess.Popen(['cp', f'{pwd}/poetry.lock', f'{path}/poetry.lock'])
            subprocess.Popen(['cp', f'{pwd}/pyproject.toml', f'{path}/pyproject.toml'])

            #chmod +x deploy.sh #для прав на исполнение
            subprocess.Popen([f'{path}/deploy.sh'], cwd=pwd+cwd)

            subprocess.Popen(['rm', f'{path}/poetry.lock'])
            subprocess.Popen(['rm', f'{path}/pyproject.toml'])

    return jsonify({'message': 'Webhook received'}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
