import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class RandomSequence {
    public static void main(String[] args) throws IOException {
        FileWriter writer = new FileWriter("java_sequence.txt");
        Random rand = new Random();

        for (int i = 0; i < 1024; i++) {
            writer.write(rand.nextInt(2) + "");
        }

        writer.close();
    }
}
