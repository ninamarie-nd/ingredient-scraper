#!/usr/bin/env bash
# Deploys the label reader (Cloud Vision OCR) to Cloud Functions gen 2.
# Run in Cloud Shell from the label-reader folder: bash deploy.sh
set -euo pipefail
PROJECT=puberty-scanner-ocr-514017
REGION=us-central1
SECRET=vision-api-key

gcloud config set project "$PROJECT"
gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com run.googleapis.com \
  artifactregistry.googleapis.com secretmanager.googleapis.com eventarc.googleapis.com

PN=$(gcloud projects describe "$PROJECT" --format='value(projectNumber)')
gcloud secrets add-iam-policy-binding "$SECRET" \
  --member="serviceAccount:${PN}-compute@developer.gserviceaccount.com" \
  --role=roles/secretmanager.secretAccessor --project="$PROJECT" >/dev/null

gcloud functions deploy read_label --gen2 --runtime=python312 --region="$REGION" \
  --source=. --entry-point=read_label --trigger-http --allow-unauthenticated \
  --set-secrets="VISION_API_KEY=${SECRET}:latest" --max-instances=5 --memory=512MB --quiet

URL=$(gcloud functions describe read_label --gen2 --region="$REGION" --format='value(serviceConfig.uri)')
echo "FUNCTION_URL=$URL"
echo "Test (should print 403 origin not allowed):"
curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Origin: https://example.com" "$URL" || true
