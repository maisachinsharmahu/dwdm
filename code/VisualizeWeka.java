import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.JComponent;
import javax.swing.JFrame;
import weka.classifiers.trees.J48;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.gui.treevisualizer.PlaceNode2;
import weka.gui.treevisualizer.TreeVisualizer;
import weka.gui.AttributeVisualizationPanel;
import weka.gui.visualize.MatrixPanel;

public class VisualizeWeka {
    static class PrintTree extends TreeVisualizer {
        PrintTree(String graph) {
            super(null, graph, new PlaceNode2());
            m_BackgroundColor = java.awt.Color.WHITE;
            m_LineColor = java.awt.Color.BLACK;
            m_FontColor = java.awt.Color.BLACK;
        }
    }

    static void save(JComponent c, int w, int h, String file)
            throws Exception {
        JFrame frame = new JFrame("WEKA");
        frame.getContentPane().add(c);
        frame.setSize(w, h);
        frame.setVisible(true);
        Thread.sleep(2500);
        if (c instanceof TreeVisualizer) {
            ((TreeVisualizer) c).fitToScreen();
            Thread.sleep(1500);
        }
        int S = 3;
        BufferedImage img = new BufferedImage(c.getWidth() * S,
            c.getHeight() * S, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.scale(S, S);
        c.paint(g);
        g.dispose();
        ImageIO.write(img, "png", new File(file));
        frame.dispose();
        System.out.println("saved " + file + "  (" + img.getWidth() + " x "
                           + img.getHeight() + ")");
    }

    public static void main(String[] args) throws Exception {
        Instances data = DataSource.read("data/iris.arff");
        data.setClassIndex(data.numAttributes() - 1);

        MatrixPanel matrix = new MatrixPanel();
        matrix.setInstances(data);
        matrix.setPointSize(2);
        save(matrix, 900, 700, "out/exp8_matrix.png");

        for (int i = 0; i < data.numAttributes() - 1; i++) {
            AttributeVisualizationPanel hist =
                new AttributeVisualizationPanel();
            hist.setInstances(data);
            hist.setAttribute(i);
            save(hist, 420, 300, "out/exp8_hist" + (i + 1) + ".png");
        }

        J48 tree = new J48();
        tree.buildClassifier(data);
        TreeVisualizer tv = new PrintTree(tree.graph());
        save(tv, 800, 520, "out/exp8_tree.png");
    }
}
