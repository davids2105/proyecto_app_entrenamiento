from flask import Blueprint, request , jsonify
import utils.db as db
import utils.funciones as func 
""" from controllers import plan as p """


evaluation = Blueprint("evaluation",__name__)

@evaluation.route("/evaluation", methods=["POST"])
def create():
    try:
        data = request.get_json()

        # Validaciones mínimas
        required = ["documento", "peso", "altura", "nivel_actividad", "objetivo",
                    "diasdispon", "tiempodisponible", "descripcion", "coach", "date"]

        for field in required:
            if field not in data:
                return {"error": f"Falta el campo requerido: {field}"}, 400

        documento = data["documento"]
        peso      = data["peso"]
        altura    = data["altura"]

        # Obtener datos del deportista
        edad, sexo = traeDatosSportam(documento)
      

        if not edad or not sexo:
            return {"error": "El deportista no existe o faltan datos."}, 404

        # Cálculos
        imc, clasific_imc = func.calular_imc(peso, altura)
        grasa_corporal    = func.grasa_corporal(imc, edad, sexo)
        tmb               = func.calcular_tmb(peso, altura, edad, sexo)
        calorias_manten   = func.calorias_mantenimiento(tmb, data["nivel_actividad"])
        obj_calorico      = func.calorias_objetivo(calorias_manten, data["objetivo"])
        pesomin, pesomax  = func.peso_saludable(altura)
        
        """         imc = 154
        clasific_imc = "Sobrepeso"
        grasa_corporal = 400
        tmb = 150
        calorias_manten=2500
        obj_calorico = 2500
        pesomin = 84
        pesomax = 90 """

        # Crear plan
        datos_plan = {
            "objetivo": data["objetivo"],
            "frecuencia": f"{data['diasdispon']} veces por semana",
            "tiempo": data["tiempodisponible"],
            "nivel": data["nivel_actividad"],
        }

        #cod_plan = p.crear_plan(datos_plan) 
        cod_plan = 1;
   

        # Insert en BD
        conn = db.conexion()
        cursor = conn.cursor()

        sql = """
        INSERT INTO assessment(
            descripcion, weigth, heigtht, imc, date, activitylevel,
            objetive, daysavailable, availabletime, bmiclassification,
            bodyfat, Tmb, `maintenance_calories`, id_sportman,
            id_coach, `target_calories`, `ideal_weight_min`,
            `ideal_weight_max`, cod_plan
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(sql, (
            data["descripcion"],
            peso,
            altura,
            imc,
            data["date"],
            data["nivel_actividad"],
            data["objetivo"],
            data["diasdispon"],
            data["tiempodisponible"],
            clasific_imc,
            grasa_corporal,
            tmb,
            calorias_manten,
            documento,
            data["coach"],
            obj_calorico,
            pesomin,
            pesomax,
            cod_plan
        ))

        conn.commit()
        cursor.close()

        return {"message": "Evaluation saved"}, 201

    except Exception as e:
        return {"error": str(e)}, 500




""" @evaluation.route("/evaluation1",methods=["POST"])
def create1():
    try:
        data = request.get_json()
        documento = data['documento']
        peso, altura = data['peso'],data['altura']
        edad, sexo = traeDatosSportam(documento)
        imc,clasific_imc = func.calular_imc(peso,altura)
        grasa_corporal = func.grasa_corporal(imc,edad,sexo)
        tmb =  func.calcular_tmb(peso,altura,edad,sexo)
        calorias_manten =  func.calorias_mantenimiento(tmb,data['nivel_actividad'])
        obj_calorico =  func.calorias_objetivo(calorias_manten,data['objetivo'])
        pesomin,pesomax = func.peso_saludable(altura)
        
        datos = {
            "objetivo": data['objetivo'],
            "frecuencia": data['diasdispon'] +" veces por semana",
            "tiempo": data['tiempodisponible'],
            "nivel": data['nivel_actividad'],
                  
        }
        cod_plan =  p.crear_plan(datos)
        
        
        conn = db.conexion()
        cursor = conn.cursor()
        sql = "INSERT INTO `assessment`( `descripcion`, `weigth`, `heigtht`, `imc`, `date`, `activitylevel`, `objetive`, `daysavailable`, `availabletime`, `bmiclassification`, `bodyfat`, `Tmb`, `maintenance_calories`, `id_sportman`, `id_coach`, `target_calories`, `ideal_weight_min`, `ideal_weight_max`, `cod_plan`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,
        (data['descripcion'],
        data['peso'],
        data['altura'],
        imc,
        data['date'],
        data['nivel_actividad'],
        data['objetivo'],
        data['diasdispon'],
        data['tiempodisponible'],
        clasific_imc,
        grasa_corporal,
        tmb,
        calorias_manten,
        documento,
        data['coach'],
        obj_calorico,
        pesomin,
        pesomax,
        cod_plan
        
        ))
        conn.commit()
        cursor.close()
        return{"message":"Evaluation save"},201
    except Exception as e:
        return {"error":str(e)},500 """

def traeDatosSportam(id):
    try:
        conn = db.conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT age, sex FROM sportman where id = %s  ",(id,))
        row = cursor.fetchone()
        age = row["age"]
        sex = row["sex"]
        return age, sex
    except Exception as e:
        raise Exception(f"Error en traeDatosSportam: {str(e)}")

@evaluation.route("/evaluation",methods=["GET"])
def read():
    try:
        conn = db.conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from assessment")
        return cursor.fetchall()
    except Exception as e:
        return {"error":str(e)},500
    
    
