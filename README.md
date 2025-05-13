
# 📈 Daily Stock Price ETL Pipeline using Apache Airflow ☁️
![screenshot](https://github.com/Bhargav-Barewar/Stock-Data-ETL-Pipeline-to-S3/blob/main/Daily_Stock_Price_ETL_Workflow.png)

This project is an automated **ETL pipeline** built with **Apache Airflow**, designed to:

✅ **Extract** historical stock data for AAPL from the Financial Modeling Prep API  
🔧 **Transform** it by calculating technical indicators (50-day & 200-day SMA)  
☁️ **Load** it into an Amazon S3 bucket as a CSV file

All this happens automatically every day via Airflow 💫

---

## 🧰 Tech Stack Used


- 🐳 Docker – to containerize Airflow for easy and consistent execution  
- 🪂 Apache Airflow – for scheduling and automation
- 🐍 Python – main language used
- 🐼 Pandas – for data transformation
- 🛢️ Boto3 – to connect and upload to Amazon S3
- 🔐 FinancialModelingPrep API – to fetch stock data

---

## 📁 Project Structure

```bash
📦
 └── dags/
     └── stock_data_ETL.py   # The main Airflow DAG file
```

---

## 🔁 How the ETL Works (Step-by-Step)

### 1. **Extract**
Fetches last **200 days** of AAPL stock price data from the FMP API  
→ Saves it as a raw CSV: `/tmp/stock_raw.csv`

### 2. **Transform**
Reads the raw data and calculates:
- 📊 50-day Simple Moving Average (`50_SMA`)
- 📊 200-day Simple Moving Average (`200_SMA`)  
→ Saves the final output to `/tmp/stock_transformed.csv`

### 3. **Load**
Uploads the cleaned and transformed file to your **Amazon S3 bucket** with a name like:
```
AAPL_2025-05-12.csv
```

### 4. **Cleanup**
To keep the system clean, it automatically deletes:
- `/tmp/stock_raw.csv`
- `/tmp/stock_transformed.csv`

✅ No leftover files. Clean machine. 🧹

---

## 🔐 Security – Using Airflow Variables

All sensitive credentials (like API keys and AWS secrets) are stored securely using **Airflow Variables**, not hardcoded in the script.  
This is a best practice to keep your credentials safe 💡

---

## 🖥️ Setup Instructions (for Beginners)

### ✅ Step 1: Clone the Repo
```bash
git clone https://github.com/Bhargav-Barewar/Stock-Data-ETL-Pipeline-to-S3.git
cd Stock-Data-ETL-Pipeline-to-S3
```

### ✅ Step 2: Set up Apache Airflow
Use the official **Airflow Docker setup**:

👉 [Airflow Docker Setup Guide](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)

---
### ✅ Step 3: Installing Requests, Boto3, and Pandas in Airflow Docker Container
## Steps to Install Packages

1. **Access the container**:
   ```bash
   docker exec -it <container_name> bash
   ```

2. **Check if packages are installed**:
   ```bash
   pip show requests
   pip show boto3
   ```

3. **Install the packages if not present**:
   ```bash
   pip install requests boto3 pandas
   ```

## Notes
- These changes will be lost if the container is stopped or recreated. To make them persistent, modify the Dockerfile or `docker-compose.yml` file to include these packages.

## 🧩 Step 4: Add Airflow Variables (via GUI)

Open Airflow in your browser:  
📍 `http://localhost:8080`

Then:

1. Click **Admin → Variables**
2. Click the "**+**" button to add the following key–value pairs:
3. Get api key from [link](https://site.financialmodelingprep.com/developer/docs/daily-chart-charts)

| Variable Name     | Purpose                          | Example Value               |
|------------------|----------------------------------|-----------------------------|
| `api_key`        | API key for FMP                  | `your_fmp_api_key`     |
| `aws_access_key` | AWS access key                   | `your_aws_access_key`       |
| `aws_secret_key` | AWS secret access key            | `your_aws_secret_key`       |
| `s3_bucket`      | Your S3 bucket name              | `your-bucket-name`          |

✅ These variables are used **securely inside the DAG** — not visible to others!

---

## 🚦 Step 4: Run the DAG

1. Start your Airflow environment:
```bash
airflow scheduler
airflow webserver
```

2. In Airflow UI, find and **enable** the DAG:
   - Name: `stock_etl_to_s3`
   - Turn it ON ✅
   - Click ▶️ to run manually or wait for the daily schedule

---

## 📂 Output in Amazon S3

Each run creates a file like this in your S3 bucket:
```
s3://your-s3-bucket/AAPL_2025-05-12.csv
```

✅ The file contains stock data + 50-day & 200-day SMAs

---
## 🎯 Why Use This?

This project is great if you want to:

- ✅ Learn **Airflow with real data**
- ✅ Understand how to use **ETL pipelines**
- ✅ Practice **secure credential management**
- ✅ Combine **Python, APIs, AWS, and automation**

---

## ✨ Author

Made with ❤️ and ☕ by **Bhargav-Barewar**

---
