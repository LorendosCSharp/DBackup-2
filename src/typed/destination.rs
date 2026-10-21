use serde::Deserialize;

#[derive(Debug,Deserialize)]
#[serde(tag="type", rename_all="snake_case")]
enum Destination{
    SSH(SSHDestination),
    Telegram(TelegramDestination)
}

struct TelegramDestination{
    chat_id:i32,
    bot_keypath:String
}

struct SSHDestination{
    user:String,
    ip:String,
    port:i32=22,
    key_path:String,
    remote_directory:String
}

trait DestinationFunctions{

    fn send(&self,path:String);

}


impl DestinationFunctions for TelegramDestination{
    fn send(&self, path:String){
        
    }
}