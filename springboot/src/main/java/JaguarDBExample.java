

import java.io.*;
import java.sql.DatabaseMetaData;
import java.sql.PreparedStatement;
import javax.sql.DataSource;
import java.sql.SQLException;
import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.DriverManager;
import java.util.Random;

import com.jaguar.jdbc.JaguarDriver;
import com.jaguar.jdbc.JaguarDataSource;
import com.jaguar.jdbc.JaguarStatement;
import com.jaguar.jdbc.JaguarPreparedStatement;
import com.jaguar.jdbc.JaguarResultSetMetaData;

import org.springframework.boot.*;
import org.springframework.boot.autoconfigure.*;
import org.springframework.stereotype.*;
import org.springframework.web.bind.annotation.*;


@RestController
@EnableAutoConfiguration
public class JaguarDBExample {

    @RequestMapping("/")
    String home() {
        return "Hello World from JaguarDB SprintBoot!";
    }

    @RequestMapping("/create")
    String create() {
        try {
            Statement statement = connection_.createStatement();
            statement.executeUpdate("create table if not exists boot123 ( key: uid uuid, value: addr char(32));" );
        } catch (SQLException e ) {
            return "create table exception";
        }
        
        return "Created table boot123 key: uid uuid, value: addr char(32)";
    }

    @RequestMapping("/insert")
    String insert() {
        StringBuffer sb = new StringBuffer();

        try {
            JaguarStatement jst;
            Statement statement = connection_.createStatement();
            statement.executeUpdate("insert into boot123 (addr ) values ( 'v1000')");
            jst = (JaguarStatement)statement;

            sb.append( jst.getLastUuid() + "<br>");

            statement.executeUpdate("insert into boot123 (addr ) values ( 'v2000')");
            jst = (JaguarStatement)statement;
            sb.append( jst.getLastUuid() + "<br>");

            statement.executeUpdate("insert into boot123 (addr ) values ( 'v3000')");
            jst = (JaguarStatement)statement;
            sb.append( jst.getLastUuid() + "<br>");

        } catch ( SQLException e ) {
            return "insert into table exception";
        }

        sb.append("<br>Inserted records into table boot123");
        return sb.toString();
    }

    @RequestMapping("/select")
    String select() {
        ResultSet rs;

        try {
            Statement statement = connection_.createStatement();
            rs = statement.executeQuery("select * from boot123");
        } catch ( SQLException e ) {
            return "select exception";
        }

        String key, val;
        StringBuffer sb = new StringBuffer();

        try {
            while(rs.next()) {
                key = rs.getString("uid");
                val = rs.getString("addr");

                sb.append( key );
                sb.append( ":" );
                sb.append( val );
                sb.append( "<br>" );
            }
        } catch ( SQLException e ) {
            return "select next() exception";
        }
    
        String hdr = "select result:<br><br>";
        String ret = hdr + sb.toString();
        return ret;
    }

    @RequestMapping("/drop")
    String drop() {
        try {
            Statement statement = connection_.createStatement();
            statement.executeUpdate("drop table if exists boot123");
        } catch (  SQLException e ) {
            return "drop exception";
        }

        return "Table boot123 is dropped";
    }


    public static void main(String[] args) throws Exception {
        System.loadLibrary("JaguarClient");

        ds_ = new JaguarDataSource( "127.0.0.1", 8888, "test");
        connection_ = ds_.getConnection("admin", "jaguarjaguarjaguar");

        SpringApplication.run(JaguarDBExample.class, args);
    }

    static private DataSource ds_;
    static private Connection connection_;

}
