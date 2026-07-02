import logging
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from communications.services import ChatService

logger = logging.getLogger("twilio_whatsapp")

class TwilioWebhookView(APIView):
    """
    APIView de Django REST Framework para recibir mensajes entrantes de WhatsApp vía Twilio.
    Valida la firma de seguridad X-Twilio-Signature, persiste la conversación y los mensajes,
    y responde usando TwiML con un mensaje echo de retorno.
    """
    permission_classes = []  # El webhook es público; la seguridad se maneja mediante X-Twilio-Signature

    def post(self, request, *args, **kwargs):
        # 1. Extraer los datos enviados por Twilio
        from_number = request.data.get('From', '')
        body_text = request.data.get('Body', '')
        message_sid = request.data.get('MessageSid', '')

        # 2. Validar firma de Twilio si está activo en la configuración
        validate_sig = os.environ.get("VALIDATE_TWILIO_SIGNATURE", "true").lower() in ("1", "true", "yes")
        if validate_sig:
            auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
            if not auth_token:
                logger.error("VALIDATE_TWILIO_SIGNATURE está activo pero TWILIO_AUTH_TOKEN no está definido.")
                return Response("Configuración de firma incompleta", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            validator = RequestValidator(auth_token)
            signature = request.headers.get("X-Twilio-Signature", "")
            
            # Obtener URL absoluta solicitada por Twilio
            url = request.build_absolute_uri()
            
            # Convertir request.POST (QueryDict) a dict estándar para el validador
            params = request.POST.dict()
            
            if not validator.validate(url, params, signature):
                logger.warning("Firma de Twilio inválida detectada y rechazada.")
                return Response("Invalid signature", status=status.HTTP_403_FORBIDDEN)

        logger.info(f"Mensaje entrante de {from_number}: {body_text}")

        # 3. Guardar en base de datos y transmitir en tiempo real mediante ChatService
        try:
            # Obtener o crear la conversación
            conversation = ChatService.get_or_create_conversation(
                phone_number=from_number,
                channel='WHATSAPP'
            )
            
            # Registrar el mensaje entrante (enviado por el familiar/usuario)
            ChatService.add_message(
                conversation=conversation,
                sender='USER',
                message=body_text,
                twilio_sid=message_sid
            )
        except Exception as e:
            logger.error(f"Error procesando mensaje en ChatService: {str(e)}")
            # Continuamos para responder a Twilio de todas formas y evitar reintentos continuos del webhook

        # 4. Generar respuesta inline con TwiML (Echo de prueba)
        twiml = MessagingResponse()
        twiml.message(f"Hello back user, you said: {body_text}")
        
        return HttpResponse(str(twiml), content_type="application/xml")
