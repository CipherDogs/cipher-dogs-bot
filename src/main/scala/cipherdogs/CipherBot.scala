package cipherdogs

import cats.effect.{Sync, Timer}
import telegramium.bots.high._
import telegramium.bots.high.implicits._

class CipherBot[F[_]]()(implicit bot: Api[F], syncF: Sync[F], timer: Timer[F]) extends LongPollBot[F](bot) {

  import cats.syntax.flatMap._
  import cats.syntax.functor._
  import telegramium.bots._
}
