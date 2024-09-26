from flask import Flask, render_template, request, session, jsonify
from OpenAI import OpenAI  # Используем твой модуль для генерации ответов
from OpenAI.OpenAI import create_responce

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Нужен для сессий

# Главная страница - начало диалога
@app.route('/')
def index():
    session.clear()  # Очищаем сессию в начале
    session['variables'] = {
        "name": "",
        "project_info": "",
        "detalization_answers": "",
        "questions": "",
        "task1": "",
        "task2": "",
        "task3": "",
        "task4": "",
        "answer1": "",
        "answer2": "",
        "answer3": "",
        "answer4": ""
    }
    session['stage'] = 0  # Стадия 0 — знакомство
    return render_template('index.html')

# Endpoint для отправки данных пользователя и перехода по стадиям
@app.route('/next', methods=['POST'])
def next_stage():
    variables = session['variables']
    stage = session.get('stage', 0)
    user_input = request.json.get('user_input')

    # Обрабатываем стадии
    if stage == 0:  # Стадия 0: Ввод имени
        variables['name'] = user_input
        response = f"Рада знакомству! {variables['name']}, давай начнем! Расскажи мне побольше о своем проекте: как он называется, как ты видишь его применение, кто твоя целевая аудитория и какие задачи он решает? "
        session['stage'] = 1  # Переходим к следующей стадии

    elif stage == 1:  # Стадия 1: Ввод информации о проекте
        variables['project_info'] = user_input
        response = create_responce(variables, stage)
        response = f"{response['first']}<br>{response['second']}"
        session['stage'] = 2  # Следующая стадия — детализация

    elif stage == 2:  # Стадия 2: Детализация
        variables['detalization_answers'] = user_input
        response = create_responce(variables, stage).choices[0].message.content
        session['stage'] = 3  # Переход к заданиям

    elif stage == 3:  # Стадия 3: Генерация и вывод заданий
        # Генерируем задания с помощью твоего модуля
        response_data = create_responce(variables, stage)
        print(response_data)
        for i in range(1, 5):
            variables[f"task{i}"] = response_data[f"task{i}"]
            print(response_data[f"task{i}"])
        response = f"Вот твоё первое задание: {variables['task1']}"
        session['stage'] = 3.1  # Переход к заданиям

    elif stage == 3.1:  # Стадия 4: Пользователь выполняет задания
        variables['answer1'] = user_input
        response = f"Теперь второе задание: {variables['task2']}"
        session['stage'] = 3.2  # Переход к следующему заданию

    elif stage == 3.2:  # Стадия 4: Пользователь выполняет задания
        variables['answer2'] = user_input
        response = f"Теперь третье задание: {variables['task3']}"
        session['stage'] = 3.3  # Переход к следующему заданию

    elif stage == 3.3:  # Стадия 4: Пользователь выполняет задания
        variables['answer3'] = user_input
        response = f"Теперь четвертое задание: {variables['task4']}"
        session['stage'] = 4  # Переход к следующему заданию

    elif stage == 4:  # Стадия 4: Пользователь выполняет задания
        variables['answer4'] = user_input
        response = create_responce(variables, stage).choices[0].message.content
        print(response)
        session['stage'] = 5

    elif stage == 5:
        response = "Спасибо за участие! 🚀"
        session['stage'] = 0  # Сброс на начало

    # Сохраняем переменные обратно в сессию
    session['variables'] = variables
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
