# Thierry Bot
Le bot original ne fonctionne plus donc voici un fork avec un beau readme sur comment le faire fonctionner.

J'ai effectué quelques corrections et améliorations. Si ce fork vous plaît, n'hésitez pas à mettre une étoile ⭐ sur GitHub.

N'ayant pas pu récupéré les icones d'origine, j'ai remplacé l'utilisation d'emoji customs par du texte. C'est moins joli mais ça fonctionne partout.

De plus, j'ai ajouté un serveur web pour que l'app puisse tourner en continu et être déployée sur Render.

## Commandes
  - `;help` Affiche l'aide.
  - `;start difficulty` Démarre une partie de Motus. Le paramètre `difficulty` peut prendre les valeurs:
    - `easy`
    - `medium`
    - `hard`
  - `;stop` Arrête la partie.

## Installation et déploiement sur Render

### Fork
- Créer un Fork de ce repository sur GitHub

### Créer un bot sur Discord

- Aller sur https://discord.com/developers/applications
- Nouvelle application : Nom, icone, description tags à définir et valider
- Dans "OAuh2", cliquer sur "Reset Secret" pour obtenir une clé. La conserver.
- Le restant peut être modifié à loisir ("Rich Presence"...)

### Déploiement sur Render
Render propose une offre gratuite suffisante pour héberger le bot pour une installation sur un serveur discord.

  - Aller sur https://render.com
  - Créer un compte
  - Créer un web service
  - Le connecter au repository GitHub du fork
  - Dans "Environment variables", définir:
    - `DISCORD_TOKEN`: La clé obtenue précédemment
    - `PYTHON_VERSION`: 3.10.4
  - Build command: `pip install -r requirements.txt`
  - Start command: `python3 src/main.py`
  - Le build et le déploiement doit s'effectuer automatiquement

## Test du bot
  - Retourner sur la configuration de l'application sur Discord et aller dans "OAuth2 URL Generator"
  - Dans "Scopes", cocher `bot`
  - Dans "Bot Permission", cocher
    - General:
      - Change Nickname
    - Text permissions:
      - Send Messages
      - Create Public Threads
      - Create Private Threads
      - Send messages in Threads
      - Manage Messages
      - Manage Threads
      - Embed Links
      - Attach Files
      - Read Message History
      - Mention Everyone
      - Use External Emojis
      - Use External Stickers
      - Add Reactions
      - Use Slack Commands
  - Copier l'url générée, l'ouvrir et inviter le bot
  - Bon amusement !


