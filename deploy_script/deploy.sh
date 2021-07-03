source ./deploy_script/setup.sh
gcloud config set project $PROJECT_ID

gcloud functions deploy $FUNCTION_NAME\
    --runtime python37\
    --trigger-http\
    --entry-point=handle_message\
    --region=asia-east2