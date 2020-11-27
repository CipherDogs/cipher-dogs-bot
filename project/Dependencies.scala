import sbt._

object Dependencies {
  lazy val canoe = "org.augustjune" %% "canoe" % "0.5.1"
  lazy val catsCore = "org.typelevel" %% "cats-core" % "2.1.1"
  lazy val catsEffect = "org.typelevel" %% "cats-effect" % "2.1.4"
  lazy val fs2 = "co.fs2" %% "fs2-core" % "2.4.5"
  lazy val scalaTest = "org.scalatest" %% "scalatest" % "3.2.2"

  val common = Seq(canoe, catsCore, catsEffect, fs2, scalaTest)
}
