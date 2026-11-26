import weka.clusterers.ClusterEvaluation;
import weka.clusterers.SimpleKMeans;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;

public class ClusterWeka {
    public static void main(String[] args) throws Exception {
        Instances data = DataSource.read("data/iris.arff");

        Remove remove = new Remove();
        remove.setAttributeIndices("last");
        remove.setInputFormat(data);
        Instances noClass = Filter.useFilter(data, remove);

        SimpleKMeans kmeans = new SimpleKMeans();
        kmeans.setNumClusters(3);
        kmeans.setSeed(10);
        kmeans.buildClusterer(noClass);

        data.setClassIndex(data.numAttributes() - 1);
        ClusterEvaluation eval = new ClusterEvaluation();
        eval.setClusterer(kmeans);
        eval.evaluateClusterer(data);
        System.out.println(eval.clusterResultsToString());
    }
}
