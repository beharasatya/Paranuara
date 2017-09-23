# paranuara
A simple API to look up companies and people in Paranuara planet


Please install the below python libraries for the API to work

#pip3
-- sudo apt-get install python3-pip

# pymongo
-- pip3 install pymongo

# bottle
 -- pip3 install bottle
 
After pulling the code fromt he repository please traverse inside the "src/" directory.

Run 'python3 init_tables.py' to load the data into local mongodb

Run 'python3 search.py' to run the API as a locally hosted website

You can see the API by entering "http://127.0.0.1:8080/" in your browser.



I had already hosted it on my AWS EC2 instance. Please have a look

http://ec2-13-55-56-159.ap-southeast-2.compute.amazonaws.com:8080/

