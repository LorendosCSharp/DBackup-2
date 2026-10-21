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
pub struct FileJustTarget {}

#[derive(Debug, Deserialize, Serialize)]
pub struct FileContainerTarget {}


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
pub struct PostgresContainerTarget {}


// ------------------------------------------------------------------