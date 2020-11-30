import Dependencies._

ThisBuild / scalaVersion := "2.13.3"
ThisBuild / version := "0.1.0"
ThisBuild / organization := "net.cipherdogs"
ThisBuild / organizationName := "cipherdogs"
ThisBuild / semanticdbEnabled := true
ThisBuild / semanticdbVersion := scalafixSemanticdb.revision

lazy val root = (project in file("."))
  .settings(
    name := "CipherDogsBot",
    scalacOptions += "-Wunused:imports",
    libraryDependencies ++= common
  )

scalafmtOnCompile := true

// See https://www.scala-sbt.org/1.x/docs/Using-Sonatype.html for instructions on how to publish to Sonatype.
