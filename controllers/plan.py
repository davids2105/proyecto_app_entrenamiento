from flask import Blueprint, request , jsonify
from openai import OpenAI
from datetime import date, timedelta
from dotenv import load_dotenv

import os
import json
import utils.db as db


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


plan = Blueprint("plan",__name__)


@plan.route("/plan/<int:cod_plan>",methods=["GET"])
def read_plan(cod_plan):
    try:
        conn = db.conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM plan WHERE cod_plan = %s", (cod_plan,))
        return cursor.fetchall()
    except Exception as e:
        return {"error":str(e)},500

def crear_plan(datos_user):
    startdate = date.today()
    enddate = startdate + timedelta(days=90)

    prompt = f"""
    Genera un plan de entrenamiento personalizado.
    Datos del usuario:
    - Objetivo: {datos_user['objetivo']}
    - Frecuencia: {datos_user['frecuencia']}
    - Tiempo diario: {datos_user['tiempo']}
    - Nivel: {datos_user['nivel']}
    
    Devuelve la respuesta SOLO en formato JSON con estas claves:
    objective_plan,
    frecuencia,
    actividades_recomendadas,
    tips,
    timeplan
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    contenido = completion.choices[0].message["content"]
    plan_ia = json.loads(contenido)

    conn = db.conexion()
    cursor = conn.cursor()

    sql = """
    INSERT INTO plan (
        objective_plan,
        frecuencia,
        actividades_recomendadas,
        tips,
        cod_rutina,
        timeplan,
        startdate,
        enddate
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        plan_ia["objective_plan"],
        plan_ia["frecuencia"],
        plan_ia["actividades_recomendadas"],
        plan_ia["tips"],
        5,
        plan_ia["timeplan"],
        startdate,
        enddate
    )

    cursor.execute(sql, values)
    conn.commit()

    cod_plan_creado = cursor.lastrowid  

    cursor.close()
    conn.close()

    return cod_plan_creado