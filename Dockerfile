FROM public.ecr.aws/lambda/python:3.10


COPY price_bitcoin_early.csv ${LAMBDA_TASK_ROOT}/
COPY alerts/ ${LAMBDA_TASK_ROOT}/alerts/
COPY requirements.txt ${LAMBDA_TASK_ROOT}


CMD ["alerts/cycle_pi_alert.lambda_handler"]