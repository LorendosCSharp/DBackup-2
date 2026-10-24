use std::io;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("Failed to read config directory: {0}")]
    DirectoryRead(#[source] io::Error),

    #[error("Failed to read file '{path}': {source}")]
    FileRead {
        path: String,
        #[source]
        source: io::Error,
    },

    #[error("Failed to parse YAML in '{path}': {message}")]
    YamlParse {
        path: String,
        message: String,
    },
}