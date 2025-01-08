import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Параметры симуляции
NUM_AGENTS = 100  # Количество агентов
PROB_PURCHASE = 0.08  # Вероятность покупки продукта в день
PROB_REFER = 0.16  # Вероятность оповещения потенциального покупателя после покупки
DAYS_TO_SPOIL = 8  # Количество дней, через которое продукт портится
DAYS_TO_RESET = 5  # Количество дней, через которое пользователь продукта снова становится потенциальным покупателем
OBSERVATION_PERIOD = 90  # Срок наблюдения в днях

# Размеры прямоугольной области
WIDTH = 10
HEIGHT = 10

# День наблюдения
day_count = 0

# Создание популяции агентов
agents = []
for i in range(NUM_AGENTS):
    agent = {
        "type": "potential",  # Тип агента: "potential" или "user"
        "days_since_purchase": 0,  # Количество дней с момента последней покупки
    }
    agents.append(agent)

# Инициализация данных для графика
num_potential = []  # Количество потенциальных клиентов в день
num_users = []  # Количество пользователей продукта в день

# Функция обновления для анимации


def update(frame):
    # Обновление агентов

    global day_count

    for agent in agents:
        if agent["type"] == "potential":
            # Потенциальный покупатель может стать покупателем с вероятностью PROB_PURCHASE
            if random.random() < PROB_PURCHASE:
                agent["type"] = "user"
                agent["days_since_purchase"] = 0
        elif agent["type"] == "user":
            # Пользователь продукта может оповестить потенциального покупателя с вероятностью PROB_REFER
            if random.random() < PROB_REFER:
                for other_agent in agents:
                    if other_agent["type"] == "potential":
                        other_agent["type"] = "user"
                        other_agent["days_since_purchase"] = 0
                        break
            # Продукт портится через DAYS_TO_SPOIL дней
            agent["days_since_purchase"] += 1
            if agent["days_since_purchase"] >= DAYS_TO_SPOIL:
                agent["type"] = "potential"
            # Пользователь продукта снова становится потенциальным покупателем через DAYS_TO_RESET дней
            elif agent["days_since_purchase"] >= DAYS_TO_RESET:
                agent["type"] = "potential"

    # Подсчет количества потенциальных клиентов и пользователей в день
    num_potential.append(
        len([agent for agent in agents if agent["type"] == "potential"]))
    num_users.append(
        len([agent for agent in agents if agent["type"] == "user"]))

    # Отображение агентов в прямоугольной области
    ax1.cla()
    for agent in agents:
        if agent["type"] == "potential":
            ax1.scatter(random.random() * WIDTH,
                        random.random() * HEIGHT, c="yellow")
        elif agent["type"] == "user":
            ax1.scatter(random.random() * WIDTH,
                        random.random() * HEIGHT, c="green")

    # Отображение графика
    ax2.cla()
    ax2.plot(num_potential, label="Потенциальные клиенты")
    ax2.plot(num_users, label="Пользователи продукта")
    ax2.set_xlabel("День")
    ax2.set_ylabel("Количество")
    ax2.legend(loc='upper right', fontsize=8, framealpha=0.3)

    day_count += 1
    if day_count >= OBSERVATION_PERIOD:
        plt.close()  # Закрытие графического окна
        exit()  # Завершение программы


# Создание двух осей для области агентов и графика
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))


# Создание анимации
ani = animation.FuncAnimation(fig, update, interval=10,save_count=OBSERVATION_PERIOD)
plt.show()
