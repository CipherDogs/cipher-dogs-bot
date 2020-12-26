use futures::StreamExt;
use std::env;
use telegram_bot::*;

#[tokio::main]
async fn main() -> Result<(), Error> {
    let token = env::var("TOKEN").expect("TOKEN not set");
    let api = Api::new(token);

    let mut stream = api.stream();
    while let Some(update) = stream.next().await {
        let update = update?;
        if let UpdateKind::Message(message) = update.kind {
            if let MessageKind::Text { ref data, .. } = message.kind {
                if data.as_str() == "/start" {
                    api.send(message.chat.text("CipherDogsBot\nFuck Google! Fuck Twitter! Fuck Web2.0\nhttps://cipherdogs.net/")).await?;
                } else if data.as_str() == "/hacktheplanet" {
                    api.send(message.chat.text("Hack the planet!")).await?;
                }
            }

            if let MessageKind::NewChatMembers { ref data } = message.kind {}
        }
    }

    Ok(())
}
