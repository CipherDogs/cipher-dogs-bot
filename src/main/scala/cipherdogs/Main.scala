package cipherdogs

import canoe.api._
import canoe.models.messages.{ChatMemberAdded, TelegramMessage}
import canoe.syntax._
import cats.effect.concurrent.Semaphore
import cats.effect.{ExitCode, IO, IOApp}
import cats.syntax.all._
import fs2.Stream

object Main extends IOApp {
  val token: String = scala.util.Properties.envOrElse("TOKEN", "undefined")

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
    case _: ChatMemberAdded => msg.chat.send("CipherDogsBot\nFuck Google! Fuck Twitter! Fuck Web2.0")
    case _                  => msg.chat.send("Nop")
  }
}
