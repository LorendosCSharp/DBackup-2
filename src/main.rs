
use serde::Deserialize;


#[derive(Debug, Deserialize)]
struct Config {
    name: String,
    enabled: bool,
    retries: i32
}

fn main() {
    println!("Hello, world!");
}
