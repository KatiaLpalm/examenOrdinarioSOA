from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from service_alumno import AlumnoService

application = Application(
    [AlumnoService],
    tns='alumno.soap',
    name='AlumnoService',         
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

soap_app = WsgiApplication(application)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    print("Servicio SOAP corriendo en http://localhost:8000/?wsdl")
    server = make_server("0.0.0.0", 8000, soap_app)
    server.serve_forever()
