


from src.typed.backupDestinations.telegramDestination import TelegramBD, TelegramBDPub




print("Testing tgBackupDestinantion")
pub:TelegramBDPub = TelegramBDPub(
    chatId=1698871291,
    botKeyPath="/home/lorendos/Документы/test.env",
)

bd:TelegramBD = TelegramBD.from_pub(pub)

assert pub.chatId == 1698871291
assert pub.botKeyPath == "/home/lorendos/Документы/test.env"

assert bd.chatId == 1698871291
assert bd.type == "tg"

bd.sendTo("/home/lorendos/Документы/testing/Archive.tar.gz")
    
    
