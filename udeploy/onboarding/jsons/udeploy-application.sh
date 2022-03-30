echo "Creating Application"
curl -k -u admin:admin https://3.3.87.13:8443/rest/deploy/application/createFromWizard -X PUT -d @createApplication.json | jq .
read -p "Press any key to continue... " -n1 -s

