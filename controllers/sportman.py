from flask import Blueprint, request , jsonify
import utils.db as db

sportman = Blueprint("sportman",__name__)


@sportman.route("/sportman",methods=["POST"])
def create():
    try:
        data = request.get_json()
        conn = db.conexion()
        cursor = conn.cursor()
        sql = "INSERT INTO `sportman`(`id`, `name`,`lastname`, `phone`, `age`, `sex`,`email`) VALUES(%s,%s,%s,%s,%s,%s,%s) "
        cursor.execute(sql,
        (data['id'],
        data['name'],
        data['lastname'],
        data['phone'],
        data['age'],
        data['sex'],
        data['email']))
        conn.commit()
        cursor.close()
        return{"message":"Sportman save"},201
    except Exception as e:
        return {"error":str(e)},500


@sportman.route("/sportman",methods=["GET"])
def read():
    try:
        conn = db.conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from sportman")
        return cursor.fetchall()
    except Exception as e:
        return {"error":str(e)},500
    
    
@sportman.route("/sportman/<int:id>",methods=["PUT"])
def update(id):
    try:
        conn = db.conexion()
        cursor = conn.cursor()
        data = request.get_json()
        sql="UPDATE `sportman` SET `name`=%s,`lastname`=%s,`phone`=%s,`age`=%s,`sex`=%s,`email`=%s WHERE id =%s "
        cursor.execute(sql,(data['name'],
        data['phone'],
        data['lastname'],
        data['age'],
        data['sex'],
        data['email'],
        id))
        conn.commit()
        return {"Message":"Deportista Actualizado"},200
    except Exception as e:
        return {"error":str(e)},500

@sportman.route("/sportman/<int:id>",methods=["DELETE"])
def delete(id):
        try:
            conn = db.conexion()
            cursor = conn.cursor()
            sql ="Delete FROM `sportman` WHERE id = %s"
            cursor.execute(sql,(id,))
            conn.commit()
            return {"Message":"Deportista Eliminado"},200
        except Exception as e:
            return {"error":str(e)},500