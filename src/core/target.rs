use flate2::{Compression, write::GzEncoder};
use serde::{Deserialize, Serialize};
use tar::Builder;

use crate::core::{error::ConfigError, settings::Settings};
use std::{fs::File,path,path::PathBuf,ffi::OsStr};

pub trait TargetFunction{
    fn archive(&self,settings:&Settings)->Result<path::PathBuf,ConfigError>;
}


#[derive(Debug, Deserialize, Serialize)]
#[serde(tag = "type", content = "config", rename_all = "snake_case")]
pub enum Target {
    File(FileTarget),
    Postgres(PostgresTarget),
}


// ------------------------------------------------------------------


#[derive(Debug, Deserialize, Serialize)]
pub struct FileTarget {
    path:PathBuf,
    is_container:bool,
    container_name:String,
    stop_on_backup:bool,
}

impl FileTarget{
    pub fn new(path:PathBuf,is_container:bool,container_name:String,stop_on_backup:bool)->Self{
        Self {path, is_container, container_name, stop_on_backup }
    }
}

impl Default for FileTarget{
    fn default()->Self{
        Self{
            path:"".into(),
            is_container:false,
            container_name:"".into(),
            stop_on_backup:true,
        }
    }
}

impl TargetFunction for FileTarget {
    fn archive(&self, settings: &Settings) -> Result<path::PathBuf, ConfigError> {
        let source_path = &self.path;
        let mut output_path = settings.archive_path.clone();

        let name = source_path.file_name().ok_or_else(|| {
            // Replace this with an appropriate ConfigError constructor.
            // The source path has no filename.
        }).map_err(|_| ConfigError::NoName { path:source_path.display().to_string(), message: "".into() })?;
    
        output_path.push(name);
    
    

        output_path.set_extension("tar.gz");

        let output = File::create(&output_path).map_err(|source| ConfigError::FileRead {path: output_path.display().to_string(),source,})?;

        let encoder = GzEncoder::new(output, Compression::best());
        let mut archive = Builder::new(encoder);

        archive.follow_symlinks(false);

        if source_path.is_dir(){
            archive.append_dir_all(".", source_path).map_err(|source| ConfigError::FileRead {path: output_path.display().to_string(),source,})?
        }
        else{
            archive.append_path_with_name(source_path,name).map_err(|source| ConfigError::FileRead {path: source_path.display().to_string(),source,})?;

        }
        archive.append_path_with_name(source_path,name).map_err(|source| ConfigError::FileRead {path: source_path.display().to_string(),source,})?;

        let encoder = archive.into_inner().map_err(|source| ConfigError::FileRead {path: output_path.display().to_string(),source,})?;

        // Finish gzip compression.
        encoder.finish().map_err(|source| ConfigError::FileRead {path: output_path.display().to_string(),source,})?;

        Ok(output_path)
    }
}



// ------------------------------------------------------------------


#[derive(Debug, Deserialize, Serialize)]
pub struct PostgresTarget {
    is_container:bool,
    container_name:String,
    stop_on_backup:bool,
}

impl PostgresTarget{
    pub fn new(is_container:bool,container_name:String,stop_on_backup:bool)->Self{
        Self { is_container, container_name, stop_on_backup }
    }
}

impl Default for PostgresTarget{
    fn default()->Self{
        Self{
            is_container:false,
            container_name:"".into(),
            stop_on_backup:true,
        }
    }
}

impl TargetFunction for PostgresTarget{
    fn archive(&self,settings:&Settings)->Result<path::PathBuf,ConfigError> {
        
        if self.is_container{
            let mut path: path::PathBuf = path::PathBuf::new();
            path.push(settings.archive_path.clone());
            path.push(r"test.tar.gz");
            return Ok(path);
        }
        else{


            let mut output_path: path::PathBuf = path::PathBuf::new();
            output_path.push(settings.archive_path.clone());
            output_path.push(r"test.tar.gz");
            let output = File::create(&output_path).map_err(|source| ConfigError::FileRead {path: settings.archive_path.display().to_string(),source,})?;
            let encoder = GzEncoder::new(output, Compression::best());

            let mut archive = Builder::new(encoder);

            archive.follow_symlinks(false);

            let encoder = archive.into_inner().map_err(|source| ConfigError::FileRead {path: settings.archive_path.display().to_string(),source,})?;
            encoder.finish().map_err(|source| ConfigError::FileRead {path: settings.archive_path.display().to_string(),source,})?;
            return Ok(output_path);
        }
    }
}


// ------------------------------------------------------------------


pub fn generate_archive_target(settings: &Settings,target: Target,) -> Result<path::PathBuf, ConfigError> {
    match target {
        Target::File(file_target) => file_target.archive(settings),
        Target::Postgres(postgres_target) => postgres_target.archive(settings),
    }
}