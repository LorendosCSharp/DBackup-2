use serde::Deserialize;
use std::{path::PathBuf,fs};

use crate::core::error::ConfigError;

#[derive(Debug,Deserialize)]
pub struct Settings{
    pub config_path:PathBuf,
    pub archive_path:PathBuf,
}

impl Settings{
    pub fn read()->Result<Self, ConfigError>{
        let settings_raw=fs::read_to_string("settings.yaml").map_err(|source| ConfigError::FileRead{path:"settigns.yaml".into(),source:source},)?;

        let settings: Settings = serde_saphyr::from_str(&settings_raw).map_err(|e| ConfigError::YamlParse { path: "settings.yaml".into(), message:  e.to_string()},)?;
        
        Ok(settings)
    }
}