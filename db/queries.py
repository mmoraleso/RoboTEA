import sqlite3
from sqlite3 import Error
import mysql.connector


def crearConexion():
    try:
        con = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='robotea')
        print("Se conectó correctamente")
        return con
    except Error as error:
        print("Error a la hora de conectarse a la base de datos: " + str(error))

def getAll():
    con = crearConexion()
    query = """SELECT * FROM childrenData"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        children = cursorObj.fetchall()
        print("Se han obtenido todos los niños" )
        return children
    except Error as error:
        print("Error al obtener todo:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

def getById(_id):
    con = crearConexion()
    query = f"""SELECT * FROM childrenData WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        child = cursorObj.fetchone()
        print("Se han obtenido todos los niños")
        return child
    except Error as error:
        print("Error al obtener el niño con id = :" + str(_id) +" Error: "+ str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()
def getEmocionById(_id):
    con = crearConexion()
    query = f"""SELECT nombreEmocion, aprilTag FROM emociones WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        child = cursorObj.fetchone()
        print("Se han obtenido la emocion con id: " + str(_id))
        return child
    except Error as error:
        print("Error al obtener el emocion con id = :" + str(_id) +" Error: "+ str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

def darAlta(data):
    print("Se va a realizar una alta")
    con = crearConexion()
    query = """INSERT INTO childrenData (name, age, gender, tea, discapacidad_intelectual, comunicacion_oral) VALUES (%s,%s,%s,%s,%s,%s)"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query, data)
        con.commit()
        print("Se ha dado de alta a un nuevo niño")
        return True
    except Error as error:
        print("Error al dar de alta :" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

def actualizarDatosNiños(_id, data):
    con = crearConexion()
    print("ID que llega al actualizar: " + str(_id))
    query = f"""UPDATE childrenData SET name = %s, age = %s, gender = %s, tea = %s, discapacidad_intelectual = %s, comunicacion_oral = %s WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        datosquery = (data, _id)
        cursorObj.execute(query, data)
        con.commit()
        print("Se ha dado actualizado el niño con id = " + str(_id))
        return True
    except Error as error:
        print("Error al actualizar:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

def deleteById(_id):
    con = crearConexion()
    query = f"""DELETE FROM childrenData WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        print("Se ha eliminado el niño con id = " + str(_id))
        return True
    except Error as error:
        print("Error al borrar:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

def darAltaEmociones(data):
    print("Se va a realizar una alta")
    con = crearConexion()
    query = """INSERT INTO emociones (nombreEmocion, aprilTag) VALUES (%s,%s)"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query, data)
        con.commit()
        print("Se ha dado de alta a una emoción")
        return True
    except Error as error:
        print("Error al dar de alta :" + str(error) + " una emocion")
    finally:
        if con:
            cursorObj.close()
            con.close()

def getAllEmociones():
    con = crearConexion()
    query = """SELECT id, nombreEmocion, aprilTag FROM emociones"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        children = cursorObj.fetchall()
        print("Se han obtenido todas las emociones" )
        return children
    except Error as error:
        print("Error al obtener todo:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

def deleteEmocionesById(_id):
    con = crearConexion()
    query = f"""DELETE FROM emociones WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        print("Se ha eliminado la emocion con id = " + str(_id))
        return True
    except Error as error:
        print("Error al borrar:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()


def darAltaPregunta(data):
    print("Se va a realizar una alta")
    con = crearConexion()
    query = """INSERT INTO preguntas (titulo, pregunta) VALUES (%s,%s)"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query, data)
        con.commit()
        print("Se ha dado de alta a una pregunta")
        return True
    except Error as error:
        print("Error al dar de alta :" + str(error) + " una pregunta")
    finally:
        if con:
            cursorObj.close()
            con.close()

def getAllPreguntas():
    con = crearConexion()
    query = """SELECT * FROM preguntas"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        children = cursorObj.fetchall()
        print("Se han obtenido todas las preguntas" )
        return children
    except Error as error:
        print("Error al obtener todo:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

def actualizarEmocion(_id, data):
    con = crearConexion()
    print("ID que llega al actualizar: " + str(_id))
    query = f"""UPDATE emociones SET nombreEmocion = %s, aprilTag = %s WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        datosquery = (data, _id)
        cursorObj.execute(query, data)
        con.commit()
        print("Se ha dado actualizado la emocion con id = " + str(_id))
        return True
    except Error as error:
        print("Error al actualizar:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

def deletePreguntasById(_id):
    con = crearConexion()
    query = f"""DELETE FROM preguntas WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        print("Se ha eliminado la pregunta con id = " + str(_id))
        return True
    except Error as error:
        print("Error al borrar:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()
def getPreguntaById(_id):
    con = crearConexion()
    query = f"""SELECT pregunta FROM preguntas WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        pregunta = cursorObj.fetchone()
        print("Se ha obtenido la pregunta con id = " + str(_id))
        return pregunta
    except Error as error:
        print("Error al get Pregunta By Id:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()
def actualizarPregunta(_id, data):
    con = crearConexion()
    print("ID que llega al actualizar: " + str(_id))
    query = f"""UPDATE preguntas SET titulo = %s, pregunta = %s WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        datosquery = (data, _id)
        cursorObj.execute(query, data)
        con.commit()
        print("Se ha dado actualizado la pregunta con id = " + str(_id))
        return True
    except Error as error:
        print("Error al actualizar:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

#HISTORIAS

def getAllHistorias():
    con = crearConexion()
    query = """SELECT id, titulo, historia FROM historias"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        historias = cursorObj.fetchall()
        print("Se han obtenido todos las historias")
        return historias
    except Error as error:
        print("Error al obtener todo:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

def getHistoriasById(_id):
    con = crearConexion()
    query = f"""SELECT * FROM historias WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        historia = cursorObj.fetchone()
        print("Se ha obtenido la historia con id = " + str(_id))
        return historia
    except Error as error:
        print("Error al obtener la historia con id = :" + str(_id) +" Error: "+ str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()
def darAltaHistoria(data):
    print("Se va a realizar una alta")
    con = crearConexion()
    query = """INSERT INTO historias (titulo, historia) VALUES (%s,%s)"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query, data)
        con.commit()
        print("Se ha dado de alta una historia")
        return True
    except Error as error:
        print("Error al dar de alta :" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

def actualizarHistoria(_id, data):
    con = crearConexion()
    print("ID que llega al actualizar: " + str(_id))
    query = f"""UPDATE historias SET titulo = %s, historia = %s WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        datosquery = (data, _id)
        cursorObj.execute(query, data)
        con.commit()
        print("Se ha dado actualizado la historia con id = " + str(_id))
        return True
    except Error as error:
        print("Error al actualizar:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()
def deleteHistoriaById(_id):
    con = crearConexion()
    query = f"""DELETE FROM historias WHERE id = {_id}"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        print("Se ha eliminado la historia con id = " + str(_id))
        return True
    except Error as error:
        print("Error al borrar:" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()

#SESIONES

def darAltaSesion(data):
    print("Se va a realizar el alta de una sesion")
    con = crearConexion()
    query = """INSERT INTO sesiones (id_historia, id_usuario, id_pregunta, id_emocion, puntuacion_usuario, puntuacion_tutor, respuesta_correcta, fecha) VALUES (%s,%s,%s,%s,%s,%s,%s, %s)"""
    try:
        cursorObj = con.cursor()
        cursorObj.execute(query, data)
        con.commit()
        print("Se ha dado de alta una sesion")
        return True
    except Error as error:
        print("Error al dar de alta :" + str(error))
    finally:
        if con:
            cursorObj.close()
            con.close()