use serde::{Deserialize, Serialize};
use crate::core::error::ConfigError;
use std::fs;
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

pub fn serialize_all(path: String,) -> Result<Vec<BackupService>, ConfigError> {
    let mut data: Vec<BackupService> = Vec::new();

    let files = fs::read_dir(&path).map_err(ConfigError::DirectoryRead)?;

    for entry in files {
        // Handle errors while enumerating directory entries.
        let entry = entry.map_err(ConfigError::DirectoryRead)?;
        let file_path = entry.path();

        // Only process YAML files.
        let is_yaml = file_path.extension().is_some_and(|ext| ext == "yaml" || ext == "yml");

        if !file_path.is_file() || !is_yaml {
            continue;
        }

        let data_raw = fs::read_to_string(&file_path).map_err(|source| ConfigError::FileRead {path: file_path.display().to_string(),source,})?;

        let mut yaml: Vec<BackupService> =serde_saphyr::from_str(&data_raw).map_err(|e| ConfigError::YamlParse {path: file_path.display().to_string(),message: e.to_string(),})?;

        data.append(&mut yaml);
    }
    Ok(data)
}

pub fn trigger_backups(backup_services:Vec<BackupService>)/*->Result<String,ConfigError>*/{

    for backup_service in backup_services{
        let service:BackupService = backup_service;
        if !service.include{
            continue;
        }
        for target in service.targets{
        }
        for destination in service.destinations{
            
        }

    }
    //Ok("".into())

}