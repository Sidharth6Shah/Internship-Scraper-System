FROM public.ecr.aws/lambda/python:3.12

#Install system dependencies for Chrome
RUN dnf install -y \
    unzip \
    atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm && \
    dnf clean all

#Python dependencies to install
RUN pip install --no-cache-dir \
    selenium==4.27.1 \
    boto3==1.34.34 \
    requests==2.31.0 \
    python-dotenv

#Install Chrome and Chromedriver
RUN dnf install -y wget unzip && \
    CHROME_VERSION=131.0.6778.204 && \
    wget -q https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip && \
    unzip chrome-linux64.zip && \
    mkdir -p /opt/chrome && \
    mv chrome-linux64 /opt/chrome/ && \
    chmod +x /opt/chrome/chrome-linux64/chrome && \
    rm chrome-linux64.zip && \
    wget -q https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /opt/chromedriver && \
    chmod +x /opt/chromedriver && \
    rm -rf chromedriver-linux64.zip chromedriver-linux64 && \
    dnf clean all

#Copy the code
COPY main.py config.py db_manager.py notifier.py ${LAMBDA_TASK_ROOT}/
COPY scrapers/ ${LAMBDA_TASK_ROOT}/scrapers/
RUN chmod -R 755 ${LAMBDA_TASK_ROOT}

#Set lambda function to run
CMD ["main.lambda_handler"]