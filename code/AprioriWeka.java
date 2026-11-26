import weka.associations.Apriori;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

public class AprioriWeka {
    public static void main(String[] args) throws Exception {
        Instances data = DataSource.read("data/weather.nominal.arff");
        System.out.println("Dataset: " + data.relationName() + "  ("
            + data.numInstances() + " instances, "
            + data.numAttributes() + " attributes)\n");

        Apriori apriori = new Apriori();
        apriori.setNumRules(10);
        apriori.setLowerBoundMinSupport(0.2);
        apriori.setMinMetric(0.9);
        apriori.buildAssociations(data);

        System.out.println(apriori);
    }
}
