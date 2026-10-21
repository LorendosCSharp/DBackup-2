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

}

impl BackupService {
    pub fn new(name: String,destinations: Vec<Destination>,targets: Vec<Target>,cron: String,include: bool,) -> Self {
        Self {
            name,
            destinations,
            targets,
            cron,
            include,
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
            Target::File(FileTarget::Normal(FileJustTarget::new("/some/path/to/file".into()))),
            Target::File(FileTarget::Container(FileContainerTarget::new("test_file_container".into(),true,"/some/path/to/file/inside/container".into()))),
            Target::Postgres(PostgresTarget::Normal(PostgresJustTarget {})),
            Target::Postgres(PostgresTarget::Container(PostgresContainerTarget::new("test_postgres_container".into(),true))),
        ],
        "0 0 * * *".into(),
        true,
        );
        return service;
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