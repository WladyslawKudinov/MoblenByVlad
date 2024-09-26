import time

from pywebio import start_server
from pywebio.input import input, FLOAT, textarea, actions
from pywebio.output import put_text, put_markdown

from OpenAI.OpenAI import create_responce


def bmi():
    variables = {"name":"", "project_info":"", "detalization_answers":"", "questions":"", "task1":"", "task2":"", "task3":"", "task4":"", "answer1":"", "answer2":"", "answer3":"", "answer4":""}
    responses = []

    stage = 0 # 0/5 understanding the project
    name = input("Привет, меня зовут Зари! Я очень хотела бы с тобой познакомиться, как тебя зовут?🥹", value="Вася")
    variables["name"] = name
    put_markdown("<h1>Зари</h1>")
    put_markdown(f"""Привет, {name} 👋
    
    <b>Я буду твоим наставником на пути к успеху с твоим проектом. Очень рада познакомиться! 😊</b>  
    
    Расскажи мне побольше о своем проекте: как он называется, как ты видишь его применение, кто твоя целевая аудитория  
    и какие задачи он решает?  

    Хочу понять все детали, чтобы помочь тебе наилучшим образом. Жду твоего ответа! 🚀""")
    project_info = textarea("Расскажи мне побольше о своём проекте:", rows=10, value="Ну, наш проект - это ИИ-ассистент для школ. Он может генерировать и проверять задания. То есть мы значительно сокращаем время преподавателей на проверку и составление заданий, а ученикам моментально даем надежный фидбек. Пока что мы думали внедрить это в работу репетиторов по обществознанию, но не вышло. Потом попробовали продавать школам, но тоже не получилось. И сейчас мы пробуем продать это онлайн-курсам вроде Скиллбокса. Мы сейчас MVP и думаем в B2B2C.")
    variables["project_info"] = project_info
    put_markdown(f"<h1>{variables['name']}</h1>")
    put_markdown(f"{project_info}")

    stage = 1 # 1/5 selecting additional questions for detalization
    put_markdown(f"""<h1>Зари</h1>""")
    response = create_responce(variables, stage) # json response
    first_response = response["first"]
    second_response = response["second"]
    variables["questions"] = second_response
    put_markdown(first_response+"<br>"+second_response)
    detalization_answers = textarea("Раскрой детали о проекте!")
    variables["detalization_answers"] = detalization_answers
    put_markdown(f"<h1>{variables['name']}</h1>")
    put_markdown(f"{detalization_answers}")

    stage = 2 # 2/5 analyzing the answers on additional questions
    put_markdown(f"""<h1>Зари</h1>""")
    response = create_responce(variables, stage)
    responses.append(response.choices[0].message.content)
    put_markdown(response.choices[0].message.content)
    put_markdown("<h3>Теперь, чтобы помочь тебе отточить навыки и решить эти проблемы, я хочу дать тебе несколько заданий. Готов? 🚀</h3>")
    actions(label="Готов к заданиям?", buttons=[
        {'label': 'Да!', 'value': 'continue', 'color': 'success'},
        {'label': 'Завершить.', 'value': 'finish', 'color': 'danger'}
    ])

    if actions == "finish":
        put_markdown("<h1>Зари</h1>")
        put_markdown(f"""<h3>Жаль, что ты не готов к заданиям. Надеюсь, что ты вернешься, когда будешь готов. Удачи! 🍀</h3>""")
        return
    else:
        put_markdown("<h1>Зари</h1>")
        put_markdown(f"""<h3>Отлично! Тогда давай начнем! 🚀</h3>""")

    stage = 3 # 3/5 generating tasks
    response = create_responce(variables, stage)
    for i in range(4):
        variables[f"task{i+1}"] = response[f"task{i+1}"]

    put_markdown(f"""<h1>Зари</h1>""")
    put_markdown(f"""<h3>Вот твое первое задание:</h3>""")
    put_markdown(f"""<h3>{variables["task1"]}</h3>""")
    variables["answer1"] = textarea("Ваш ответ на задание:")

    put_markdown(f"""<h1>Зари</h1>""")
    put_markdown(f"""<h3>Вот твое второе задание:</h3>""")
    put_markdown(f"""<h3>{variables["task2"]}</h3>""")
    variables["answer2"] = textarea("Ваш ответ на задание:")

    put_markdown(f"""<h1>Зари</h1>""")
    put_markdown(f"""<h3>Вот твое третье задание:</h3>""")
    put_markdown(f"""<h3>{variables["task3"]}</h3>""")
    variables["answer3"] = textarea("Ваш ответ на задание:")

    put_markdown(f"""<h1>Зари</h1>""")
    put_markdown(f"""<h3>Вот твое четвертое задание:</h3>""")
    put_markdown(f"""<h3>{variables["task4"]}</h3>""")
    variables["answer4"] = textarea("Ваш ответ на задание:")

    stage = 4 # 4/5 analyzing the answers on tasks
    put_markdown(f"""<h1>Зари</h1>""")
    response = create_responce(variables, stage)
    responses.append(response.choices[0].message.content)
    put_markdown(response.choices[0].message.content)

    put_markdown(f"""<h1>Зари</h1>""")
    put_markdown(f"""<h3>Спасибо за участие в проекте! 🚀</h3>""")




