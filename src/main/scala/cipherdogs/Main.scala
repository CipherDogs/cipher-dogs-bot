package cipherdogs

import canoe.api._
import canoe.models.{Chat, Supergroup, Sticker}
import canoe.models.messages.{ChatMemberAdded, TelegramMessage}
import canoe.syntax._
import cats.effect.concurrent.Semaphore
import cats.effect.{ExitCode, IO, IOApp}
import cats.syntax.all._
import fs2.Stream

object Main extends IOApp {
  val token: String = scala.util.Properties.envOrElse("TOKEN", "undefined")

  val cyberRussianCommunity: Sticker = Sticker(
    "CAACAgIAAxkBAAJAXV-ZAjfq6sotbN3e5_Nc-NMc3RWlAAJWAQACK9RLC9RAtYotQ8NPGwQ",
    "CAACAgIAAxkBAAJAXV-ZAjfq6sotbN3e5_Nc-NMc3RWlAAJWAQACK9RLC9RAtYotQ8NPGwQ",
    0,
    0,
    false,
    None,
    None,
    None,
    None,
    None,
  )

  val fuckgoogle: Sticker = Sticker(
    "CAACAgIAAxkBAAJAhl-ZZlpBtcyICOlr_VyWthXoch_7AAIYAQACK9RLC7eumetzzfY-GwQ",
    "CAACAgIAAxkBAAJAhl-ZZlpBtcyICOlr_VyWthXoch_7AAIYAQACK9RLC7eumetzzfY-GwQ",
    0,
    0,
    false,
    None,
    None,
    None,
    None,
    None,
  )

  def run(args: List[String]): IO[ExitCode] =
    Stream
      .resource(TelegramClient.global[IO](token))
      .flatMap { implicit client =>
        Stream.eval(Semaphore[IO](0)).flatMap { sem =>
          Bot.polling[IO].follow(start(sem), greeting(sem))
        }
      }
      .compile
      .drain
      .as(ExitCode.Success)

  def start[F[_]: TelegramClient](semaphore: Semaphore[F]): Scenario[F, Unit] =
    for {
      chat <- Scenario.expect(command("start").chat)
      _    <- Scenario.eval(chat.send("CipherDogsBot\nFuck Google! Fuck Twitter! Fuck Web2.0"))
    } yield ()

  def greeting[F[_]: TelegramClient](semaphore: Semaphore[F]): Scenario[F, Unit] =
    for {
      msg <- Scenario.expect(any)
      _   <- Scenario.eval(greetingBack(msg))
    } yield ()

  def greetingBack[F[_]: TelegramClient](msg: TelegramMessage): F[_] = msg match {
    case _: ChatMemberAdded =>
      msg.chat match {
        case Supergroup(_, _, username) if username.contains("cyber_russian_community") => msg.chat.send(cyberRussianCommunity)
        case Supergroup(_, _, username) if username.contains("fuckgoogle")              => msg.chat.send(fuckgoogle)
      }
    case _ => msg.chat.send("Nop")
  }

  def statistics[F[_]: TelegramClient](chat: Chat, message: String): Scenario[F, Unit] =
    for {
      _ <- Scenario.eval(chat.send(message))
    } yield ()
}
