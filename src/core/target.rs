use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
#[serde(tag = "type", content = "config", rename_all = "snake_case")]
pub enum Target {
    File(FileTarget),
    Postgres(PostgresTarget),
}


// ------------------------------------------------------------------


#[derive(Debug, Deserialize, Serialize)]
#[serde(tag = "type", content = "config", rename_all = "snake_case")]
pub enum FileTarget {
    Normal(FileJustTarget),
    Container(FileContainerTarget),
}

#[derive(Debug, Deserialize, Serialize)]
pub struct FileJustTarget {
    path:String
}

#[derive(Debug, Deserialize, Serialize)]
pub struct FileContainerTarget {
    container_name:String,
    stop_on_backup:bool,
    path:String
}


impl FileJustTarget{
    pub fn new(path:String,) -> Self {
        Self {
            path,
        }
    }
}
impl FileContainerTarget{
    pub fn new(container_name:String,stop_on_backup:bool,path:String,) -> Self {
        Self {
            container_name,
            stop_on_backup,
            path,
        }
    }
}


// ------------------------------------------------------------------


#[derive(Debug, Deserialize, Serialize)]
#[serde(tag = "type", content = "config", rename_all = "snake_case")]
pub enum PostgresTarget {
    Normal(PostgresJustTarget),
    Container(PostgresContainerTarget),
}

#[derive(Debug, Deserialize, Serialize)]
pub struct PostgresJustTarget {}

#[derive(Debug, Deserialize, Serialize)]
pub struct PostgresContainerTarget {
    container_name:String,
    stop_on_backup:bool,
}


impl PostgresJustTarget{
    pub fn new() -> Self {
        Self {
        
        }
    }
}
impl PostgresContainerTarget{
    pub fn new(container_name:String,stop_on_backup:bool,) -> Self {
        Self {
            container_name,
            stop_on_backup,
        }
    }
}

// ------------------------------------------------------------------
