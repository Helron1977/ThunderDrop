import sqlite3

class TranslationManager:
    translations = {
        'en': {
            'POINTS_MESSAGE': "you have {points} points.",
            'BUY_SUCCESS': "purchased {quantity} {troop_type}(s).",
            'BUY_FAILURE': "you don't have enough points.",
            'INVALID_TROOP_TYPE': "Invalid troop type.",
            'ATTACK_VICTORY': "has defeated",
            'ATTACK_DEFEAT': "was defeated by",
            'DRAW': "It's a draw!",
            'ARMY_STATUS': "Here's the state of your army:\n"
                               "🛡️ Infantry: {infantry}   🏹 Archers: {archer} 🐎 Cavalry: {cavalry}",
            'LANG_SET': "Language set to {language}.",
            'LANG_UNSUPPORTED': "Unsupported language.",
            'HOSPITAL_STATUS': "Here is the status of your wounded troops:\n"
                               "🛡️ Infantry: {wounded_infantry}\n"
                               "🏹 Archers: {wounded_archer}\n"
                               "🐎 Cavalry: {wounded_cavalry}",
            # Ajoutez d'autres traductions ici
        },
        'fr': {
            'POINTS_MESSAGE': "vous avez {points} points.",
            'BUY_SUCCESS': "a acheté {quantity} {troop_type}(s).",
            'BUY_FAILURE': "vous n'avez pas assez de points.",
            'INVALID_TROOP_TYPE': "Type de troupe invalide.",
            'ATTACK_VICTORY': "a vaincu",
            'ATTACK_DEFEAT': "a été vaincu par",
            'DRAW': "Match nul!",
            'ARMY_STATUS': "Voici l'état de votre armée :\n"
                               "🛡️ Infanterie : {infantry}      🏹 Archers : {archer}     🐎 Cavalerie : {cavalry}",
            'LANG_SET': "Langue définie sur {language}.",
            'LANG_UNSUPPORTED': "Langue non supportée.",
            'HOSPITAL_STATUS': "Voici l'état de vos troupes blessées :\n"
                               "🛡️ Infanterie : {wounded_infantry}\n"
                               "🏹 Archers : {wounded_archer}\n"
                               "🐎 Cavalerie : {wounded_cavalry}",
            # Ajoutez d'autres traductions ici
        }
    }


    @staticmethod
    def gettext(user_id, text_key, **kwargs):
        user_language = TranslationManager.get_user_language(user_id)
        template = TranslationManager.translations[user_language].get(text_key, text_key)
        return template.format(**kwargs)

    @staticmethod
    def get_user_language(user_id):
        conn = sqlite3.connect('bot_data.db')
        c = conn.cursor()
        c.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else 'en'
    
    @staticmethod
    def set_user_language(user_id, language):
        conn = sqlite3.connect('bot_data.db')
        c = conn.cursor()

        # Vérifier si l'utilisateur existe déjà
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = c.fetchone()

        if result:
            # Mettre à jour la langue si l'utilisateur existe
            c.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
        else:
            # Insérer un nouvel utilisateur si ce n'est pas le cas
            c.execute('INSERT INTO users (user_id, language) VALUES (?, ?)', (user_id, language))

        conn.commit()
        conn.close()
