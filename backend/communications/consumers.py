import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs'].get('conversation_id')
        self.room_group_name = f"chat_{self.conversation_id}"

        # Unirse al grupo de la conversación
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Recibe mensajes directamente del cliente WebSocket y los guarda usando ChatService.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        sender = text_data_json.get('sender', 'USER')

        # Importar ChatService localmente para evitar importación circular
        from communications.services import ChatService

        # Guardar en base de datos de manera segura y asíncrona
        try:
            msg_obj = await database_sync_to_async(ChatService.add_message_by_id)(
                conversation_id=self.conversation_id,
                sender=sender,
                message=message
            )
            # Nota: add_message ya difunde el mensaje al grupo mediante group_send,
            # por lo tanto, no es estrictamente necesario volver a llamar group_send desde aquí
            # para evitar duplicar el mensaje al emisor si está suscrito al mismo grupo.
        except Exception as e:
            # Enviar mensaje de error al WebSocket del emisor
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))

    async def chat_message(self, event):
        """
        Recibe los eventos difundidos en el grupo y los retransmite al WebSocket.
        """
        await self.send(text_data=json.dumps({
            'id': event.get('id'),
            'message': event.get('message'),
            'sender': event.get('sender'),
            'created_at': event.get('created_at')
        }))
