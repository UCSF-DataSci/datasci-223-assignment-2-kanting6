# Patient Cohort Analysis Report

## Analysis Approach

This analysis focused on categorizing patients into different BMI cohorts and examining key health metrics across these groups. The implementation leverages Polars, a high-performance DataFrame library, to process patient data efficiently with minimal memory overhead.

### Methodology

1. **Data Transformation**: Initial conversion of CSV data to Parquet format for optimized read/write operations and columnar storage benefits
2. **BMI Cohort Classification**: Patients were categorized into four clinically relevant BMI ranges:
   - Underweight (BMI < 18.5)
   - Normal (BMI 18.5-24.9)
   - Overweight (BMI 25-29.9)
   - Obese (BMI ≥ 30)
3. **Aggregate Analysis**: For each BMI cohort, we calculated:
   - Average glucose levels
   - Total patient count
   - Average age

## Patterns and Insights

Our analysis revealed several noteworthy patterns across BMI cohorts:

1. **Glucose Correlation**: Average glucose levels showed a positive correlation with increasing BMI categories, with the highest values typically appearing in the "Obese" cohort. This aligns with established medical literature linking higher BMI to increased risk of insulin resistance and diabetes.

2. **Age Distribution**: The analysis identified demographic patterns in BMI distribution, with different age groups showing varying tendencies toward specific BMI categories. This information could support targeted interventions for particular age/BMI combinations.

3. **Cohort Sizes**: The distribution of patients across BMI categories provides valuable population-level insights about the prevalence of different weight classifications in the studied population.

## Leveraging Polars for Efficiency

We utilized several Polars features to optimize performance and memory usage during analysis:

1. **Lazy Evaluation**: The implementation uses Polars' lazy execution model through `scan_parquet()` and chained `pipe()` operations. This approach enables query optimization and reduces memory overhead by delaying computation until explicitly requested with `collect()`.

2. **Columnar Processing**: By using Parquet's columnar format, we reduced I/O operations and memory usage, accessing only the necessary columns ("BMI", "Glucose", "Age") for analysis.

3. **Efficient Aggregation**: Polars' optimized group-by operations allowed for rapid calculation of metrics across cohorts using native functions.

