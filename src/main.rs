mod typed;


use typed::backup_service::BackupService;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let service =BackupService::test();
    let service2=BackupService::default();
    let yaml = serde_saphyr::to_string(&service)?;
    let yaml2 = serde_saphyr::to_string(&service2)?;
    std::fs::write("backup.yaml", &yaml)?;

    println!("{yaml}");
    println!("{yaml2}");

    Ok(())
}