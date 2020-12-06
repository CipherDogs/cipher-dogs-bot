package cipherdogs

import canoe.api._
import canoe.models.{Chat, Supergroup, Sticker}
import canoe.models.messages.ChatMemberAdded
import canoe.syntax._
import cats.effect.concurrent.Semaphore
import cats.effect.{ExitCode, IO, IOApp, Timer}
import fs2.Stream

import scala.concurrent.duration._

object Main extends IOApp {
  val token: String = scala.util.Properties.envOrElse("TOKEN", "undefined")

  val ruChat: Supergroup = Supergroup(-1001259375319L, None, Some("cyber_russian_community"))
  val enChat: Supergroup = Supergroup(-1001187351352L, None, Some("fuckgoogle"))

  val ruSticker: Sticker = Sticker(
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

  val enSticker: Sticker = Sticker(
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
          Bot.polling[IO].follow(start(sem), chatID(sem), greeting(sem))
        }
      }
      .compile
      .drain
      .as(ExitCode.Success)

  def start[F[_]: TelegramClient](semaphore: Semaphore[F]): Scenario[F, Unit] =
    for {
      chat <- Scenario.expect(command("start").chat)
      _    <- Scenario.eval(chat.send("CipherDogsBot\nFuck Google! Fuck Twitter! Fuck Web2.0\nhttps://cipherdogs.net/"))
    } yield ()

  def chatID[F[_]: TelegramClient](semaphore: Semaphore[F]): Scenario[F, Unit] =
    for {
      chat <- Scenario.expect(command("chatid").chat)
      _    <- Scenario.eval(chat.send(s"Chat ID: ${chat.id}"))
    } yield ()

  def greeting[F[_]: TelegramClient](semaphore: Semaphore[F]): Scenario[F, Unit] =
    for {
      msg <- Scenario.expect(any)
      _ <- msg match {
        case _: ChatMemberAdded =>
          msg.chat match {
            case Supergroup(_, _, username) if username.contains("cyber_russian_community") => Scenario.eval(msg.chat.send(ruSticker))
            case Supergroup(_, _, username) if username.contains("fuckgoogle")              => Scenario.eval(msg.chat.send(enSticker))
          }
        case _ => Scenario.pure[F](msg)
      }
    } yield ()

  def statistics[F[_]: TelegramClient: Timer](semaphore: Semaphore[F], chat: Chat): Scenario[F, Unit] = chat match {
    case Supergroup(_, _, username) if username.contains("cyber_russian_community") || username.contains("fuckgoogle") =>
      for {
        _ <- Scenario.eval(chat.send(s"Statistics"))
        _ <- Scenario.eval(Timer[F].sleep(4.hours)) >> statistics(semaphore, chat)
      } yield ()
  }
}
