# twitter.py
 Twitter Clone

## Installation

In this section, we'll cover how to install Twitter.py in developer mode on a Linux system, specifically Ubuntu, which is a popular and user-friendly distribution based on Debian.

Please note that we recommend using a Linux operating system, preferably Debian-based, for the best experience with Twitter.py. While it's possible to run Twitter.py on other operating systems, we can't guarantee that it will work as expected.

With that in mind, let's get started with the installation process.

### Python

Here are the instructions to install Twitter.py in developer mode with Python:

1. Run the following command in the terminal to update the package repository:

    ```shell
    sudo apt update
    ```

2. Install python3, pip, and venv by running the following command:

    ```shell
    sudo apt-get install python3 python3-pip python3-venv -y
    ```

3. Clone the Twitter.py repository using the following command:

    ```shell
    git clone https://github.com/milosnowcat/twitter.py.git
    ```

4. Navigate to the **'twitter.py'** directory by running the following command:

    ```shell
    cd twitter.py
    ```

5. Create a Python virtual environment by running the following command:

    ```shell
    python3 -m venv env
    ```

6. Activate the Python virtual environment by running the following command:

    ```shell
    source env/bin/activate
    ```

7. Install the required dependencies by running the following command:

    ```shell
    pip3 install -r requirements.txt
    ```

8. Run the database migrations by running the following command:

    ```shell
    python3 manage.py migrate
    ```

9. Create a superuser by running the following command:

    ```shell
    python3 manage.py createsuperuser
    ```

10. Start the development server by running the following command:

    ```shell
    python3 manage.py runserver
    ```

11. Open your web browser and enter the following address in the address bar: **'http://localhost:8000'**. You will see the application in action and can log in with the credentials you specified during the superuser creation.

### Docker Compose

Here are the instructions to install Twitter.py in developer mode with docker-compose:

1. Run the following command in the terminal to update the package repository:

    ```shell
    sudo apt update
    ```

2. Install Docker and Docker Compose by running the following command:

    ```shell
    sudo apt-get install docker.io docker-compose -y
    ```

3. Clone the Twitter.py repository using the following command:

    ```shell
    git clone https://github.com/milosnowcat/twitter.py.git
    ```

4. Navigate to the **'twitter.py'** directory by running the following command:

    ```shell
    cd twitter.py
    ```

5. Start the Docker container with the following command:

    ```shell
    sudo docker-compose up -d --build
    ```

6. Open your web browser and enter the following address in the address bar: **'http://localhost:8000'**. You will see the application in action and can log in with the following credentials: username: **'admin'**, password: **'admin'**.

7. To stop the Docker container, run the following command:

    ```shell
    sudo docker-compose stop
    ```

8. To start the Docker container again, run the following command:

    ```shell
    sudo docker-compose start
    ```

### Docker

Here are the instructions to install Twitter.py in developer mode with Docker:

1. Run the following command in the terminal to update the package repository:

    ```shell
    sudo apt update
    ```

2. Install Docker by running the following command:

    ```shell
    sudo apt-get install docker.io -y
    ```

3. Pull the Twitter.py image from the GHCR by running the following command:

    ```shell
    sudo docker pull ghcr.io/milosnowcat/twitter.py:6.0.15
    ```

4. Start the Twitter.py container by running the following command:

    ```shell
    sudo docker run -p 8000:8000 ghcr.io/milosnowcat/twitter.py:6.0.15
    ```

5. Open your web browser and enter the following address in the address bar: **'http://localhost:8000'**. You will see the application in action and can log in with the following credentials: username: **admin**, password: **admin**.
