# Step 1: Start with a base Python image
FROM python:3.12.3

RUN pip install --upgrade pip
RUN pip install gunicorn

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . .

# Step 4: Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port Flask will run on (default is 5000)
EXPOSE 5000

# Step 6: Set the command to run your application
CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:5000", "app.main:app"]

