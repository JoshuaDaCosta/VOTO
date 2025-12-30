from datetime import datetime
from flask import*
from flask import render_template, request, redirect, url_for, session, abort, flash
from index import Voto
import sqlite3
from FRONTEND import FRONTEND
from crypto import encrypt_user, decrypt_user




@FRONTEND.route("/")
def home():
    try:
        sy=Voto()
        resultados=sy.apurar_votos()
        votos_hash = sy.listar_hash_eleitores()
        return render_template("index.html", resultados=resultados, votos_hash=votos_hash)
    except Exception as e:
        return render_template("entidade.html")


@FRONTEND.route("/candidato", methods=["GET", "POST"])
def candidato():
    if request.method=="POST":
        try:
            nome=request.form.get("username").strip() 
            telf=request.form.get("phone")
            email=request.form.get("email")
            partido=request.form.get("partido")
            sy=Voto()
            sy.candidato()
            sy.alistar(nome, telf, email, partido)
            session["user"]=email
            
            return redirect(url_for("app_candidato"))
            
        except:
            return redirect("/")
            
    return render_template("candidato.html")

@FRONTEND.route("/app_candidato")
def app_candidato():
    if ("user" in session):
        return f"Bem-vindo, {session['user']}, <a href='/sair'>Sair</a>!"
   
    
    abort(404)
    return "Não tens permissão"

@FRONTEND.route("/app_eleitor", methods=["GET", "POST"])
def app_eleitor():
    try:
        con=Voto.conexao(self=None)
        cursor=con.cursor()
        cursor.execute("SELECT * FROM CANDIDATOS")
        candidatos=cursor.fetchall()
        for i in range(len(candidatos)):

            nome_d=decrypt_user(candidatos[i][1])
            telefone_d=decrypt_user(candidatos[i][2])
            partido_d=decrypt_user(candidatos[i][3])
            email_d=decrypt_user(candidatos[i][4])
            candidatos[i]=[candidatos[i][0], nome_d, telefone_d, partido_d, email_d]
            
        return render_template("app_eleitor.html", candidatos=candidatos)
    except Exception as e:
        abort(404)
        return redirect("/")

@FRONTEND.route("/eleitor", methods=["GET", "POST"])
def eleitor():
    if request.method=="POST":
        try:
            global nome_e
            nome_e = request.form.get("username").strip()
            telf=request.form.get("phone")
            bi=request.form.get("bi")
            gps=request.form.get("gps")
            sy=Voto()
            sy.eleitor()
            sy.alistar_e(nome_e, telf, bi, gps)
            session['user_e']=nome_e          
            return redirect(url_for("app_eleitor"))     
            
        except:
            return redirect("/")
            
    return render_template("eleitor.html")


@FRONTEND.route("/votar/<candidato_id>", methods=["POST"])
def votar(candidato_id):
    if "user_e" not in session:
        abort(403)  # Proibir acesso se o usuário não estiver logado

    sy = Voto()
    sy.votar(nome_e, candidato_id)

    flash("Voto registrado com sucesso!", "success")
    return redirect(url_for("home"))
@FRONTEND.route("/sair")
def logout():
    if ("user" in session):
        session.pop('user')
        redirect("/candidato")
    return redirect("/")
    
    



    

