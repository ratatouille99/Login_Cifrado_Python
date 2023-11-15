import mysql.connector 
 
class Registro_usuarios():

    def __init__(self):
        self.conexion = mysql.connector.connect( host='localhost',
                                            database ='usuarios', 
                                            user = 'root',
                                            password ='')

    def estudiante(self,usuario, password, aula, salt):
        try:
            cur = self.conexion.cursor()
            sql='''INSERT INTO estudiantes VALUES('{}','{}','{}','{}')'''.format(usuario,password,aula, salt)
            cur.execute(sql)
            self.conexion.commit()    
            cur.close()
                                   
            return True
        
        except:
            return False
    
    def maestro(self,usuario, password, aula, salt):
        try:
            cur = self.conexion.cursor()
            sql='''INSERT INTO maestros VALUES('{}','{}','{}','{}')'''.format(usuario,password,aula, salt)
            cur.execute(sql)
            self.conexion.commit()    
            cur.close()
            
            return True
        
        except:
            return False
    
    def obtener_salt_est(self, usuario):
        result = None
        cur = self.conexion.cursor()
        sql = "SELECT salt FROM estudiantes WHERE u_estudiante = %s"
        cur.execute(sql, (usuario,))
        result = cur.fetchone()
        cur.close()

        if result:
            return result[0]
        else:
            return None
            
    def obtener_salt_ma(self, usuario):
            result = None
            cur = self.conexion.cursor()
            sql = "SELECT salt FROM maestros WHERE n_usuario = %s"
            cur.execute(sql, (usuario,))
            result = cur.fetchone()
            cur.close()

            if result:
                return result[0]
            else:
                return None

        
    def sesion_est(self, usuario, password):
        result = None
        cur = self.conexion.cursor()
        sql = "SELECT aula FROM estudiantes WHERE u_estudiante = %s AND p_estudiante = %s"
        cur.execute(sql, (usuario, password))
        result = cur.fetchone()
        cur.close()

        if result:
            return True, result[0], "Estudiante"
        elif result is None:
            return False, None, None

    def sesion_ma(self, usuario, password):
        result = None
        cur = self.conexion.cursor()
        sql = "SELECT aul FROM maestros WHERE n_usuario = %s AND n_pass = %s"
        cur.execute(sql, (usuario, password))
        result = cur.fetchone()
        cur.close()

        if result:
            return True, result[0], "Maestro"
        elif result is None:
            return False, None, None