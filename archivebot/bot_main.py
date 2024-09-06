from telethon import TelegramClient, events
import os
import logging

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Vos identifiants API pour votre compte utilisateur
api_id = '29819571'
api_hash = 'c759c02a88286520500989f0d48e5e7f'
phone_number = '+33756827085'  # Remplacez par votre numéro de téléphone avec le code pays

# Initialiser le client avec votre compte utilisateur
client = TelegramClient('user_session', api_id, api_hash)

# Chemin de téléchargement par défaut
download_path = './downloads'

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("Bonjour ! Envoyez-moi le nom ou l'ID du canal pour télécharger les médias. Utilisez /list pour voir les médias téléchargés.")

@client.on(events.NewMessage)
async def handle_message(event):
    message_text = event.message.message

    if message_text.startswith("/"):
        return

    await event.reply(f"Téléchargement des médias à partir de {message_text}...")

    try:
        await download_media_from_entity(message_text)
        await event.reply("Téléchargement terminé. Les médias ont été enregistrés.")
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement : {str(e)}")
        await event.reply(f"Erreur lors du téléchargement : {str(e)}")

async def download_media_from_entity(entity_name_or_id, limit=100):
    """Télécharge les médias d'un groupe ou canal spécifié par son nom ou son ID."""
    logger.info(f"Commence à télécharger les médias de {entity_name_or_id}")
    async for message in client.iter_messages(entity_name_or_id, limit=limit):
        if message.media:
            # Déterminer le type de média et définir le dossier
            media_type = get_media_type(message)
            media_folder = os.path.join(download_path, entity_name_or_id, media_type)
            if not os.path.exists(media_folder):
                os.makedirs(media_folder)

            # Déterminer l'extension de fichier
            file_extension = get_file_extension(message)

            # Télécharger le fichier média
            file_path = os.path.join(media_folder, f"{message.id}{file_extension}")
            await message.download_media(file=file_path)
            logger.info(f"Média téléchargé : {file_path}")

def get_media_type(message):
    """Retourne le type de média en tant que chaîne pour la gestion des dossiers."""
    if message.photo:
        return 'photos'
    elif message.video:
        return 'videos'
    elif message.audio:
        return 'audios'
    elif message.document:
        return 'documents'
    return 'unknown'

def get_file_extension(message):
    """Retourne l'extension de fichier appropriée basée sur le type de média."""
    if message.photo:
        return ".jpg"
    elif message.video:
        return ".mp4"
    elif message.audio:
        return ".mp3"
    elif message.document:
        file_name = message.file.name if message.file else "unknown"
        return f".{file_name.split('.')[-1]}" if '.' in file_name else ".file"
    return ".media"

@client.on(events.NewMessage(pattern='/list'))
async def list_downloads(event):
    """Liste les médias téléchargés."""
    entity_folders = [f for f in os.listdir(download_path) if os.path.isdir(os.path.join(download_path, f))]
    if not entity_folders:
        await event.reply("Aucun média téléchargé pour le moment.")
        return
    
    response = "Médias téléchargés:\n"
    for entity in entity_folders:
        entity_path = os.path.join(download_path, entity)
        for root, _, files in os.walk(entity_path):
            for file in files:
                response += f"{entity}/{file}\n"
    
    await event.reply(response)

def main():
    client.start(phone=phone_number)
    logger.info("Bot démarré et connecté.")
    client.run_until_disconnected()

if __name__ == "__main__":
    main()
