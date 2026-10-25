mod core;
use std::fs;

use crate::core::{backup_service::{self, BackupService, serialize_all, trigger_backups}, settings::{self, Settings}};

fn main(){


    let settings:Settings;

    match Settings::read(){
        Ok(_settings)=>{
            settings=_settings;
        }
        Err(error)=>{
            eprintln!("Error while loading settings: {error}");
            return;
        }
    }

    // I need this to create a test backup.yaml I could use later
    // let test_backup_service:BackupService = BackupService::test();
    // let yaml = serde_saphyr::to_string(&test_backup_service).unwrap();
    // fs::write("backup.yaml",yaml);
    let backup_services:Vec<BackupService>;

    match serialize_all(settings.config_path.clone()){
        Ok(services)=>{
            println!("Loaded all services");
            backup_services=services;
        }
        Err(error)=>{
            eprintln!("Error while loading all services: {error}");
            return;
        }
    }
    trigger_backups(&settings, backup_services);

}