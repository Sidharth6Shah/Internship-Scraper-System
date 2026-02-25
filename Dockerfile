FROM public.ecr.aws/lambda/python:3.12

#Install system dependencies for Chromium
RUN dnf install -y \
    atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm && \
    dnf clean all

#Python dependencies to install
RUN pip install --no-cache-dir \
    playwright==1.49.0 \
    boto3==1.34.34 \
    requests==2.31.0 \
    python-dotenv

#Playwright dependencies to install
RUN playwright install chromium

#Copy the code
COPY main.py config.py db_manager.py notifier.py ${LAMBDA_TASK_ROOT}/
COPY scrapers/ ${LAMBDA_TASK_ROOT}/scrapers/
RUN chmod -R 755 ${LAMBDA_TASK_ROOT}

#Set lambda function to run
CMD ["main.lambda_handler"]