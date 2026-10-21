mod typed;
mod core;
use std::fs;


use crate::{core::serialize::serialize_all, typed::{backup_service::BackupService, settings::{self, Settings}}};

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

    let backup_services:Vec<BackupService>;

    match serialize_all(settings.config_path){
        Ok(services)=>{
            println!("Loaded all services");
            backup_services=services;
        }
        Err(error)=>{
            eprintln!("Error while loading all services: {error}");
            return;
        }
    }
    for service in &backup_services{

        let name = &service.name;
        println!("{name}");
    }

}