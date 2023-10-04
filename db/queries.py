import sqlite3
from sqlite3 import Error

def crearConexion():
    try:
        con = sqlite3.connect('children.db')
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

def darAlta(data):
    print("Se va a realizar una alta")
    con = crearConexion()
    query = """INSERT INTO childrenData (name, age, gender) VALUES (?,?,?)"""
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
    query = f"""UPDATE childrenData SET name = ?, age = ?, gender = ? WHERE id = {_id}"""
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
    query = """INSERT INTO emociones (nombreEmocion) VALUES (?)"""
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
    query = """SELECT id, nombreEmocion FROM emociones"""
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
    query = """INSERT INTO preguntas (titulo, pregunta) VALUES (?,?)"""
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

def deletePreguntasById(_id):
    con = crearConexion()
    query = f"""DELETE FROM preguntas WHERE id = {_id}"""
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

def actualizarPregunta(_id, data):
    con = crearConexion()
    print("ID que llega al actualizar: " + str(_id))
    query = f"""UPDATE preguntas SET titulo = ?, pregunta = ? WHERE id = {_id}"""
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