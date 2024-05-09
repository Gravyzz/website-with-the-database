# Импорт необходимых модулей из библиотек Flask и Flask-WTF


from flask import Flask, render_template
from flask_wtf import FlaskForm

# Импорт классов полей из модуля wtforms
from wtforms import StringField, IntegerField, SubmitField, TelField, RadioField

# Импорт валидаторов из модуля wtforms.validators
from wtforms.validators import InputRequired

# Импорт модуля SQLAlchemy
from flask_sqlalchemy import SQLAlchemy



# Создаем экземпляр Flask с названием приложения
app = Flask(__name__)

# Установка URI для подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'

# Создаем объект базы данных
db = SQLAlchemy(app)

# Класс Пользователя для базы данных
class Travel(db.Model):
    #Указываем им таблицы
    __tablename__ = 'travel'

    # Заводим поля
    UID = db.Column(db.Integer, primary_key=True)
    Place_of_the_trip = db.Column(db.String(80))
    Date_of_the_trip = db.Column(db.String(80))
    Budget = db.Column(db.String(80))
    Place_of_residence = db.Column(db.String(80))
    How_long = db.Column(db.String(80))
    

   
    # Метод для текстового представления объекта Пользователя
    def __str__(self):
        return f'<Путешествие {self.Place_of_the_trip}, {self.Date_of_the_trip}, {self.Budget}, {self.Place_of_residence}, {self.How_long},  >'

# Определение класса формы регистрации
class RegistrationForm(FlaskForm):  
    # Заводим поля
    Place_of_the_trip = StringField(validators=[InputRequired()])
    Date_of_the_trip = TelField(validators=[InputRequired()])
    Budget = StringField(validators=[InputRequired()])
    Place_of_residence = StringField(validators=[InputRequired()])
    How_long = StringField(validators=[InputRequired()])
    # Поле кнопки отправки формы
    submit = SubmitField(label=('Submit'))

    
# Обработчик маршрута для главной страницы
@app.route('/')
def index():
    db.create_all()
    return render_template('main.html')

# Обработчик маршрута для страницы пользователей с таблицей
@app.route('/users')
def users():
    #SELECT запрос на получение всей таблицы (список записей)
    travels = Travel.query.all() 
    # Вывод полученных Пользователей в консоль
    for user in travels:
        print(user)
    # Возвращаем html c таблицей
    return render_template('users.html', Travel = travels)

# Обработчик маршрута для страницы регистрации
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    # Создаем экземпляр формы для регистрации
    form = RegistrationForm()

    # Проверяем, была ли форма отправлена и прошла ли валидацию
    if form.validate_on_submit():
        # Если форма прошла валидацию, получаем данные из полей формы
        Place_of_the_trip, Date_of_the_trip, Budget, Place_of_residence, How_long = form.Place_of_the_trip.data, form.Date_of_the_trip.data, form.Budget.data, form.Place_of_residence.data, form.How_long.data       
        # Выводим данные формы в консоль для отладки
        print(Place_of_the_trip, Date_of_the_trip, Budget, Place_of_residence, How_long)
        # Создаем новый объект Пользователя
        new_travel = Travel(Place_of_the_trip=Place_of_the_trip, Date_of_the_trip=Date_of_the_trip, Budget= Budget, Place_of_residence=Place_of_residence, How_long=How_long, is_active=True)
        db.session.add(new_travel)  # Добавляем Пользователя в базу данных
        db.session.commit()  # Фиксация изменений в базе данных
        # Возвращаем приветственное сообщение (html) с использованием имени пользователя
        return render_template('success_reg.html')
    
    # Если форма не была отправлена или не прошла валидацию,
    # отображаем HTML-шаблон с формой регистрации,
    # передавая объект формы для отображения введенных пользователем данных
    return render_template('reg_form_wtf.html', form=form)


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False  # Отключаем проверку CSRF для WTForms
    app.run(debug=True)  # Запускаем приложение в режиме отладки
