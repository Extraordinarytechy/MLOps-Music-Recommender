import pandas as pd
import mlflow
import mlflow.sklearn
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split, cross_validate
from melorec.processing.feature_engine import get_training_data
from melorec.config import MODEL_PATH
import joblib

def run_training():
    print("Starting model training...")
    
    # 1. Get Data
    df = get_training_data()
    
    # 2. Load data into Surprise
    # The reader defines the 1-5 rating scale
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'song_id', 'rating']], reader)
    
    # 3. Start MLflow run
    with mlflow.start_run():
        
        # 4. Define and train model
        params = {
            'n_factors': 150,
            'n_epochs': 30,
            'lr_all': 0.005,
            'reg_all': 0.02
        }
        model = SVD(n_factors=params['n_factors'], 
                    n_epochs=params['n_epochs'], 
                    lr_all=params['lr_all'], 
                    reg_all=params['reg_all'])
        
        print("Cross-validating...")
        # 5. Evaluate
        cv_results = cross_validate(model, data, measures=['RMSE', 'MAE'], cv=5, verbose=False)
        
        # Log params and metrics
        mlflow.log_params(params)
        mlflow.log_metric("rmse_mean", cv_results['test_rmse'].mean())
        mlflow.log_metric("mae_mean", cv_results['test_mae'].mean())
        
        print(f"Mean RMSE: {cv_results['test_rmse'].mean()}")
        
        # 6. Re-train on full dataset
        print("Training on full dataset...")
        trainset = data.build_full_trainset()
        model.fit(trainset)
        
        # 7. Save the model
        joblib.dump(model, MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")
        mlflow.sklearn.log_model(model, "svd_model")

if __name__ == "__main__":
    run_training()