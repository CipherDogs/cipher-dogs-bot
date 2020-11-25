import sbt._

object Dependencies {
  lazy val catsCore = "org.typelevel" %% "cats-core" % "2.1.1"
  lazy val catsEffect = "org.typelevel" %% "cats-effect" % "2.1.4"
  lazy val scalaTest = "org.scalatest" %% "scalatest" % "3.2.2"
  lazy val telegramiumCore = "io.github.apimorphism" %% "telegramium-core" % "2.49.0"
  lazy val telegramiumHigh =  "io.github.apimorphism" %% "telegramium-high" % "2.49.0"

  val common = Seq(catsCore, catsEffect, scalaTest, telegramiumCore, telegramiumHigh)
}
