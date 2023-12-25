from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError



app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


# crear una ruta de envio de email con el servicio SES AWS
@app.route('/sendemail', methods=['POST'])
def send_email():
    
    # obtener los datos del json enviado
    data = request.get_json()
    # obtener los datos del json
    usuario = data['usuario']
    mensaje = data['mensaje']
    correo = data['correo']
    asunto = data['asunto']

    print(usuario, mensaje, correo, asunto)

    # correo del remitente
    SENDER = "miguel.1701929020@ucaldas.edu.co"
    # END: ed8c6549bwf9

    # correo del destinatario
    RECIPIENT = correo

    CONFIGURATION_SET = "ConfigSet"

    # configuracion del servidor de correo
    AWS_REGION = "us-east-1"

    # configuracion del asunto del correo
    SUBJECT = asunto

    # configuracion del cuerpo del correo
    BODY_TEXT = (f"""UrbanNav\r\n
    Hola {usuario},\n
    {mensaje}.\n
    Cordial Saludo,
    """)
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1>UrbanNav</h1>
    <p>Estimado {usuario}</p>
    <p>{mensaje}</p>
    <p>Cordial Saludo,</p>
    </body>
    </html>
                """
    # configuracion del cuerpo del correo
    CHARSET = "UTF-8"


    # configuracion del cliente de ses
    client = boto3.client(
        'ses',
        region_name=AWS_REGION ,
        aws_access_key_id = "AKIAVANUUQ5LB3JTLD5E",
        aws_secret_access_key = "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"  
        )
    
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        return e.response['Error']['Message']
    else:
        return "Email sent! Message ID: " + response['MessageId']

# ruta para enviar sns usando el servicio SMS de AWS
@app.route('/sendsms', methods=['POST'])
def send_sms():
        
        # obtener los datos del json enviado
        data = request.get_json()
        telefono = data['telefono']
        usuario = data['usuario']
        codigo = data['codigo']

        mensaje = "Querido " + usuario + ", su codigo de verificacion es: " + codigo + ". No lo comparta con nadie."

        print(telefono, mensaje)

        numeroInternacional = "+57" + telefono

        print(numeroInternacional)
    
        # configuracion del cliente de sns
        client = boto3.client(
            'sns',
            region_name="us-east-1" ,
            aws_access_key_id = "AKIAVANUUQ5LB3JTLD5E",
            aws_secret_access_key = "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"  
            )
        
        try:
            response = client.publish(
                PhoneNumber=numeroInternacional,
                Message=mensaje,
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': 'MySenderID'
                    },
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
        except ClientError as e:
            return e.response['Error']['Message']
        else:
            return "SMS sent! Message ID: " + response['MessageId']

    

# iniciar el servidor flask
if __name__ == "__main__":
    app.run(debug=True)      