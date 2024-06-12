follow steps 1-3 from https://github.com/Chewy-Inc/pricebot-pse

aws configure sso --profile worker-pricing-analytics-dev #profile name in aws. Make sure to put this in docker compose:

```AWS_PROFILE: worker-pricing-analytics-dev```

Create a profile:

```% aws configure sso --profile worker-pricing-analytics-dev```

Test created profile: % aws s3 ls --profile worker-pricing-analytics-dev

```AWS_PROFILE: worker-pricing-analytics-dev #```

notes:

```
% docker compose up
% docker compose up -d --build
% aws-sso-util login --print-creds
```


Login to image:

```docker exec -it airflow-local-dev-airflow-1 bash```

