FROM public.ecr.aws/lambda/python:3.11

#Python dependencies to install
RUN pip install --no-cache-dir \
    playwright==1.49.0 \
    boto3==1.34.34 \
    requests==2.31.0 \
    python-dotenv

#Playwright dependencies to install
RUN playwright install chromium
RUN playwright install-deps chromium

#Copy the code
COPY main.py config.py db_manager.py notifier.py ${LAMBDA_TASK_ROOT}/
COPY scrapers/ ${LAMBDA_TASK_ROOT}/scrapers/

#Set lambda function to run
CMD ["main.lambda_handler"]