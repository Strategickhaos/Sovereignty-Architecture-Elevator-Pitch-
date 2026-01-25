import java.util.Scanner;

public class LabProgram {
   public static void main(String[] args) {
      Scanner scnr = new Scanner(System.in);
      String userText = scnr.nextLine();
      int count = 0;
      for (int i = 0; i < userText.length(); i++) {
         char c = userText.charAt(i);
         if (c != ' ' && c != '.' && c != '!' && c != ',') {
            count++;
         }
      }
      System.out.println(count);
   }
}
