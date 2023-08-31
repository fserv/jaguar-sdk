
JAR=$HOME/jaguar/lib/jaguar-jdbc-2.1.jar

mvn install:install-file -Dfile=$JAR -DgroupId=com.jaguardb -DartifactId=jaguar-jdbc -Dversion=2.1 -Dpackaging=jar
