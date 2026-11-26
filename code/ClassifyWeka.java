import java.util.Random;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.trees.J48;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

public class ClassifyWeka {
    public static void main(String[] args) throws Exception {
        Instances data = DataSource.read("data/iris.arff");
        data.setClassIndex(data.numAttributes() - 1);

        Classifier[] models = {new J48(), new NaiveBayes()};
        String[] names = {"J48 (decision tree)", "Naive Bayes"};

        for (int m = 0; m < models.length; m++) {
            Evaluation eval = new Evaluation(data);
            eval.crossValidateModel(models[m], data, 10, new Random(1));

            System.out.println("=== " + names[m] + " : 10-fold CV ===");
            System.out.printf("Correctly classified : %.0f of %.0f "
                + "(%.2f %%)%n", eval.correct(), eval.numInstances(),
                eval.pctCorrect());
            System.out.printf("Kappa statistic      : %.4f%n",
                eval.kappa());
            System.out.printf("Mean absolute error  : %.4f%n",
                eval.meanAbsoluteError());
            System.out.printf("Weighted precision   : %.3f%n",
                eval.weightedPrecision());
            System.out.printf("Weighted recall      : %.3f%n",
                eval.weightedRecall());
            System.out.printf("Weighted F-measure   : %.3f%n",
                eval.weightedFMeasure());
            System.out.println(eval.toMatrixString("Confusion matrix"));
        }

        J48 tree = new J48();
        tree.buildClassifier(data);
        System.out.println("=== J48 tree built on full data ===");
        System.out.println(tree);
    }
}
