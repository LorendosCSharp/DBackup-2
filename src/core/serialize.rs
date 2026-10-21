use crate::typed::{backup_service::BackupService, error::ConfigError};
use std::fs;




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

