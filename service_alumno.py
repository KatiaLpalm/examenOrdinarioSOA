from spyne import ServiceBase, rpc, Integer, Unicode, ComplexModel, Array
from database import get_connection

class AlumnoType(ComplexModel):
    id_alumno = Integer
    matricula = Unicode
    nombre = Unicode
    apellido = Unicode
    carrera = Unicode
    estatus = Unicode


class AlumnoService(ServiceBase):

    # Registrar alumno
    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def registrar_alumno(ctx, matricula, nombre, apellido, carrera, estatus):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO alumno (matricula, nombre, apellido, carrera, estatus)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (matricula, nombre, apellido, carrera, estatus))
        conn.commit()

        cursor.close()
        conn.close()

        return "Alumno registrado correctamente"

    # Consultar alumno por matrícula
    @rpc(Unicode, _returns=AlumnoType)
    def consultar_alumno(ctx, matricula):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_alumno, matricula, nombre, apellido, carrera, estatus
            FROM alumno
            WHERE matricula = %s
        """, (matricula,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return AlumnoType(
                id_alumno=0,
                matricula="NO",
                nombre="NO",
                apellido="NO",
                carrera="NO",
                estatus="NO EXISTE"
            )

        return AlumnoType(
            id_alumno=row[0],
            matricula=row[1],
            nombre=row[2],
            apellido=row[3],
            carrera=row[4],
            estatus=row[5]
        )

    # Eliminar alumno
    @rpc(Unicode, _returns=Unicode)
    def eliminar_alumno(ctx, matricula):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_alumno FROM alumno WHERE matricula=%s", (matricula,))
        existe = cursor.fetchone()

        if not existe:
            return "Alumno no existe"

        cursor.execute("DELETE FROM alumno WHERE matricula=%s", (matricula,))
        conn.commit()

        cursor.close()
        conn.close()

        return "Alumno eliminado"

    # Editar alumno: consultar → eliminar → registrar
    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def editar_alumno(ctx, matricula, nombre, apellido, carrera, estatus):
        # 1. Consultar
        consulta = AlumnoService.consultar_alumno(ctx, matricula)
        if consulta.matricula == "NO":
            return "No se puede editar: alumno no existe"

        # 2. Eliminar
        AlumnoService.eliminar_alumno(ctx, matricula)

        # 3. Volver a insertar
        AlumnoService.registrar_alumno(ctx, matricula, nombre, apellido, carrera, estatus)

        return "Alumno editado correctamente"

    @rpc(_returns=Array(AlumnoType))
    def listar_alumnos(ctx):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_alumno, matricula, nombre, apellido, carrera, estatus FROM alumno")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        resultado = []
        for r in rows:
            resultado.append(
                AlumnoType(
                    id_alumno=r[0],
                    matricula=r[1],
                    nombre=r[2],
                    apellido=r[3],
                    carrera=r[4],
                    estatus=r[5]
                )
            )
        return resultado
