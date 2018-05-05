#! /bin/bash
# CREATE DATABASE postgresql

echo
echo "Creating database  ..."
sudo -u postgres psql -c "CREATE DATABASE twitterharassment_db;"

echo 
echo "Creating TABLE status ..."
psql twitterharassment_db -c "CREATE TABLE IF NOT EXISTS status (id INT PRIMARY KEY, description VARCHAR(25));"

echo 
echo "Populating TABLE status data ..."
psql twitterharassment_db -c "INSERT INTO status (id, description) VALUES 
				(0, 'Not processed'),
				(1, 'In progress'),
				(2, 'Completed');"

echo 
echo "Creating TABLE friends ..."
psql twitterharassment_db -c "CREATE TABLE IF NOT EXISTS friends (handle  VARCHAR(25) PRIMARY KEY, status INT);"

echo 
echo "Creating TABLE followers ..."
psql twitterharassment_db -c "CREATE TABLE IF NOT EXISTS followers (handle  VARCHAR(25) PRIMARY KEY, status INT);"

echo 
echo "Creating TABLE tweets ..."
psql twitterharassment_db -c "CREATE TABLE IF NOT EXISTS tweets (handle  VARCHAR(25) PRIMARY KEY, status INT);"

echo
echo "Creating TABLE profiles ..."
psql twitterharassment_db -c "CREATE TABLE IF NOT EXISTS profiles (handle  VARCHAR(25) PRIMARY KEY, status INT);"

echo 
echo "GRANTING access to USER:wsdl ON TABLE friends ..."
psql twitterharassment_db -c "GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON friends TO wsdl;"

echo "GRANTING access to USER:wsdl ON TABLE followers ..."
psql twitterharassment_db -c "GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON followers TO wsdl;"

echo "GRANTING access to USER:wsdl ON TABLE tweets ..."
psql twitterharassment_db -c "GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON tweets TO wsdl;"

echo "GRANTING access to USER:wsdl ON TABLE profiles ..."
psql twitterharassment_db -c "GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON profiles TO wsdl;"
