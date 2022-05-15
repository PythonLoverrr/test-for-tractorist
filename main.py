import sys
from random import randint, shuffle

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout,
    QGroupBox, QButtonGroup, QRadioButton,
    QPushButton, QLabel,
)
from PyQt5.QtGui import QPixmap, QIcon

from data_models import Question, User
import data.steppe as style

app = QApplication(sys.argv)
header, questions_list = Question.generate_list_question(style.file_name)
user = User(len(questions_list))

##############################################################################
# Widgets configuration                                                      #
##############################################################################
window = QWidget()
window.setStyleSheet(style.background)
window.setWindowIcon(QIcon(style.logo))
window.resize(
    style.win_width, style.win_height
)

pixmap = QPixmap(style.logo)
logo = QLabel()
logo.resize(pixmap.width(), pixmap.height())
logo.setPixmap(pixmap)

btn_answer = QPushButton('Ответить')  # кнопка ответа
btn_answer.setStyleSheet(style.ans_button_style)
btn_answer.setFixedSize(200, 50)

lb_Question = QLabel()  # текст вопроса
lb_Question.setStyleSheet(style.q_text_style)
lb_Question.setWordWrap(True)
lb_Question.setAlignment(Qt.AlignCenter)

RadioGroupBox = QGroupBox(header)  # группа на экране для переключателей с ответами
RadioGroupBox.setStyleSheet(style.header_text_style)

rbtn_1 = QRadioButton()
rbtn_2 = QRadioButton()
rbtn_3 = QRadioButton()
rbtn_4 = QRadioButton()
button_group = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]
[rbtn.setStyleSheet(style.radiobutton_style) for rbtn in button_group]

RadioGroup = QButtonGroup()  # это для группировки переключателей, чтобы управлять их поведением
[RadioGroup.addButton(rbtn) for rbtn in button_group]

layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout()  # вертикальные будут внутри горизонтального
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1)  # два ответа в первый столбец
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3)  # два ответа во второй столбец
layout_ans3.addWidget(rbtn_4)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3)  # разместили столбцы в одной строке

RadioGroupBox.setLayout(layout_ans1)  # готова "панель" с вариантами ответов

AnsGroupBox = QGroupBox("Результат теста")
lb_Result = QLabel('И...')  # здесь размещается надпись "правильно" или "неправильно"
lb_Correct = QLabel('ответ будет тут!')  # здесь будет написан текст правильного ответа


layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)

AnsGroupBox.setLayout(layout_res)
layout_line1 = QHBoxLayout()  # вопрос
layout_line2 = QHBoxLayout()  # варианты ответов или результат теста
layout_line3 = QHBoxLayout()  # кнопка "Ответить"

layout_line1.addWidget(lb_Question, stretch=1)
layout_line1.addWidget(logo, alignment=Qt.AlignRight)
layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)
AnsGroupBox.hide()  # скроем панель с ответом, сначала должна быть видна панель вопросов

layout_line3.addStretch(1)
layout_line3.addWidget(btn_answer, stretch=2)  # кнопка должна быть большой
layout_line3.addStretch(1)

layout_card = QVBoxLayout()

layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5)  # пробелы между содержимым


##############################################################################
# Functional                                                                 #
##############################################################################
def show_result():
    """Показать панель ответов """
    RadioGroupBox.hide()
    lb_Question.hide()
    AnsGroupBox.setStyleSheet(style.lb_Finish_style)
    lb_Correct.setText(f'{user.score}/{user.question_num}')
    lb_Correct.setStyleSheet(style.lb_Result_style)
    AnsGroupBox.show()
    btn_answer.setStyleSheet(style.res_button_style)
    btn_answer.setText('Закрыть')


def show_question():
    """ Показать панель вопросов """
    btn_answer.setText('Ответить')
    RadioGroup.setExclusive(False)  # сняли ограничения, чтобы можно было сбросить выбор радиокнопки
    [rbtn.setChecked(False) for rbtn in button_group]
    RadioGroup.setExclusive(True)  # вернули ограничения, теперь только одна радиокнопка может быть выбрана


def ask(q: Question):
    """
    Функция записывает значения вопроса и ответов в соответствующие виджеты,
    при этом варианты ответов распределяются случайным образом
    """
    shuffle(button_group)  # перемешали список из кнопок, теперь на первом месте списка какая-то непредсказуемая кнопка
    button_group[0].setText(q.right_answer)  # первый элемент списка заполним правильным ответом, остальные - неверными
    button_group[1].setText(q.wrong1)
    button_group[2].setText(q.wrong2)
    button_group[3].setText(q.wrong3)
    lb_Question.setText(q.question)  # вопрос
    show_question()  # показываем панель вопросов


# def show_correct(res):
#     """ Показать результат - установим переданный текст в надпись "результат" и покажем нужную панель """
#     lb_Result.setText(res)
#     show_result()


def check_answer():
    """Если выбран какой-то вариант ответа, то надо проверить и показать панель ответов"""
    if any([rbtn.isChecked() for rbtn in button_group]):
        if button_group[0].isChecked():
            user.score += 1
        next_question()


def next_question():
    """Задает случайный вопрос из списка """
    if questions_list:
        shuffle(questions_list)
        q = questions_list.pop()
        ask(q)
    else:
        show_result()


def click_answer_button():
    """Определяет, надо ли показывать другой вопрос либо проверить ответ на этот """
    if btn_answer.text() == 'Ответить':
        check_answer()  # проверка ответа
    elif btn_answer.text() == 'Закрыть':
        exit()

##############################################################################
# Run application                                                            #
##############################################################################
window.setLayout(layout_card)
window.setWindowTitle(header)
btn_answer.clicked.connect(click_answer_button)  # по нажатии на кнопку выбираем, что конкретно происходит
next_question()
window.show()
app.exec()
