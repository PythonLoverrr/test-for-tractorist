import sys
from random import randint, shuffle 

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QRadioButton,  
        QPushButton, QLabel, QMainWindow,
        )
from PyQt5.QtGui import QPixmap, QPalette
import steppe as style


logo = style.logo

app = QApplication(sys.argv)

window = QWidget()
window.setStyleSheet(style.background)
window.setWindowTitle("Тест")
window.resize(1500,800)

pixmap =  QPixmap(logo)
logo = QLabel()
logo.resize(pixmap.width(),pixmap.height())
logo.setPixmap(pixmap)

class Question():
    ''' содержит вопрос, правильный ответ и три неправильных'''
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3
 
with open("steppe.txt","r", encoding = "utf-8") as file:
        
        questions_list = [] 
        temp = []
        file.readline()
        for num, line in enumerate (file, start=1):
                temp.append(line.strip())
                if num %5 ==0:
                        questions_list.append(Question(*temp[-5:]))

 
btn_OK = QPushButton('Ответить') # кнопка ответа
btn_OK.setStyleSheet(style.ans_button_style)
btn_OK.setFixedSize(200,50)

lb_Question = QLabel('Самый сложный вопрос в мире!') # текст вопроса
lb_Question.setStyleSheet(style.q_text_style)
lb_Question.setWordWrap(True)
 
RadioGroupBox = QGroupBox("Тест для тракториста") # группа на экране для переключателей с ответами
RadioGroupBox.setStyleSheet(style.header_text_style)
 
rbtn_1 = QRadioButton('Вариант 1')
rbtn_2 = QRadioButton('Вариант 2')
rbtn_3 = QRadioButton('Вариант 3')
rbtn_4 = QRadioButton('Вариант 4')

rbtn_4.setStyleSheet(style.radiobutton_style)
rbtn_3.setStyleSheet(style.radiobutton_style)
rbtn_2.setStyleSheet(style.radiobutton_style)
rbtn_1.setStyleSheet(style.radiobutton_style)

RadioGroup = QButtonGroup() # это для группировки переключателей, чтобы управлять их поведением
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)
 
layout_ans1 = QHBoxLayout()   
layout_ans2 = QVBoxLayout() # вертикальные будут внутри горизонтального
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1) # два ответа в первый столбец
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3) # два ответа во второй столбец
layout_ans3.addWidget(rbtn_4)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3) # разместили столбцы в одной строке
 
RadioGroupBox.setLayout(layout_ans1) # готова "панель" с вариантами ответов 
 
AnsGroupBox = QGroupBox("Результат теста")
lb_Result = QLabel('И...') # здесь размещается надпись "правильно" или "неправильно"
lb_Correct = QLabel('ответ будет тут!') # здесь будет написан текст правильного ответа
lb_Correct_2 = QLabel(".")#############
 
layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)
layout_res.addWidget(lb_Correct_2, alignment=Qt.AlignHCenter, stretch=2)######

AnsGroupBox.setLayout(layout_res)
layout_line1 = QHBoxLayout() # вопрос
layout_line2 = QHBoxLayout() # варианты ответов или результат теста
layout_line3 = QHBoxLayout() # кнопка "Ответить"
 
layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout_line1.addWidget(logo, alignment=Qt.AlignRight)
layout_line2.addWidget(RadioGroupBox)   
layout_line2.addWidget(AnsGroupBox)  
AnsGroupBox.hide() # скроем панель с ответом, сначала должна быть видна панель вопросов
 
layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2) # кнопка должна быть большой
layout_line3.addStretch(1)
 
layout_card = QVBoxLayout()
 
layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5) # пробелы между содержимым
def show_result():
    ''' показать панель ответов '''
    RadioGroupBox.hide()
    logo.hide()
    #window.resize(250,250)
    lb_Question.hide()
    AnsGroupBox.setStyleSheet(style.lb_Result_style )
    AnsGroupBox.setStyleSheet(style.lb_Finish_style)
    print(str(window.score))
    lb_Correct.setText(str(window.score))
    lb_Correct_2.setText(str("/10"))
    AnsGroupBox.show()
    btn_OK.setText('Закрыть')
 
def show_question():
    ''' показать панель вопросов '''
    btn_OK.setText('Ответить')
    RadioGroup.setExclusive(False) # сняли ограничения, чтобы можно было сбросить выбор радиокнопки
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    RadioGroup.setExclusive(True) # вернули ограничения, теперь только одна радиокнопка может быть выбрана
 
answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]
 
def ask(q: Question):
    ''' функция записывает значения вопроса и ответов в соответствующие виджеты, 
    при этом варианты ответов распределяются случайным образом'''
    shuffle(answers) # перемешали список из кнопок, теперь на первом месте списка какая-то непредсказуемая кнопка
    answers[0].setText(q.right_answer) # первый элемент списка заполним правильным ответом, остальные - неверными
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_Question.setText(q.question) # вопрос
    show_question() # показываем панель вопросов 
 
def show_correct(res):
    ''' показать результат - установим переданный текст в надпись "результат" и покажем нужную панель '''
    lb_Result.setText(res)
    show_result()
 
def check_answer():
    ''' если выбран какой-то вариант ответа, то надо проверить и показать панель ответов'''
    if answers[0].isChecked():
        # правильный ответ!
        window.score += 1
        next_question()
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            next_question()
    
def next_question():
    ''' задает случайный вопрос из списка '''
    window.total += 1 
    if window.total<=len(questions_list):
        q = questions_list[window.total -1]
        ask(q)
    else:
        show_result()
    
def click_OK():
    ''' определяет, надо ли показывать другой вопрос либо проверить ответ на этот '''
    if btn_OK.text() == 'Ответить':
        check_answer() # проверка ответа
    elif btn_OK.text() == 'Закрыть':
        exit_button_style = "QPushButton{font-size: 9pt;background-color: rgb(240, 240, 240);}"
        btn_OK.setStyleSheet(exit_button_style)
        exit()

window.setLayout(layout_card)
window.setWindowTitle('Тест для тракториста')
btn_OK.clicked.connect(click_OK) # по нажатии на кнопку выбираем, что конкретно происходит
window.score = 0
window.total = 0
next_question()
#window.resize(1500, 800)
window.show()
app.exec()




































 





























