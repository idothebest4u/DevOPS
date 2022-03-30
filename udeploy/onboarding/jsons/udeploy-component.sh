echo "Make sure to update the ms-folio variable in json files to required app name"
echo " Usage : sed -i 's/APP_NAME/ms-folio/g' *"
read -p "Press any key to continue... " -n1 -s
echo "Creating Application Component"
curl -k -u admin:admin https://3.3.87.13:8443/cli/component/create -X PUT -d @createAppComponent.json | jq .
echo "Creating Application Indexes Componenet"
curl -k -u admin:admin https://3.3.87.13:8443/cli/component/create -X PUT -d @createAppIndexComponent.json | jq .
echo "Make sure to attach UOAPI tag to newly created App component and UOINDEXES to newly created App Indexes Xomponent at this time."
## curl -k -u admin:admin https://3.3.87.13:8443/rest/tag/Component -X PUT -d @addComponentTag.json
read -p "Press any key to continue... " -n1 -s

