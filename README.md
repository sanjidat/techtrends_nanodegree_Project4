# techtrends_nanodegree_Project4

# Overview
TechTrends is an online website used as a news sharing platform, that enables consumers to access the latest news within the cloud-native ecosystem. In addition to accessing the available articles, readers are able to create new media articles and share them.

<img src="Images/techtrend.jpg" alt="" width="500" height="350" style="border:5px solid black">

To run this application follow these steps:

1. Initialize the database by using the python init_db.py command. This creates or overwrites (if the file already exists) the database.db file that is used to store and access the available posts.
2. Run the TechTrends application by using the python app.py command. The application is running on port 3111 and you can access it by querying the http://127.0.0.1:3111/ endpoint.

# Dependencies
Make sure you have the following dependencies installed:
1. Install Python using the official Python document https://www.python.org/downloads/
2. Install Git using the using the instruction provided in the document https://git-scm.com/downloads
3. Install Docker using the using the instruction provided in the document https://docs.docker.com/get-docker/
4. Install Vagrant using the using the instruction provided in the document https://www.vagrantup.com/downloads
5. Install VirtualBox using the using the instruction provided in the document https://www.virtualbox.org/wiki/Downloads. Ensure that you have VirtualBox 6.1.16 or higher installed.

# Step 1: Best Practices For Application Deployment
Throughout this step, you should apply some of the learned best development practices to the TechTrends project. As a result, you will add the metrics and health check endpoints, in addition to the logging functionality.

1. Check the Python installation and clone the https://github.com/sanjidat/techtrends_nanodegree_Project4.git repository
2. python3 --version  (To Check the Python version installed)
3. cd techtrends_nanodegree_Project4/techtrends/

<h3>Healthcheck endpoint</h3>
@app.route('/healthz')

def healthz():

  response = app.response_class(
          response=json.dumps({"result":"OK - healthy"}),
          status=200,
          mimetype='application/json'
  )
  return response
<h3>Metrics endpoint</h3>
@app.route('/metrics')
def metrics():
  connection = get_db_connection()
  number_of_posts = connection.execute('SELECT * FROM number_of_posts').fetchall
  connection.close()  
  response = app.response_class(
          response=json.dumps({"status":"success","code":0,"data":{"UserCount":140,"UserCountActive":23}}),
          status=200,
          mimetype='application/json'
  )
  return response
<h3>Logs</h3>
if __name__ == "__main__":
   logging.basicConfig(filename='app.log',level=logging.DEBUG, handlers=[logging.StreamHandler(sys.stdout), logging.StreamHandler(sys.stderr)])
   app.run(host='0.0.0.0', port='3111')

