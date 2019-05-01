import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Scanner;

public class Main {

  public static void verifySolution(String originalMsg, String forgedMsg, String payload) {
    Split forgedMsgSplit = new Split(forgedMsg);
    String payloadedMsg = forgedMsgSplit.preamble+"---"+payload+"---"+forgedMsgSplit.body;
    Hash hashOriginal = new Hash(originalMsg);
    Hash hashPayloadedMsg = new Hash(payloadedMsg);
    if (!hashOriginal.equals(hashPayloadedMsg)) {
      throw new RuntimeException(hashOriginal+"!="+hashPayloadedMsg);
    }
  }

  public static void main(String[] args) {
    Scanner in = new Scanner(System.in, "ISO_8859_1");
    int N = in.nextInt();
    for (int i = 1; i <= N; ++i) {
      int M = in.nextInt(); in.nextLine();
      StringBuilder originalMsg = new StringBuilder();
      for (int j = 0; j < M; ++j)
        originalMsg.append(in.nextLine());
      int L = in.nextInt(); in.nextLine();
      StringBuilder forgedMsg = new StringBuilder();
      for (int j = 0; j < L; ++j)
        forgedMsg.append(in.nextLine());
      Algorithm alg = new Algorithm(originalMsg.toString(), forgedMsg.toString());
      String payload = alg.findForgedPrinterConfig();
      verifySolution(originalMsg.toString(), forgedMsg.toString(), payload);
      System.out.format("Case #%d: %s\n", i, alg.findForgedPrinterConfig());
    }
  }

}

class Hash implements Cloneable {

  public Hash() {
    hash = new int[16];
    Arrays.fill(hash, 0);
  }

  public Hash(String text, int offset) {
    this();
    byte[] textBytes = text.getBytes(StandardCharsets.ISO_8859_1);
    for (int i = 0; i < textBytes.length; ++i)
      hash[(offset+i)%16] = (hash[(offset+i)%16] + textBytes[i])%256;
  }

  public Hash(String text) {
    this(text,0);
  }

  public Hash add(Hash other) {
    Hash result = new Hash();
    for (int i = 0; i < 16; ++i)
      result.hash[i] = ( hash[i] + other.hash[i] )%256;
    return result;
  }

  public Hash subtract(Hash other) {
    Hash result = new Hash();
    for (int i = 0; i < 16; ++i)
      result.hash[i] = ( hash[i] - other.hash[i] + 256 )%256;
    return result;
  }

  int get(int index) {
    return hash[index];
  }

  @Override
  public String toString() {
    return Arrays.toString(hash);
  }

  @Override
  public boolean equals(Object other) {
    if (!(other instanceof Hash))
      return false;
    Hash otherCasted = (Hash)other;
    return Arrays.equals(hash, otherCasted.hash);
  }

  // it's less distracting to deal with non-negative integers
  private int[] hash;
}

class Split {
  Split(String message) {
    int indexEndOfPreamble = message.indexOf("---");
    int indexBeginOfBody = indexEndOfPreamble + 6;
    preamble = message.substring(0, indexEndOfPreamble);
    body = message.substring(indexBeginOfBody);
  }
  public final String preamble;
  public final String body;
}


class ArraySlice {
  public ArraySlice(int[] baseTable, int begin, int end, int step) {
    this.baseTable = baseTable;
    this.begin = begin;
    this.end = end;
    this.step = step;
  }

  public int length() {
    return (end - begin + step - 1)/step;
  }

  public int get(int index) {
    return baseTable[getBaseIndex(index)];
  }

  public void set(int index, int value) {
    baseTable[getBaseIndex(index)] = value;
  }

  private int getBaseIndex(int index) {
    int baseIndex = begin + step*index;
    if (baseIndex >= end)
      throw new IndexOutOfBoundsException();
    return baseIndex;
  }

  private int[] baseTable;
  private int begin;
  private int end;
  private int step;

}

class Algorithm {

  public Algorithm(String originalMsg, String forgedMsg) {
    Hash hashOriginal = new Hash(originalMsg);
    Hash hashForged = new Hash(forgedMsg);
    Split forgedMsgSplit = new Split(forgedMsg);
    offsetPrinterConfig = forgedMsgSplit.preamble.length() + 3;
    Hash hashForgedHead = new Hash(forgedMsgSplit.preamble+"---");
    targetHash = new Hash[16];
    for (int i = 0; i < 16; ++i) {
      int offset = 3 + i + forgedMsgSplit.preamble.length();
      Hash hashForgedTail = new Hash("---"+forgedMsgSplit.body, offset);
      targetHash[i] = hashOriginal.subtract(hashForgedHead.add(hashForgedTail));
    }
  }

  private boolean forceSumToTarget(ArraySlice elements, int target) {
    int inc = ( (target-48*elements.length())%256 + 256 )%256;
    if (inc <= 74*elements.length()) {
      int i = elements.length() - 1;
      while (inc > 0) {
        int addThis = inc <= 74? inc : 74;
        inc -= addThis;
        elements.set(i, 48+addThis);
        i -= 1;
      }
      return true;
    }
    return false;
  }

  public String findForgedPrinterConfig() {
    // with a code of length 64 we can match pretty much every hash
    byte[] foundCode = null;
    for (int codeLength = 0; codeLength<=64 & foundCode==null; ++codeLength) {
      int[] code = new int[codeLength];
      Arrays.fill(code, 48);
      Hash targetForThisCodeLength = targetHash[codeLength%16];
      boolean fail = false;
      for (int i = 0; i < 16 & !fail; ++i) {
        ArraySlice itemsMappedToI = new ArraySlice(code, ( (i-offsetPrinterConfig)%16 + 16 )%16, codeLength, 16);
        if (!forceSumToTarget(itemsMappedToI, targetForThisCodeLength.get(i)))
          fail = true;
      }
      if (!fail) {
        foundCode = new byte[codeLength];
        for (int i = 0; i < codeLength; ++i) {
          foundCode[i] = (byte)code[i];
        }
      }
    }
    if (foundCode == null) {
      throw new RuntimeException("This shouldn't happen!");
    }
    String codeStr = new String(foundCode, StandardCharsets.ISO_8859_1);
    return codeStr;
  }

  int offsetPrinterConfig;
  // target hash of the printer configuration for different payload lengths modulo 16
  Hash[] targetHash;
}

