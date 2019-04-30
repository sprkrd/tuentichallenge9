import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Scanner;

class Main {

  public static byte[] notSoComplexHash(String input_text) {
    byte[] hash = new byte[16];
    Arrays.fill(hash, (byte)0);
    byte[] text_bytes = input_text.getBytes(StandardCharsets.ISO_8859_1);
    for (int i = 0; i < text_bytes.length; ++i)
      hash[i%16] = (byte) (hash[i%16] + text_bytes[i]);
    return hash;
  }

  public static String findForgedPrintConfig(String original_msg, String forged_msg) {
    return "not implemented yet";
  }

  public static void main(String[] args) {
    Scanner in = new Scanner(System.in, StandardCharsets.ISO_8859_1);
    int N = in.nextInt();
    for (int i = 1; i <= N; ++i) {
      int M = in.nextInt(); in.nextLine();
      StringBuilder original_msg = new StringBuilder();
      for (int j = 0; j < M; ++j)
        original_msg.append(in.nextLine());
      int L = in.nextInt(); in.nextLine();
      StringBuilder forged_msg = new StringBuilder();
      for (int j = 0; j < L; ++j)
        forged_msg.append(in.nextLine());
      String forged_print_config = findForgedPrintConfig(
          original_msg.toString(), forged_msg.toString());
      System.out.format("Case #%d: %s\n", i, forged_print_config);
    }
  }

}


