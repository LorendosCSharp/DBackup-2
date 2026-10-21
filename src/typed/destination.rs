use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
#[serde(tag = "type", content = "config", rename_all = "snake_case")]
pub enum Destination {
    Ssh(SSHDestination),
    Telegram(TelegramDestination),
}

#[derive(Debug, Deserialize, Serialize)]
pub struct TelegramDestination {
    chat_id: i32,
    bot_keypath: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct SSHDestination {
    user: String,
    ip: String,
    port: i32,
    key_path: String,
    remote_directory: String,
}

impl Default for SSHDestination {
    fn default() -> Self {
        Self {
            user: String::new(),
            ip: String::new(),
            port: 22,
            key_path: String::new(),
            remote_directory: String::new(),
        }
    }
}

impl Default for TelegramDestination {
    fn default() -> Self {
        Self {
            chat_id: 0,
            bot_keypath: String::new(),
        }
    }
}