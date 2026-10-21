use serde::{Deserialize, Serialize};
use super::destination::{
    Destination, SSHDestination, TelegramDestination,
};
use super::target::{
    Target, FileTarget, FileJustTarget, FileContainerTarget,
    PostgresTarget, PostgresJustTarget, PostgresContainerTarget,
};

#[derive(Debug, Deserialize, Serialize)]
pub struct BackupService {
    pub name: String,
    pub destinations: Vec<Destination>,
    pub targets: Vec<Target>,
    pub cron: String,
    pub include: bool,

    id: String, 
}

impl BackupService {
    pub fn new(name: String,destinations: Vec<Destination>,targets: Vec<Target>,cron: String,include: bool,) -> Self {
        Self {
            name,
            destinations,
            targets,
            cron,
            include,
            id: Self::generate_id(),
        }
    }

    pub fn test()-> BackupService{
        let service = BackupService::new(
        "daily_backup".into(),
        vec![
            Destination::Ssh(SSHDestination::default()),
            Destination::Telegram(TelegramDestination::default()),
        ],
        vec![
            Target::File(FileTarget::Normal(FileJustTarget {})),
            Target::File(FileTarget::Container(FileContainerTarget {})),
            Target::Postgres(PostgresTarget::Normal(PostgresJustTarget {})),
            Target::Postgres(PostgresTarget::Container(PostgresContainerTarget {})),
        ],
        "0 0 * * *".into(),
        true,
        );
        return service;
    }

    fn generate_id() -> String {
        return uuid::Uuid::new_v4().to_string();
    }

    pub fn id(&self) -> &str {
        &self.id
    }
}


impl Default for BackupService{
    fn default() -> Self{
        Self::new(
            "".into(), 
            vec![], 
            vec![],
            "0 0 * * *".into(), 
            true
        )
    }
}