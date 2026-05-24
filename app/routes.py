from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Usuario, Medicamento
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # adiciona medicamentos só se o banco estiver vazio
    if not Medicamento.query.first():
        db.session.add(Medicamento(nome="PARACETAMOL", quantidade=20))
        db.session.add(Medicamento(nome="DIPIRONA", quantidade=15))
        db.session.add(Medicamento(nome="IBUPROFENO", quantidade=10))
        db.session.commit()

    return render_template('index.html')

@main.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = Usuario.query.filter_by(nome=nome).first()
        if user and check_password_hash(user.senha, senha):
            session['user'] = user.nome
            return redirect('/menu')
    return render_template('login.html')

@main.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = generate_password_hash(request.form['senha'])
        novo = Usuario(nome=nome, senha=senha)
        db.session.add(novo)
        db.session.commit()
        return redirect('/login')
    return render_template('cadastro.html')

@main.route('/menu')
def menu():
    if 'user' not in session:
        return redirect('/')
    return render_template('menu.html')

@main.route('/buscar', methods=['GET','POST'])
def buscar():
    resultado = None
    if request.method == 'POST':
        nome = request.form['medicamento']
        med = Medicamento.query.filter(Medicamento.nome.ilike(f"%{nome}%")).first()
        if med:
            resultado = f"{med.nome} - {med.quantidade} unidades"
        else:
            resultado = "Não encontrado"
    return render_template('buscar.html', resultado=resultado)

@main.route('/logout')
def logout():
    session.clear()
    return redirect('/')
@main.route('/add_medicamento', methods=['GET','POST'])
def add_medicamento():
    if request.method == 'POST':
        nome = request.form['nome'].upper()
        quantidade = request.form['quantidade']

        novo = Medicamento(nome=nome, quantidade=quantidade)
        db.session.add(novo)
        db.session.commit()

        return redirect('/menu')

    return render_template('add_medicamento.html')
@main.route('/lista')
def lista():
    meds = Medicamento.query.all()
    return render_template('lista.html', meds=meds)
from reportlab.pdfgen import canvas
from flask import send_file
import io

@main.route('/pdf')
def gerar_pdf():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    meds = Medicamento.query.all()

    y = 800
    for m in meds:
        p.drawString(100, y, f"{m.nome} - {m.quantidade}")
        y -= 20

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="medicamentos.pdf", mimetype='application/pdf')
