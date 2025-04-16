import polars as pl
import os

def analyze_patient_cohorts(input_file: str) -> pl.DataFrame:
    """
    Analyze patient cohorts based on BMI ranges.
    Args:
        input_file: Path to the input CSV file
    Returns:
        DataFrame containing cohort analysis results with columns:
        - bmi_range: The BMI range (e.g., "Underweight", "Normal", "Overweight", "Obese")
        - avg_glucose: Mean glucose level by BMI range
        - patient_count: Number of patients by BMI range
        - avg_age: Mean age by BMI range
    """
    # Create temporary parquet file
    parquet_file = "patients_temp.parquet" 
    
    try:
        # Convert CSV to Parquet for efficient processing
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
            
        pl.read_csv(input_file).write_parquet(parquet_file)
        
        # Create a lazy query to analyze cohorts
        cohort_results = pl.scan_parquet(parquet_file).pipe(
            lambda df: df.filter((pl.col("BMI") >= 10) & (pl.col("BMI") <= 60))
        ).pipe(
            lambda df: df.select(["BMI", "Glucose", "Age"])
        ).pipe(
            # Fix: Use when-then-otherwise instead of cut() to avoid shape errors
            lambda df: df.with_columns(
                pl.when(pl.col("BMI") < 18.5).then(pl.lit("Underweight"))
                  .when((pl.col("BMI") >= 18.5) & (pl.col("BMI") < 25)).then(pl.lit("Normal"))
                  .when((pl.col("BMI") >= 25) & (pl.col("BMI") < 30)).then(pl.lit("Overweight"))
                  .otherwise(pl.lit("Obese"))
                  .alias("bmi_range")
            )
        ).pipe(
            lambda df: df.group_by("bmi_range").agg([
                pl.col("Glucose").mean().alias("avg_glucose"),
                pl.len().alias("patient_count"),
                pl.col("Age").mean().alias("avg_age")
            ])
        ).collect()
        
        return cohort_results
    
    except Exception as e:
        print(f"Error during cohort analysis: {e}")
        raise
    
    finally:
        # Cleanup temporary file
        if os.path.exists(parquet_file):
            try:
                os.remove(parquet_file)
            except:
                print(f"Warning: Could not remove temporary file {parquet_file}")

def main():
    # Input file
    input_file = "patients_large.csv"
    
    try:
        # Run analysis
        results = analyze_patient_cohorts(input_file)
        
        # Print summary statistics
        print("Cohort Analysis Results:")
        print(results)
        
    except Exception as e:
        print(f"Analysis failed: {e}")

if __name__ == "__main__":
    main()    




