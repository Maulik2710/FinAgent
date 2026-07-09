from app.data_pipeline.downloader import download_all_stocks
from app.feature_engineering.pipeline import engineer_features_pipeline

def main():
    download_all_stocks()
    engineer_features_pipeline()

if __name__ == "__main__":
    main()