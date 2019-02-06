package socket1;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class server{
	public static final int port_number = 8088;
	
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		String hostName = "192.168.3.76";
		System.out.println("run");
		ServerSocket socketServer;
		Socket socket;
		InputStream is = null;
		OutputStream os = null;
		socketServer = new ServerSocket(port_number);
		System.out.println("sockect created on " + hostName); 
		socket = socketServer.accept();
		System.out.println("accepted");
		is =  socket.getInputStream();
		os = socket.getOutputStream();
		System.out.println("start listening");
		PrintStream write = new PrintStream(os);
		BufferedReader read = new BufferedReader(new InputStreamReader(is));
		System.out.println(is.read());
		while(true) {
			System.out.println((char)is.read());
		}
	}

}
