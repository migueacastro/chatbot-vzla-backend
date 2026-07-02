from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from communications.models import Conversation, Message

class ChatService:
    @staticmethod
    def get_or_create_conversation(phone_number, channel='WHATSAPP', case=None):
        """
        Obtiene una conversación existente o crea una nueva para el canal y número de teléfono.
        """
        conversation, created = Conversation.objects.get_or_create(
            phone_number=phone_number,
            channel=channel,
            defaults={'case': case}
        )
        return conversation

    @staticmethod
    def add_message(conversation, sender, message, twilio_sid=None):
        """
        Crea un mensaje en la base de datos y lo transmite por WebSocket en tiempo real.
        """
        msg = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message=message,
            twilio_sid=twilio_sid
        )

        # Transmitir en tiempo real usando Django Channels
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f"chat_{conversation.id}",
                {
                    "type": "chat_message",
                    "id": msg.id,
                    "message": msg.message,
                    "sender": msg.sender,
                    "created_at": msg.created_at.isoformat()
                }
            )
        return msg

    @classmethod
    def add_message_by_id(cls, conversation_id, sender, message, twilio_sid=None):
        """
        Busca la conversación por ID y agrega el mensaje.
        """
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            return cls.add_message(conversation, sender, message, twilio_sid)
        except Conversation.DoesNotExist:
            raise ValueError(f"La conversación con ID {conversation_id} no existe.")
