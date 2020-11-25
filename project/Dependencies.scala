import sbt._

object Dependencies {
  lazy val catsCore = "org.typelevel" %% "cats-core" % "2.1.1"
  lazy val catsEffect = "org.typelevel" %% "cats-effect" % "2.1.4"
  lazy val scalaTest = "org.scalatest" %% "scalatest" % "3.2.2"
  lazy val canoe = "org.augustjune" %% "canoe" % "0.5.1"

  val common = Seq(catsCore, catsEffect, scalaTest, canoe)
}
