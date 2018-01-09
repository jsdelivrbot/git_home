package custom

import scala.io.Source
import scala.io.StdIn.readLine

class fileReader {
  /**Read local file*/
  def read(filename: String): Unit = {
    for (line <- Source.fromFile(filename).getLines) {
      println(line)
    }
  }
}

object Demo {
  def main(args: Array[String]): Unit = {
    val filename = readLine("File:")
    var reader = new fileReader()
    reader.read(filename)
  }
}
