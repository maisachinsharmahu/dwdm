import weka.core.Attribute;
import weka.core.AttributeStats;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

public class IntroWeka {
    public static void main(String[] args) throws Exception {
        Instances data = DataSource.read("data/iris.arff");
        data.setClassIndex(data.numAttributes() - 1);

        System.out.println("Relation   : " + data.relationName());
        System.out.println("Instances  : " + data.numInstances());
        System.out.println("Attributes : " + data.numAttributes());
        System.out.println("Class      : " + data.classAttribute().name());
        System.out.println();

        for (int i = 0; i < data.numAttributes(); i++) {
            Attribute a = data.attribute(i);
            AttributeStats st = data.attributeStats(i);
            if (a.isNumeric()) {
                System.out.printf("%d. %-12s numeric  min=%.1f max=%.1f "
                    + "mean=%.2f sd=%.2f%n", i + 1, a.name(),
                    st.numericStats.min, st.numericStats.max,
                    st.numericStats.mean, st.numericStats.stdDev);
            } else {
                System.out.printf("%d. %-12s nominal  %s%n", i + 1,
                    a.name(), a.toString().replaceAll(".*\\{", "{"));
            }
        }

        System.out.println("\nClass distribution:");
        int[] counts = data.attributeStats(data.classIndex()).nominalCounts;
        for (int c = 0; c < counts.length; c++) {
            System.out.println("  " + data.classAttribute().value(c)
                + " = " + counts[c]);
        }
        System.out.println("\nFirst 3 instances:");
        for (int i = 0; i < 3; i++) {
            System.out.println("  " + data.instance(i));
        }
    }
}
